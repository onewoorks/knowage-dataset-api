from datetime import datetime
from ..common import CommonMethod
from ...model.mysql.government_management import MYSQL_GM_QUERY

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
        gm_query = MYSQL_GM_QUERY()
        monthly_actual_pv = gm_query.pending_payment_cycle_monthly_actual_pv()
        monthly_po_cancel = gm_query.pending_payment_cycle_monthly_po_cancel()
        # pending_payment_data = []
        # start_column = 100



        # for i in range(datetime.today().month):
        #     columns = []
        #     for a in range(18):
        #         content = {}
        #         content[start_column+a] = 
        #         columns.append(content)
        #         print(content)
        #     print('\n')
        #     # content['month'] = monthly_actual_pv[i]['date_pv'].upper()
        #     # content['actual_pv'] = "{:,.0f}".format(int(monthly_actual_pv[i]['total_pv']))
        #     # content['po_cancel'] = "{:,.0f}".format(int(monthly_po_cancel[i]['total_pv_cancel']))
        #     # pv_expected = int(monthly_actual_pv[i]['total_pv']) - int(monthly_po_cancel[i]['total_pv_cancel'])
        #     # content['pv_expected'] = "{:,.0f}".format(pv_expected)
        #     # content['pending_payment'] = self.PendingPaymentCycleMonthlyInfo()
        #     # print(columns)
        #     # pending_payment_data.append(content)
        # return pending_payment_data
        pending_payment_data = []
        self.PendingPaymentDatasetConstruct(self.HEADING)
        self.PendingPaymentMonthlyInfo()
        for r in range(datetime.today().month):
            # print(r)
            # rowset = [
            #     int(monthly_actual_pv[r]['total_pv']),
            #     int(monthly_po_cancel[r]['total_pv_cancel']),
            #     int(monthly_actual_pv[r]['total_pv']) - int(monthly_po_cancel[r]['total_pv_cancel'])
            #     ]
            
            # rowset = rowset + self.PendingPaymentCycleMonthlyInfo(r)
            # print(self.PendingPaymentRowSetter(rowset))
            # pending_payment_data.append("")
            pass
        
        # info_row = gm_query.pending_payment_cycle_monthly_payment(datetime.today().month)
        
        return pending_payment_data

    def PendingPaymentMonthlyInfo(self):
        gm_query = MYSQL_GM_QUERY()
        for i in range(datetime.today().month):
            content = []
            total_pv = gm_query.pending_payment_cycle_monthly_payment(i+1)
            print(common.GetMonthName(i+1))

            for m in total_pv:
                content.append(m['date_index'])
            print(content)
            print('\n')


    
    
    def PendingPaymentRowSetter(self, rowset):
        content = []

        return rowset
        

    def PendingPaymentDatasetConstruct(self, rowset):
        start_column = 100
        content = {}
        for i in range(len(self.HEADING)):
            content[start_column+i] = rowset[i]
        return content