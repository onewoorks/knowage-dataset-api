from .. import execute_oracle_query

from datetime import datetime, date 


class RETURN_RESPONSE:
    def response(self, columns, result):
        final = []
        for r in result:
            data = {}
            index = 0
            for c in columns:
                data[c] = r[index]
                index += 1
            final.append(data)
        return final


class ORACLE_SM_QUERY(RETURN_RESPONSE):
        def ytd_mof_registration(self):
            year = datetime.now().year
            query = "SELECT "
            query += "b.appl_type as \"application_type\", "
            query += "sum(d.PAYMENT_AMT) as \"total_amount\" "
            query += "FROM SM_MOF_CERT a, sm_appl b, py_bill c, PY_PAYMENT d "
            query += "WHERE "
            query += "a.appl_id =  b.appl_id "
            query += "AND c.org_profile_id = b.supplier_id "
            query += "AND b.appl_no = c.bill_no "
            query += "AND c.BILL_ID = d.BILL_ID "
            query += "AND to_char(a.eff_date, 'YYYY') = '{}' ".format(year)
            query += "AND a.is_bumi_cert = 0 "
            query += "AND d.PAYMENT_AMT = '400' "
            query += "AND d.RECEIPT_NO IS NOT NULL "
            query += "GROUP BY b.appl_type "
            query += "ORDER BY 1 "
            resp = execute_oracle_query(query)
            columns = ("APPLICATION_TYPE", "AMOUNT")
            return self.response(columns, resp)

        def actual_mof_registration(self, current_year='now', current_month='now'):
            year = datetime.now().year if current_year == 'now' else current_year
            month = datetime.now().month if current_year == 'now' else current_month
            query = "SELECT "
            query += "to_char(a.eff_date,'YYYY-MM') as \"year_and_month\", "
            query += "b.appl_type as \"application_type\", "
            query += "sum(d.PAYMENT_AMT) as \"total_amount\" "
            query += "FROM SM_MOF_CERT a, sm_appl b, py_bill c, PY_PAYMENT d "
            query += "WHERE "
            query += "a.appl_id =  b.appl_id "
            query += "AND c.org_profile_id = b.supplier_id "
            query += "AND b.appl_no = c.bill_no "
            query += "AND c.BILL_ID = d.BILL_ID "
            query += "AND to_char(a.eff_date, 'YYYY-MM') = '{}-{}' ".format(
                year, str(month).zfill(2))
            query += "AND a.is_bumi_cert = 0 "
            query += "AND d.PAYMENT_AMT = '400' "
            query += "AND d.RECEIPT_NO IS NOT NULL "
            query += "GROUP BY b.appl_type, to_char(a.eff_date, 'YYYY-MM') "
            query += "ORDER BY 1 "
            resp = execute_oracle_query(query)
            columns = ("YEAR_AND_MONTH", "APPLICATION_TYPE", "AMOUNT")
            return self.response(columns, resp)

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
