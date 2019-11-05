from .. import execute_query
from . import Common_Query

from datetime import datetime

common_query = Common_Query()

class MYSQL_GM_QUERY():

    def create_new_ws(self, ws_data):
        common_query.Register_New_Ws(ws_data)

    def create_archived_ws(self, ws_data, year):
        common_query.register_archived_ws(ws_data, year)

    def get_latest_ws(self,module_name):
        return common_query.get_latest_ws_data(module_name)

    def get_archived_dataset(self, module_name, year):
        return common_query.get_archived_ws_dataset(module_name, year)

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

    def pending_payment_cycle_monthly_actual_pv(self, year = datetime.now().year):
        query = "SELECT "
        query += "DATE_FORMAT(fl_created_date,'%M') AS date_pv, "
        query += "SUM(fl_total_amount) AS total_pv "
        query += "FROM ep_fulfilment_dtl_{}  ".format(year)
        query += "WHERE fl_financial_year = '{}' ".format(year)
        query += "AND fl_module IN ('Contract Order','Purchase Order') "
        query += "AND fl_latest_status_id IS NOT NULL "
        query += "GROUP BY DATE_FORMAT(fl_created_date,'%m-%Y') "
        resp = execute_query(query)
        return resp

    def pending_payment_cycle_monthly_po_cancel(self, year = datetime.now().year):
        query = "SELECT DATE_FORMAT(fl_created_date,'%M') AS date_pv, "
        query += "SUM(fl_total_amount) AS total_pv_cancel "
        query += "FROM ep_fulfilment_dtl_{} ".format(year)
        query += "WHERE fl_financial_year = '{}' ".format(year)
        query += "AND fl_module IN ('Contract Order','Purchase Order') "
        query += "AND fl_latest_status_id IN (41400,41900,47900,41440,41940,41430,40910,41410,41910,40810,41310) "
        query += "GROUP BY DATE_FORMAT(fl_created_date,'%m-%Y') "
        resp = execute_query(query)
        return resp

    def pending_payment_cycle_monthly_payment(self, current_month, year = datetime.now().year):
        query = "SELECT DATE_FORMAT(fl_trans_revenue_date,'%c') AS date_index, "
        query += "SUM(fl_total_amount) AS total_pv "
        query += "FROM ep_fulfilment_dtl_{} ".format(year)
        query += "WHERE fl_financial_year = '{}' ".format(year)
        query += "AND fl_module IN ('Contract Order','Purchase Order') "
        query += "AND fl_latest_status_id IN (41030,41035,41535,41530,41030) "
        query += "AND  DATE_FORMAT(fl_created_date,'%m-%Y') = '{}-{}' ".format(str(current_month).zfill(2), year)
        query += "GROUP BY DATE_FORMAT(fl_trans_revenue_date,'%M') "
        query += "HAVING date_index IS NOT NULL "
        query += "ORDER BY 1"
        resp = execute_query(query)
        return resp

    def pv_status_actual_pv(self, year = datetime.now().year):
        query = "SELECT fl_created_ministry_id AS ministry_id, "
        query += "SUM(fl_total_amount) AS total "
        query += "FROM ep_fulfilment_dtl_{} ".format(year)
        query += "WHERE fl_financial_year = '{}' ".format(year)
        query += "AND fl_module IN ('Contract Order','Purchase Order') "
        query += "GROUP BY fl_created_ministry_id "
        resp = execute_query(query)
        return resp

    def pv_status_cancel(self,year = datetime.now().year):
        query = "SELECT "
        query += "fl.fl_created_ministry_id as ministry_id, "
        query += "SUM(fl.fl_total_amount) AS total "
        query += "FROM ep_fulfilment_dtl_{} fl ".format(year)
        query += "WHERE fl.fl_financial_year = '{}' ".format(year)
        query += "AND fl.fl_module IN ('Contract Order','Purchase Order') "
        query += "AND fl.fl_latest_status_id IN (41400,41900,47900,41440,41940,41430,40910,41410,41910,40810,41310) "
        query += "GROUP BY fl.fl_created_ministry_id "
        resp = execute_query(query)
        return resp

    def pv_status_pending_payment(self, year = datetime.now().year):
        query = "SELECT "
        query += "fl_created_ministry_id AS ministry_id, "
        query += "SUM(fl_total_amount) AS total "
        query += "FROM ep_fulfilment_dtl_{} ".format(year)
        query += "WHERE fl_financial_year = '{}' ".format(year)
        query += "AND fl_module IN ('Contract Order','Purchase Order') "
        query += "AND fl_latest_status_id IN (41030,41035,41535,41530,41030) "
        query += "GROUP BY fl_created_ministry_id"
        resp = execute_query(query)
        return resp

    def ReadMinistryActive(self):
        query   = "SELECT org_profile_id, org_name as kementerian_name, "
        query   += "org_code " 
        query   += "FROM ep_org_profile "
        query   += "WHERE org_type_id = 2 "
        query   += "AND record_status = 1 "
        query   += "ORDER BY org_code"
        resp    = execute_query(query)
        return resp

    def top_ptj(self, top_data = None):
        query = "SELECT " 
        query += "group_top_ptj, "
        query += "ptj_code AS ptj_code, "
        query += "target_year AS target "
        query += "FROM ep_ref_target_gm "
        query += "WHERE "
        query += "YEAR = '2019' "
        query += "AND (group_top_ptj = 'TOP 01-50' OR group_top_ptj = 'TOP 51-100') "
        query += "GROUP BY ptj_code"
        resp = execute_query(query)
        return resp

    def Read_All_PTJ_Ministry(self):
        query = "SELECT "
        query += "ptj_code, ptj_name, kementerian_name "
        query += "FROM ep_org_profile_ptj"
        resp = execute_query(query)
        return resp

    def Read_PTJ_Profile(self):
        query = "SELECT "
        query += "org_profile_id, org_code, org_name, state_name "
        query += "FROM "
        query += "ep_org_profile "
        query += "WHERE org_type_id = 5 "\
            "AND state_name != 'N/A'"
        return execute_query(query)

    def ReadPVTargetAsNow(self, year = datetime.now().year, month=datetime.now().month):
        query = " SELECT "
        query += "group_top_ptj, "
        query += "ptj_code AS ptj_code, "
        query += "SUM(target_month) AS target "
        query += "FROM ep_ref_target_gm "
        query += "WHERE "
        query += "YEAR = '{}' ".format(year)
        query += "AND MONTH <= '{}'".format(month)
        query +=  "AND (group_top_ptj = 'TOP 01-50' OR group_top_ptj = 'TOP 51-100') "
        query += "GROUP BY ptj_code"
        return execute_query(query)

    def pv_status_actual_pv_by_ptj(self):
        query = "SELECT fl_created_ptj_id AS ptj_id, "
        query += "SUM(fl_total_amount) AS total "
        query += "FROM ep_fulfilment "
        query += "WHERE fl_financial_year = '2019' "
        query += "AND fl_module IN ('Contract Order','Purchase Order') "
        query += "GROUP BY fl_created_ptj_id "
        return execute_query(query) 

    def list_of_available_fulfilment_year(self):
        query = "SHOW TABLES LIKE 'ep_fulfilment_dtl_%'"
        return execute_query(query)