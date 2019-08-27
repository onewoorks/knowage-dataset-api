from .. import execute_oracle_query

from datetime import datetime

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
            columns = ("APPLICATION_TYPE","AMOUNT")
            return self.response(columns,resp)
        
        def actual_mof_registration(self, current_year = 'now', current_month = 'now'):
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
            query += "AND to_char(a.eff_date, 'YYYY-MM') = '{}-{}' ".format(year,str(month).zfill(2))
            query += "AND a.is_bumi_cert = 0 "
            query += "AND d.PAYMENT_AMT = '400' "
            query += "AND d.RECEIPT_NO IS NOT NULL "
            query += "GROUP BY b.appl_type, to_char(a.eff_date, 'YYYY-MM') "
            query += "ORDER BY 1 "
            resp = execute_oracle_query(query)
            columns = ("YEAR_AND_MONTH","APPLICATION_TYPE", "AMOUNT")
            return self.response(columns, resp)