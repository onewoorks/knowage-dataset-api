import os, json
import pandas as pd 
from flask import current_app as app

from ...model.mysql.supplier_management import SupplierManagementModel

class RazerPayServices:

    def UploadHistory(self):
        data = SupplierManagementModel().ReadRazerPayUploadHistory()
        final_data = []
        for d in data:
            d['timestamp'] = str(d['timestamp'])
            d['summary'] = json.loads(d['summary'])
            final_data.append(d)
        return final_data

    def ReadTransactionDetail(self, razer_id):
        data = SupplierManagementModel().ReadRazerPayTransactionDetail(razer_id)
        final_data = data[0]
        final_data['timestamp'] = str(final_data['timestamp'])
        final_data['summary'] = json.loads(final_data['summary'])
        final_data['user_profile'] = json.loads(final_data['user_profile'])
        return final_data
        

    def __RegisterNewUpload(self, filename, user_profile = None, summary = None):
        upload_path = os.getcwd() + app.config['UPLOAD_MEDIA']
        payloads = {
            "filename": filename.split(upload_path)[-1],
            "user_profile": user_profile,
            "summary": summary
        }
        SupplierManagementModel().CreateRazorFileUpload(payloads)

    def ProcessUploadFile(self, filename, user_profile = None):
        raw_data = pd.ExcelFile(filename)
        raw_data.sheet_names
 
        raw = raw_data.parse('Sheet1')

        raw['Date'][0]

        df = pd.DataFrame(raw)
        molpay_data = {
            "date": raw['Date'][0].split(' ')[0]
        }
        for stat in df.groupby('Status').count().index :
            total       = df[(df['Status'] == stat)].sum()['Bill Amt']
            count       = df[(df['Status'] == stat)].count()['Bill Amt']
            register    = df[(df['Status'] == stat) & (df['Bill Amt'] == 400 )].sum()['Bill Amt']
            renew       = df[(df['Status'] == stat) & (df['Bill Amt'] == 50 )].sum()['Bill Amt']
            molpay_data[stat+"_count"] = str(count)
            molpay_data[stat+"_total"] = str(total)
            molpay_data[stat+"_register"] = str(register)
            molpay_data[stat+"_renew"] = str(renew)

        for r in raw.to_dict('records'):
            payloads = {
                "date"          : r['Date'],
                "billing_name"  : r['Billing Name'],
                "amount"        : r['Bill Amt'],
                "payment_type"  : "REGISTRATION" if r['Bill Amt'] == 400 else "RENEWAL",
                "status"        : r['Status'],
                "order_id"      : r['Order ID']
            } 
            SupplierManagementModel().CreateNewRazorPayTransaction(payloads)
        self.__RegisterNewUpload(filename, user_profile, json.dumps(molpay_data))
        os.remove(filename)
        return molpay_data