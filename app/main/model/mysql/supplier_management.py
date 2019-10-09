from .. import mysql_insert_query, execute_query

class SupplierManagementModel:

    def CreateRazorFileUpload(self, payloads):
        query = "INSERT INTO razorpay_upload_history (filename,summary, user_profile) VALUE ("
        query += "'{}', ".format(payloads['filename'])
        query += "'{}', ".format(payloads['summary'])
        query += "'{}'".format(payloads['user_profile'])
        query += ")"
        mysql_insert_query(query)

    def CreateNewRazorPayTransaction(self,payloads):
        query = "INSERT INTO razorpay_transaction (date,billing_name, amount, payment_type, status, order_id) VALUE ("
        query += "'{}', ".format(payloads['date'])
        query += "'{}', ".format(payloads['billing_name'])
        query += "{}, ".format(payloads['amount'])
        query += "'{}', ".format(payloads['payment_type'])
        query += "'{}', ".format(payloads['status'])
        query += "'{}' ".format(payloads['order_id'])
        query += ")"
        mysql_insert_query(query)

    def ReadRazerPayUploadHistory(self, rows = 30):
        query = "SELECT * FROM razorpay_upload_history ORDER BY id DESC LIMIT {}".format(rows)
        return execute_query(query)

    def ReadRazerPayTransactionDetail(self, razer_id):
        query = "SELECT * FROM razorpay_upload_history WHERE id = {}".format(int(razer_id))
        return execute_query(query)

    def ActualSupplierRevenue(self,working_days,appl_type):
        query = ""
        count = 1
        valid_day = [ x for x in working_days if "null-" not in x ]
        empty_day = [ x for x in working_days if "null-" in x ]
        for i in valid_day:
            query += "SELECT '{}' AS working_day, sum(payment_amount) AS total FROM ep_supplier_payment ".format(i)
            query += "WHERE bill_type IN ('P','R') "
            query += "AND MONTH(payment_date) = 10 AND YEAR(payment_date) = '2018' "
            if '-' in i:
                day = i.split('-')
                query += "AND DAY(payment_date) >= {} ".format(day[0])
                query += "AND DAY(payment_date) <= {} ".format(day[1])
            else:
                query += "AND DAY(payment_date) = {} ".format(i)
            if appl_type == 'N':
                query += "AND doc_type IN ('KN','JN') " ## NEW
            if appl_type == 'R':
                query += "AND doc_type IN ('KR','JR') " ## RENEW
            if count < len(valid_day):
                query += "UNION ALL "
                count += 1 
        resp = execute_query(query)
        final = []
        for result in resp:
            content = {
                "working date"  : result['working_day'],
                "total"         : float(result['total'])
            }
            final.append(content)
        for e in empty_day:
            content = {
                "working date"  : e,
                "total"         : float(0)
            }
            final.append(content)
        return final