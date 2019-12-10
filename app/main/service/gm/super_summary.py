from ...model.mysql.government_management import MYSQL_GM_QUERY

class SupperSummaryService:

    def forecast_contract_utilization(self, ministry_name):
        response = MYSQL_GM_QUERY().forecast_contract_utilization(ministry_name)
        output = []
        for r in response:
            r['ct_contract_amount'] = float(r['ct_contract_amount'])
            r['utilization']        = float(r['utilization'])
            r['amount_available']   = float(r['amount_available'])
            r['forecast_thisyear']  = float(r['forecast_thisyear'])
            r['forecast_nextyear']  = float(r['forecast_nextyear'])
            r['forecast_next2years']    = float(r['forecast_next2years'])
            r['forecast_next3years']    = float(r['forecast_next3years'])
            r['forecast_next4years']    = float(r['forecast_next4years'])
            r['forecast_next5years']    = float(r['forecast_next5years'])
            output.append(r)
        return self.__forecast_contract_utilization_pivot(output)

    def __forecast_contract_utilization_pivot(self, dataset):
        pivotal = []
        for r in range(6):
            if r == 0:
                key = 'forecast_thisyear'
            if r == 1:
                key = 'forecast_nextyear'
            if r > 1:
                key = 'forecast_next'+str(r)+'years'
            data = {
                "index": r + 1,
                "ct_ministry_name_created": dataset[0]['ct_ministry_name_created'],
                "category_name":  key,
                "value": dataset[0][key]
            }
            pivotal.append(data)
        return pivotal