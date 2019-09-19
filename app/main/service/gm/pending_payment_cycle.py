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
        for r in range(datetime.today().month):
            pv_expected = int(monthly_actual_pv[r]['total_pv']) - int(monthly_po_cancel[r]['total_pv_cancel'])
            rowset = [
                common.GetMonthName(r+1),
                "{:,.0f}".format(int(monthly_actual_pv[r]['total_pv'])),
                "{:,.0f}".format(int(monthly_po_cancel[r]['total_pv_cancel'])),
                "{:,.0f}".format(float(pv_expected)),
                ]
            rowset = rowset + pending_payment_month[int(r)]
            balance_pv = pv_expected - rowset[-1]
            rowset[-1] = "{:,.0f}".format(rowset[-1])
            rowset.append("{:,.0f}".format(balance_pv))
            pending_payment_data.append(self.PendingPaymentDatasetConstruct(rowset))
        
        return pending_payment_data
    
    def NewPendingPaymentCycle(self):
        start_time = datetime.now()
        print('----start query----')
        dataset = self.CreatePendingPaymentCycleWS()
        print('----end query-----')
        end_time = datetime.now()

        input = {
            "ws_name": "GM_PENDING_PAYMENT_CYCLE",
            "ws_is_active": "1",
            "ws_desc": "GM Pending Payment Cycle - Pending Payment as at {}".format(date.today().strftime("%d %B %Y")),
            "ws_group": "SM",
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
            content = []
            grand_total = 0
            total_pv = gm_query.pending_payment_cycle_monthly_payment(i+1)
            month_pos = 0
            for m in range(12):
                if m < i:
                    content.append("")
                elif m+1 > datetime.today().month:
                    content.append("null")
                else:
                    grand_total += float(total_pv[month_pos]['total_pv'])
                    current_pos = "{:,.0f}".format(float(total_pv[month_pos]['total_pv'])) if len(total_pv) > 0 and total_pv[month_pos]['total_pv'] != '' else ""
                    content.append(current_pos)
                    month_pos += 1
            content.append(grand_total)
            to_current_month.append(content)
        return to_current_month

    def PendingPaymentRowSetter(self, rowset):
        print(rowset)
        return rowset
        

    def PendingPaymentDatasetConstruct(self, rowset):
        start_column = 100
        content = {}
        for i in range(len(self.HEADING)):
            content[start_column+i] = rowset[i]
        return content