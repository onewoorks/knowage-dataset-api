import os
import pandas as pd 
from ...model.mysql.supplier_management import SupplierManagementModel

class RazorPayServices:

    def ProcessUploadFile(self, filename):
        data_files = os.getcwd()+'/upload_media/' + filename

        raw_data = pd.ExcelFile(data_files)
        raw_data.sheet_names

        raw = raw_data.parse('Sheet1')

        raw['Date'][0]

        df = pd.DataFrame(raw)
        molpay_data = {
            "date": raw['Date'][0].split(' ')[0]
        }

        for stat in df.groupby('Status').count().index :
            total = df[(df['Status'] == stat)].sum()['Bill Amt']
            count = df[(df['Status'] == stat)].count()['Bill Amt']
            register = df[(df['Status'] == stat) & (df['Bill Amt'] == 400 )].sum()['Bill Amt']
            renew = df[(df['Status'] == stat) & (df['Bill Amt'] == 50 )].sum()['Bill Amt']
            molpay_data[stat+"_count"] = count
            molpay_data[stat+"_total"] = total
            molpay_data[stat+"_register"] = register
            molpay_data[stat+"_renew"] = renew 

        for r in raw.to_dict('records'):
            payloads = {
                "date"          : r['Date'],
                "billing_name"  : r['Billing Name'],
                "amount"        : r['Bill Amt'],
                "payment_type"  : "REGISTRATION" if r['Bill Amt'] == 400 else "RENEWAL",
                "status"        : r['Status'].upper()
            } 
            SupplierManagementModel().CreateNewRazorPayTransaction(payloads)
        return molpay_data