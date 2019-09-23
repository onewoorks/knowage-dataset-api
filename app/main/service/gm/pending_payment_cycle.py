from datetime import datetime, date
from ..common import CommonMethod
from ...model.mysql.government_management import MYSQL_GM_QUERY

import json

common = CommonMethod()

class PENDING_PAYMENT_DATASET:
    HEADING = [
        'MONTH PV', 'ACTUAL PV', 'PO CANCEL','PV EXPECTED',
        'JAN',
        'FEB',
        'MARCH',
        'APRIL',
        'MAY',
        'JUNE', 'JULY', 'AUGUST', 'SEPT','OCT','NOV','DEC',
        'Grand Total', 'BALANCE PV'
    ]

class PendingPaymentCyclePerformanceUpdate(PENDING_PAYMENT_DATASET):
    def PendingPaymentCycle(self,mode):
        print(mode)
        return self.TemplateCycleBuilder(self.SAMPLE_PENDING_PAYMENT)

    def PendingPaymentCycleMilFix(self, returned_data):
        fixData = []
        s = 0
        for i in returned_data[1:]:
            if s > 0 :
                inn = self.ConvertValue(i)
            else :
                inn = i
            fixData.append(inn)
            s += 1
        return fixData

    def ConvertValue(self,dict_values):
        clean = {}
        for i in dict_values:
            if i != 'a' and dict_values[i] != "":
                print("{} -> {}".format(i,dict_values[i]))
                val = format(dict_values[i],',d')
            else:
                val = dict_values[i]
            clean[i] = val
        return clean

    def PendingPaymentCycleFromETL(self):
        ws_name = "GM_PENDING_PAYMENT_CYCLE"
        gm_query = MYSQL_GM_QUERY()
        existed = gm_query.Get_Latest_WS(ws_name)
        if len(existed) > 0:
            dataset = json.loads(existed[0]['ws_data'])
        else:
            dataset = self.NewPendingPaymentCycle()
        return dataset

    def CreatePendingPaymentCycleWS(self):
        gm_query = MYSQL_GM_QUERY()
        monthly_actual_pv = gm_query.pending_payment_cycle_monthly_actual_pv()
        monthly_po_cancel = gm_query.pending_payment_cycle_monthly_po_cancel()
        heading = self.PendingPaymentDatasetConstruct(self.HEADING)
        pending_payment_month = self.PendingPaymentMonthlyInfo()
        pending_payment_data = [heading]
        pending_payment_data_percent = [heading]
        plain_value = []
        for r in range(datetime.today().month):
            pv_expected = float(monthly_actual_pv[r]['total_pv']) - float(monthly_po_cancel[r]['total_pv_cancel'])
            rowset = [
                common.GetMonthName(r+1),
                "{:,.2f}".format(float(monthly_actual_pv[r]['total_pv'])),
                "{:,.2f}".format(float(monthly_po_cancel[r]['total_pv_cancel'])),
                "{:,.2f}".format(float(pv_expected)),
                ]
            by_value = rowset + pending_payment_month[int(r)]
            by_percentage = rowset + self.PendingPaymentCyclePercentage(pending_payment_month[int(r)],pv_expected)
            
            balance_pv = pv_expected - by_value[-1]
            by_value[-1] = "{:,.2f}".format(by_value[-1])
            by_value.append("{:,.2f}".format(balance_pv))
            plain_value.append(by_value)

            balance_pv_percentage = "{:.2f} %".format((balance_pv/pv_expected)*100)
            by_percentage.append(balance_pv_percentage)
            pending_payment_data.append(self.PendingPaymentDatasetConstruct(by_value))
            pending_payment_data_percent.append(self.PendingPaymentDatasetConstruct(by_percentage))
        
        pending_payment_data.append(self.PendingPaymentDatasetConstruct(self.PendingPaymentCycleSummary(plain_value)))
        pending_payment_data_percent.append(self.PendingPaymentDatasetConstruct(self.PendingPaymentCycleSummary(plain_value,'percent')))
        
        return {
            "by_value" : pending_payment_data,
            "by_percent" : pending_payment_data_percent,
            "pivot" : self.PendingPaymentToPivot(plain_value),
            "pivot_summary" : self.PendingPaymentPivotSummary(pending_payment_data[-1])
        }

    def PendingPaymentCyclePercentage(self, rowset, pv_value):
        for index, item in enumerate(rowset):
            if item != "null" and item != "":
                value = str(item).replace(',','')
                rowset[index] = "{:,.2f} %".format((float(value)/float(pv_value))*100)
        return rowset

    def PendingPaymentCycleSummary(self, dataset, mode='value'):
        summary = []
        for value in dataset:
            month_column = []
            for mv in value[1:]:
                month_column.append(common.StringToNumber(mv))
            summary.append(month_column)
            
        sum_data = []
        for to_sum in summary:
            for i in range(len(to_sum)):
                if len(sum_data) < len(to_sum):
                    sum_data.append(to_sum[i])
                else:
                    sum_data[i] = sum_data[i] + to_sum[i]

        for index, value in enumerate(sum_data):
            sum_data[index] = common.NumberToFormat(value)

        if mode != 'value':
            for ind, update in enumerate(sum_data[3:]):
                sum_data[ind+3] = ""

        sum_data.insert(0,'Summary')
        return sum_data
    
    def PendingPaymentToPivot(self, dataset):
        pivot = []
        for m in range(len(dataset)):
            content = {}
            content['index'] = m+1
            content['month'] = common.GetMonthName(m+1).upper()
            content['actual_pv'] = dataset[m][1].replace(',','')
            content['po_cancel'] = dataset[m][2].replace(',','')
            content['pv_expected'] = dataset[m][3].replace(',','')
            pivot.append(content)
        return pivot
    
    def PendingPaymentPivotSummary(self, dataset):
        pivot_summary = [
            {
                "name" : "ACTUAL PV",
                "value" : dataset[101].replace(',',''),
                "format_value" : dataset[101]
            },
            {
                "name" : "PO CANCEL",
                "value" : dataset[102].replace(',',''),
                "format_value" : dataset[102]
            }
        ]
        return pivot_summary
        
    def NewPendingPaymentCycle(self):
        start_time = datetime.now()
        print('-- GM PENDING PAYMENT CYCLE --')
        print('-- start query----')
        dataset = self.CreatePendingPaymentCycleWS()
        print('-- end query-----')
        end_time = datetime.now()

        input = {
            "ws_name": "GM_PENDING_PAYMENT_CYCLE",
            "ws_is_active": "1",
            "ws_desc": "GM Pending Payment Cycle - Pending Payment as at {}".format(date.today().strftime("%d %B %Y")),
            "ws_group": "GM",
            "ws_start_execute": start_time,
            "ws_end_execute": end_time,
            "ws_duration": int((end_time-start_time).total_seconds()),
            "ws_data": json.dumps(dataset),
            "ws_created_at": datetime.now(),
            "ws_updated_at": datetime.now(),
            "ws_status": "SUCCESS",
            "ws_error": ""
        }
        gm_query = MYSQL_GM_QUERY()
        gm_query.create_new_ws(input)
        return dataset

    def PendingPaymentMonthlyInfo(self):
        gm_query = MYSQL_GM_QUERY()
        to_current_month = []
        for i in range(datetime.today().month):
            by_value = []
            by_percent = []
            grand_total = 0
            total_pv = gm_query.pending_payment_cycle_monthly_payment(i+1)
            month_pos = 0
            for m in range(12):
                if m < i:
                    by_value.append("")
                    by_percent.append("")
                elif m+1 > datetime.today().month:
                    by_value.append("null")
                    by_percent.append("null")
                else:
                    grand_total += float(total_pv[month_pos]['total_pv'])
                    current_pos = "{:,.0f}".format(float(total_pv[month_pos]['total_pv'])) if len(total_pv) > 0 and total_pv[month_pos]['total_pv'] != '' else ""
                    by_value.append(current_pos)
                    month_pos += 1
            by_value.append(grand_total)
            to_current_month.append(by_value)
        return to_current_month


    def PendingPaymentDatasetConstruct(self, rowset):
        start_column = 100
        content = {}
        for i in range(len(self.HEADING)):
            content[start_column+i] = rowset[i]
        return content