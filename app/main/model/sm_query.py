from . import execute_query, execute_oracle_query, insert_ws_data

from datetime import date, datetime

class SM_Query:
    def valid_date_group(self,array_data):
        valid_date = []
        for i in array_data:
            if "null-" not in i:
                valid_date.append(i)
        return valid_date

    def get_pv_status(self):
        query   = "SELECT kementerian_name " 
        query   += "FROM ep_org_profile_ptj "
        query   += "WHERE kementerian_name != 'DUMMY' "
        query   += "GROUP BY kementerian_name"
        resp    = execute_query(query)
        return resp
    
    def get_today_ws_name(self, ws_name, today):
        query = "SELECT ws_data FROM ws_data WHERE ws_name = '{}' ".format(ws_name)
        query += " AND DATE(ws_created_at) ='{}' AND ws_is_active = 1 ".format(today)
        resp = execute_query(query)
        return resp
    
    def union_supplier_revenue(self, working_day, target):
        month = datetime.now().month
        print("perform target supplier revenue (mysql) => {}".format(target))
        query = ""
        count = 0
        self.valid_date_group(working_day)
        for i in self.valid_date_group(working_day):
            if count > 0:
                query   += "UNION ALL "
            if i != "TOTAL":
                if '-' in i:
                    day = i.split('-')
                    query   += "(SELECT '{}' AS 'date', amount AS total FROM ep_ref_target_daily WHERE YEAR = YEAR(now()) AND MONTH='{}' AND DAY BETWEEN '{}' AND '{}' AND code_name IN ('{}') AND module = 'SM' GROUP BY group_day) ".format(i,month,day[0],day[1],target)
                else:
                    query   += "(SELECT '{}' AS 'date', amount AS total FROM ep_ref_target_daily WHERE YEAR = YEAR(now()) AND MONTH='{}' AND DAY = '{}' AND code_name IN ('{}') AND module = 'SM' GROUP BY group_day) ".format(i,month,i,target)    
                count += 1
        resp    = execute_query(query)
        return resp

    def mysql_module_target(self, module, current_year = 'now', current_month = 'now'):
        year = datetime.now().year if current_year == 'now' else current_year
        month = datetime.now().month if current_year == 'now' else current_month
        query = "SELECT code_name, amount FROM ep_ref_target "
        query += "WHERE `group`='{}' ".format(module.upper())
        query += "AND year='{}'".format(year)
        query += "AND month='{}'".format(month)
        resp = execute_query(query)
        return resp

    def mysql_module_ytd_target(self, module, current_year = 'now', current_month = "now", current_day = "now"):
        year = datetime.now().year if current_year == 'now' else current_year
        month = datetime.now().month if current_month == 'now' else current_month
        day = datetime.now().month if current_day == 'now' else current_day
        query = "SELECT code_name, sum(amount) as ytd_target "
        query += "FROM ep_ref_target_daily "
        query += "WHERE `group`='{}' ".format(module)
        query += "AND year = '{}' ".format(year)
        query += "AND month <= '{}' ".format(month) 
        query += "AND DAY <= '{}' ".format(day)
        query += "GROUP BY code_name"
        resp = execute_query(query)
        return resp
        