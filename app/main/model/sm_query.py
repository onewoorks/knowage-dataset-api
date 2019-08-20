from . import execute_query

class SM_Query:
    def get_pv_status(self):
        query   = "SELECT kementerian_name " 
        query   += "FROM ep_org_profile_ptj "
        query   += "WHERE kementerian_name != 'DUMMY' "
        query   += "GROUP BY kementerian_name"
        resp    = execute_query(query)
        return resp
    
    def union_supplier_revenue(self, working_day, target):
        query = ""
        count = 0
        for i in working_day[:-1]:
            if count > 0:
                query   += "UNION ALL "
            if i != "TOTAL":
                if '-' in i:
                    day = i.split('-')
                    query   += "(SELECT '{}' AS 'date', amount AS total FROM ep_ref_target_daily WHERE YEAR = YEAR(now()) AND MONTH='7' AND DAY BETWEEN '{}' AND '{}' AND code_name IN ('{}') AND module = 'SM' GROUP BY group_day) ".format(i,day[0],day[1],target)
                else:
                    query   += "(SELECT '{}' AS 'date', amount AS total FROM ep_ref_target_daily WHERE YEAR = YEAR(now()) AND MONTH='7' AND DAY = '{}' AND code_name IN ('{}') AND module = 'SM' GROUP BY group_day) ".format(i,i,target)    
                count += 1
        resp    = execute_query(query)
        return resp