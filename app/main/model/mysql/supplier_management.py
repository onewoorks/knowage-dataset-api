from .. import mysql_insert_query

class SupplierManagementModel:

    def CreateNewRazorPayTransaction(self,payloads):
        query = "INSERT INTO razorpay_transaction (date,billing_name, amount, payment_type) VALUE ("
        query += "'{}', ".format(payloads['date'])
        query += "'{}', ".format(payloads['billing_name'])
        query += "{}, ".format(payloads['amount'])
        query += "'{}'".format(payloads['payment_type'])
        query += ")"
        mysql_insert_query(query)