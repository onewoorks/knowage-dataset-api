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
    
    def DeleteRazerTransaction(self, date):
        query = "DELETE FROM razorpay_transaction "
        query += "WHERE DATE(date) = '{}' ".format(date)
        execute_query(query)

    def ReadRazerPayUploadHistory(self, rows = 30):
        query = "SELECT * FROM razorpay_upload_history ORDER BY id DESC LIMIT {}".format(rows)
        return execute_query(query)

    def ReadRazerPayTransactionDetail(self, razer_id):
        query = "SELECT * FROM razorpay_upload_history WHERE id = {}".format(int(razer_id))
        return execute_query(query)

    def ReadRazerPayTransactionDate(self, date):
        query = "SELECT " 
        query += "DATE(date) as date, STATUS, COUNT(id) as quantity, "
        query += "SUM(IF(payment_type=\"RENEWAL\",amount,0)) AS 'renewal', "
        query += "SUM(IF(payment_type=\"REGISTRATION\",amount,0)) AS 'registration', "
        query += "SUM(amount) AS total_collection "
        query += "FROM razorpay_transaction WHERE DATE(date) = '{}' ".format(date)
        query += "GROUP BY status; "
        return execute_query(query)
    
    def CreateBulkTransaction(self, csv_file):
        query = "LOAD DATA LOCAL INFILE '{}' ".format(csv_file)
        query += "INTO TABLE razorpay_transaction "
        query += "FIELDS TERMINATED BY ',' ENCLOSED BY '\"' "
        query += "LINES TERMINATED BY '\r\n' IGNORE 1 LINES "
        query += "(`DATE`,`billing_name`,`amount`, `payment_type`, `STATUS`, `order_id`, `payment_mode`, `app_code`) " 
        return mysql_insert_query(query)
    
    def ReadTransactionSummaryByMonth(self, month = None, year = None):
        query = "SELECT "
        query += "DATE_FORMAT(DATE,'%d') AS day, "
        query += "SUM(IF(STATUS = 'captured',amount,0)) AS captured_amount, "
        query += "SUM(IF(STATUS = 'captured',1,0)) AS captured_count, "
        query += "SUM(IF(STATUS = 'failed',amount,0)) AS failed_amount, "
        query += "SUM(IF(STATUS = 'failed',1,0)) AS failed_count, "
        query += "SUM(IF(STATUS = 'blocked',amount,0)) AS blocked_amount, "
        query += "SUM(IF(STATUS = 'blocked',1,0)) AS blocked_count "
        query += "FROM razorpay_transaction WHERE MONTH(DATE) = '{}' AND YEAR(DATE) = '{}' ".format(month if month is not None else "MONTH(now)", year if year is not None else "YEAR(now)")
        query += "GROUP BY DAY(DATE)"
        return execute_query(query)
    
    def ReadTransactionSummaryMonthPaymentMode(self, month = None, year = None, status = 'captured'):
        query = "SELECT "
        query += "DAY(DATE) AS day, "
        query += "SUM(amount) AS total_captured, "
        query += "SUM(IF(amount = 400, amount, 0)) AS registration_fee_total, "
        query += "SUM(IF(amount = 50, amount, 0)) AS processing_fee_total, "
        query += "SUM(IF(amount = 400 AND payment_mode = 'FPX', amount,0)) AS registration_fee_fpx, "
        query += "SUM(IF(amount = 400 AND payment_mode = 'CARD', amount,0)) AS registration_fee_card, "
        query += "SUM(IF(amount = 50 AND payment_mode = 'FPX', amount,0)) AS processing_fee_fpx, "
        query += "SUM(IF(amount = 50 AND payment_mode = 'CARD', amount,0)) AS processing_fee_card "
        query += "FROM razorpay_transaction "
        query += "WHERE MONTH(DATE) = '{}' AND YEAR(DATE) = '{}' ".format(month if month is not None else "MONTH(now)", year if year is not None else "YEAR(now)")
        query += "AND STATUS = '{}' ".format(status)
        query += "GROUP BY DAY(DATE) "
        return execute_query(query)

    def ReadTransactionPivotSummary(self, month = None, year = None, status = 'captured'):
        query = "SELECT * FROM razorpay_transaction "
        query += "WHERE MONTH(DATE) = '{}' AND YEAR(DATE) = '{}' ".format(month if month is not None else "MONTH(now)", year if year is not None else "YEAR(now) ")
        query += "AND status = '{}' ".format(status)
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