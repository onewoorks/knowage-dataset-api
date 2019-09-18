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

    def pending_payment_cycle_monthly_actual_pv(self):
        query = "SELECT DATE_FORMAT(fl_created_date,'%M') AS date_pv, "
        query += "SUM(fl_total_amount) AS total_pv "
        query += "FROM ep_fulfilment  "
        query += "WHERE fl_financial_year = '2019' "
        query += "AND fl_module IN ('Contract Order','Purchase Order') "
        query += "GROUP BY DATE_FORMAT(fl_created_date,'%m-%Y') "
        resp = execute_query(query)
        return resp

    def pending_payment_cycle_monthly_po_cancel(self):
        query = "SELECT DATE_FORMAT(fl_created_date,'%M') AS date_pv, "
        query += "SUM(fl_total_amount) AS total_pv_cancel "
        query += "FROM ep_fulfilment "
        query += "WHERE fl_financial_year = '2019' "
        query += "AND fl_module IN ('Contract Order','Purchase Order') "
        query += "AND fl_latest_status_id IN (41400,41900,47900,41440,41940,41430,40910,41410,41910,40810,41310) "
        query += "GROUP BY DATE_FORMAT(fl_created_date,'%m-%Y') "
        resp = execute_query(query)
        return resp

    def pending_payment_cycle_monthly_payment(self, current_month):
        query = "SELECT DATE_FORMAT(fl_trans_revenue_date,'%c') AS date_index, "
        query += "SUM(fl_total_amount) AS total_pv "
        query += "FROM ep_fulfilment "
        query += "WHERE fl_financial_year = '2019' "
        query += "AND fl_module IN ('Contract Order','Purchase Order') "
        query += "AND fl_latest_status_id IN (41030,41035,41535,41530,41030) "
        query += "AND  DATE_FORMAT(fl_ag_approved_date,'%m-%Y') = '{}-2019' ".format(str(current_month).zfill(2))
        query += "GROUP BY DATE_FORMAT(fl_trans_revenue_date,'%M') "
        query += "HAVING date_index IS NOT NULL "
        query += "ORDER BY 1"
        resp = execute_query(query)
        return resp