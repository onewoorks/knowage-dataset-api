from . import execute_query

class EpContract:
    def get_all_contract(self):
        query = "SELECT * FROM ep_contract LIMIT 10"
        resp = execute_query(query)
        for i in resp:
            i['ct_eff_date'] = i['ct_eff_date'].strftime("%Y-%m-%d")
            i['ct_exp_date'] = i['ct_exp_date'].strftime("%Y-%m-%d")
            i['ct_contract_amount'] = str(i['ct_contract_amount'])
        return resp

    def get_contract_information(self, contract_id):
        query = "SELECT * FROM ep_contract  WHERE ct_contract_id = {} LIMIT 20".format(contract_id)
        resp = execute_query(query)
        for i in resp:
            i['ct_eff_date'] = i['ct_eff_date'].strftime("%Y-%m-%d")
            i['ct_exp_date'] = i['ct_exp_date'].strftime("%Y-%m-%d")
            i['ct_contract_amount'] = str(i['ct_contract_amount'])
        return resp
