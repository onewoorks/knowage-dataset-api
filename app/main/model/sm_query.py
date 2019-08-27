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
        
    def ora_actual_supplier_revenue(self,working_days,appl_type):
        this_month = date.today().strftime("%Y-%m")
        print("perform actual supplier revenue (oracle) => {}".format(appl_type))
        query = ""
        count = 1
        for i in working_days:
            query += "SELECT '{}' AS working_date , SUM(x.PAYMENT_AMT) AS total   FROM ( ".format(i)
            query += "SELECT DISTINCT"
            query += "  a.mof_account_id," 
            query += "  b.appl_no," 
            query += "  b.appl_type,"
            query += "  a.eff_date,"
            query += "  a.exp_date,"
            query += "  d.PAYMENT_DATE,"
            query += "  d.PAYMENT_AMT "
            query += "FROM SM_MOF_CERT a, sm_appl b, py_bill c, PY_PAYMENT d "
            query += "WHERE"
            query += "  a.appl_id =  b.appl_id"
            query += "  AND c.org_profile_id = b.supplier_id"
            query += "  AND b.appl_no = c.bill_no"
            query += "  AND c.BILL_ID = d.BILL_ID"
            if '-' in i:
                day = i.split('-')
                day_start = day[0].zfill(2)
                day_end = day[1].zfill(2)
                query += "  AND to_char(a.eff_date, 'YYYY-MM-DD') >= '{}-{}'".format(this_month,day_start)
                query += "  AND to_char(a.eff_date, 'YYYY-MM-DD') <= '{}-{}'".format(this_month,day_end)
            else:
                query += "  AND to_char(a.eff_date, 'YYYY-MM-DD') = '{}-{}'".format(this_month,i.zfill(2))
            query += "  AND a.is_bumi_cert = 0"
            query += "  AND b.appl_type IN ('{}')".format(appl_type)
            query += "  AND d.PAYMENT_AMT = '400'"
            query += "  AND d.RECEIPT_NO IS NOT NULL"
            query += "  ORDER BY 1"
            query += ") X GROUP BY 1,'{}' ".format(i)
            if count < len(working_days):
                query += "UNION ALL "
            count += 1
        resp = execute_oracle_query(query)
        final = []
        for result in resp:
            content = {
                "working date": result[0],
                "total": result[1]
            }
            final.append(content)
        return final