import os, json, csv
from datetime import datetime
from calendar import monthrange
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
            "user_profile": json.dumps(user_profile),
            "summary": summary
        }
        SupplierManagementModel().CreateRazorFileUpload(payloads)
    
    def __CheckTransactionDate(self, date):
        existed = SupplierManagementModel().ReadRazerPayTransactionDate(date)
        return existed if len(existed) > 0 else False

    def __ExistedData(self, payloads):
        result = {
            "date"  : str(payloads[0]['date'])
        }
        for data in payloads:
            result[data['STATUS'] + '_register']    = float(data['registration'])
            result[data['STATUS'] + '_renew']       = float(data['renewal'])
            result[data['STATUS'] + '_count']       = int(data['quantity'])
            result[data['STATUS'] + '_total']       = float(data['total_collection'])
        return result

    def RazerTransactionOverwrite(self, filename, user_profile):
        file_path = os.getcwd() + app.config['UPLOAD_MEDIA'] + filename
        raw_data = pd.ExcelFile(file_path)
        raw_data.sheet_names
        raw = raw_data.parse('Sheet1')
        SupplierManagementModel().DeleteRazerTransaction(raw['Date'][0].split(' ')[0])
        response = self.__TransactionInfo(raw=raw,filename= file_path, user_profile= user_profile )
        return response

    def __TransactionInfo(self, raw, filename, user_profile):
        raw['Date'][0]
        df = pd.DataFrame(raw)
        response = {}
        response['date'] = raw['Date'][0].split(' ')[0]
        for stat in df.groupby('Status').count().index :
            total       = df[(df['Status'] == stat)].sum()['Bill Amt']
            count       = df[(df['Status'] == stat)].count()['Bill Amt']
            register    = df[(df['Status'] == stat) & (df['Bill Amt'] == 400 )].sum()['Bill Amt']
            renew       = df[(df['Status'] == stat) & (df['Bill Amt'] == 50 )].sum()['Bill Amt']
            response[stat+"_count"]     = str(count)
            response[stat+"_total"]     = str(total)
            response[stat+"_register"]  = str(register)
            response[stat+"_renew"]     = str(renew)
            response['status']          = 800
        
        to_csv = []
        for r in raw.to_dict('records'):
            payloads = {
                "date"          : r['Date'],
                "billing_name"  : r['Billing Name'],
                "amount"        : r['Bill Amt'],
                "payment_type"  : "REGISTRATION" if r['Bill Amt'] == 400 else "RENEWAL",
                "status"        : r['Status'],
                "order_id"      : r['Order ID']
            } 
            to_csv.append(payloads)
        self.__RegisterNewUpload(filename, user_profile, json.dumps(response))
        self.__WriteCSVUploadDelete('razer_transaction', to_csv)
        os.remove(filename)
        return response

    def ProcessUploadFile(self, filename, user_profile = None):
        raw_data = pd.ExcelFile(filename)
        raw_data.sheet_names
        raw = raw_data.parse('Sheet1')
        existed = self.__CheckTransactionDate(raw['Date'][0].split(' ')[0])
        response = {}
        if not existed:
            response = self.__TransactionInfo(raw = raw, filename= filename, user_profile=json.loads(user_profile))
        else:
            upload_path = os.getcwd() + app.config['UPLOAD_MEDIA']
            response["status"]          = 809
            response['message']         = "Transaction date already existed"
            response['existed_data']    = self.__ExistedData(existed)
            response['filename']        = filename.split(upload_path)[-1]
            response['user_profile']    = json.loads(user_profile)
        
        return response
    
    def __WriteCSVUploadDelete(self, to_filename, payloads):
        file_path =  os.getcwd() + app.config['TMP_FOLDER'] + to_filename + ".csv"
        headers = payloads[0].keys()
        with open(file_path, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, headers,quoting=csv.QUOTE_ALL)
            dict_writer.writeheader()
            dict_writer.writerows(payloads)
        SupplierManagementModel().CreateBulkTransaction(file_path)

    def ReadMonthTransactionSummary(self, month = None, year = None):
        data = SupplierManagementModel().ReadTransactionSummaryByMonth(datetime.now().month,datetime.now().year)
        response = []
        for d in data:
            content = {
                "1 id"                : str(int(d['day'])-1),
                "2 day"               : str(d['day']),
                "3 captured_amount"   : float(d['captured_amount']),
                "4 captured_count"    : int(d['captured_count']),
                "5 failed_amount"     : float(d['failed_amount']),
                "6 failed_count"      : int(d['failed_count']),
                "7 blocked_amount"    : float(d['blocked_amount']),
                "8 blocked_count"     : int(d['blocked_count'])
            }
            response.append(content)

        # for day in range(monthrange(datetime.now().year, datetime.now().month)[1]):
        #     if any(d['id'] == str(day) for d in response):
        #         print(day)
        return response