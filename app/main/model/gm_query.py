from . import execute_query

from datetime import datetime

class GM_Query:
    def ReadMinistryActive(self):
        query   = "SELECT org_profile_id, org_name as kementerian_name, "
        query   += "org_code " 
        query   += "FROM ep_org_profile "
        query   += "WHERE org_type_id = 2 "
        query   += "AND record_status = 1 "
        query   += "ORDER BY org_code"
        resp    = execute_query(query)
        return resp

    def get_ministry_location_count(self):
        query   = "SELECT "
        query   += "ptj_state_name AS state, "
        query   += "COUNT(ptj_profile_id) AS no_of_ptj "
        query   += "FROM ep_org_profile_ptj "
        query   += "WHERE ptj_state_name != 'N/A' "
        query   += "GROUP BY ptj_state_code " 
        resp    = execute_query(query)
        return resp

    def get_ministry_no_of_ptj(self):
        query   = "SELECT "
        query   += "kementerian_name, "
        query   += "COUNT(ptj_profile_id) AS total "
        query   += "FROM "
        query   += "ep_org_profile_ptj "
        query   += "WHERE kementerian_name != 'DUMMY' "
        query   += "GROUP BY kementerian_name "
        query   += "ORDER BY total DESC"
        resp    = execute_query(query)
        return resp

    def get_working_days(self):
        query   = "SELECT DAY(DATE) as day, "
        query   += "category "
        query   += "FROM ep_yearly_calendar "
        query   += "WHERE YEAR(DATE) = YEAR(NOW()) AND MONTH(DATE) = MONTH(NOW())"
        resp    = execute_query(query)
        return resp