from .. import execute_query
from . import Common_Query

common_query = Common_Query()

class MYSQL_GM_QUERY():

    def Get_Latest_WS(self,module_name):
        return common_query.Get_Latest_WS_Data(module_name)

    def yearly_target(self):
        query = "SELECT sum(target_year) AS yearly_target "
        query += "FROM ep_ref_target_gm " 
        query += "WHERE YEAR = YEAR(now())"
        resp = execute_query(query)
        return resp
    
    def detail_year_target(self):
        query = "SELECT "
        query += "tgm.*, ptj.kementerian_name "
        query += "FROM ep_ref_target_gm tgm "
        query += "LEFT JOIN ep_org_profile_ptj ptj ON ptj.ptj_code = tgm.ptj_code "
        query += "WHERE tgm.year = year(now())"
        resp = execute_query(query)
        return resp

    def detail_year_target_ws(self):
        query = "SELECT ws_data "
        query += "FROM ws_data "
        query += "WHERE ws_name = 'GM_TARGET' AND ws_is_active = '1' LIMIT 1"
        resp = execute_query(query)
        return resp

    def monthly_target(self):
        query = "SELECT month, sum(target_year) AS target_value "
        query += "FROM ep_ref_target_gm "
        query += "WHERE YEAR = YEAR(now()) "
        query += "GROUP BY MONTH"
        resp = execute_query(query)
        return resp