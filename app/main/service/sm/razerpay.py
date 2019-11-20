import os, json, csv
from datetime import datetime, date
from calendar import monthrange
import pandas as pd 
from flask import current_app as app

from ...model.mysql import Common_Query
from ...model.mysql.supplier_management import SupplierManagementModel

class RazerPaySetter:
    WS_NAME = {
        "RAZERPAY_TRANSACTION" : "RAZERPAY_TRANSACTION"
    }
    GROUP = "SM"

class RazerPayServices(RazerPaySetter):

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
                "payment_type"  : "REGISTRATION" if r['Bill Amt'] == 400 else "PROCESSING",
                "status"        : r['Status'],
                "order_id"      : r['Order ID'],
                "payment_mode"  : "FPX" if type(r['App Code']) is float else "CARD",
                "app_code"      : "" if type(r['App Code']) is float else r['App Code']
            } 
            to_csv.append(payloads)
        self.__RegisterNewUpload(filename, user_profile, json.dumps(response))
        self.__WriteCSVUploadDelete('razer_transaction', to_csv)
        os.remove(filename)
        self.create_razerpay_dataset()
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

    def read_month_transaction_summary(self, month = None, year = None):
        data = SupplierManagementModel().ReadTransactionSummaryMonthPaymentMode(datetime.now().month,datetime.now().year, status='captured')
        response = []
        header = {
            "100"   : "Day",
            "101"   : "Total Captured",
            "102"   : "Registration Fee Total",
            "103"   : "Registration Fee (FPX)",
            "104"   : "Registration Fee (CARD)",
            "105"   : "Processing Fee Total",
            "106"   : "Processing Fee (FPX)",
            "107"   : "Processing Fee (CARD)"
        }
        response.append(header)
        for d in data:
            content = {
                "100"   : str(d['day']),
                "101"   : "{0:,.2f}".format(float(d['total_captured'])),
                "102"   : "{0:,.2f}".format(float(d['registration_fee_total'])),
                "103"   : "{0:,.2f}".format(float(d['registration_fee_fpx'])),
                "104"   : "{0:,.2f}".format(float(d['registration_fee_card'])),
                "105"   : "{0:,.2f}".format(float(d['processing_fee_total'])),
                "106"   : "{0:,.2f}".format(float(d['processing_fee_fpx'])),
                "107"   : "{0:,.2f}".format(float(d['processing_fee_card']))
            }
            response.append(content)
        return response
    
    def month_transaction_to_pivot_summary(self):
        razer_transactions  = SupplierManagementModel().ReadTransactionPivotSummary(datetime.now().month,datetime.now().year, status='captured')
        df                  = pd.DataFrame(razer_transactions).drop(['billing_name','order_id', 'id','app_code'], axis=1)
        response = { 
            "summary": self.__RazerTransactionPivotSummary(df),
            "pivot" : self.__RazerTransactionGraphPivot(df)
        }
        return response

    def __RazerTransactionPivotSummary(self, payloads):
        df_summary  = payloads.groupby(['payment_type','payment_mode']).sum().drop(['status'],axis=1)
        summary = {
            "processing_fpx"        : float(df_summary.loc['PROCESSING'].loc['FPX']),
            "processing_card"       : float(df_summary.loc['PROCESSING'].loc['CARD']),
            "registration_fpx"      : float(df_summary.loc['REGISTRATION'].loc['FPX']),
            "registration_card"     : float(df_summary.loc['REGISTRATION'].loc['CARD']),
            "processing_amount"     : float(df_summary.loc['PROCESSING'].loc['FPX']+df_summary.loc['PROCESSING'].loc['CARD']),
            "registration_amount"   : float(df_summary.loc['REGISTRATION'].loc['FPX']+df_summary.loc['REGISTRATION'].loc['CARD']),
            "fpx_amount"            : float(df_summary.loc['PROCESSING'].loc['FPX']+df_summary.loc['REGISTRATION'].loc['FPX']),
            "card_amount"           : float(df_summary.loc['PROCESSING'].loc['CARD']+df_summary.loc['REGISTRATION'].loc['CARD']),
            "big_amount"            : float(payloads.sum().loc['amount'])
        }
        return summary

    def __RazerTransactionGraphPivot(self, payloads):
        max_day     = payloads['date'].dt.day.max()
        daily_df    = payloads.groupby([pd.to_datetime(payloads['date']),'payment_type','payment_mode']).sum().drop('status',axis=1)
        year_month  = str(payloads['date'].dt.year.max()) + '-' + str(payloads['date'].dt.month.max()) + '-'
        pivot_data  = []
        total_days = monthrange(payloads['date'].dt.year.max(),payloads['date'].dt.month.max())[1]
        for d in range(total_days):
            day = year_month + str(d+1).zfill(2)
            daily = {
                "id"                    : int(d+1),
                "day"                   : str(d+1), 
                "processing_fpx"        : float(daily_df.loc(axis=0)[day,'PROCESSING','FPX'].sum()),
                "processing_card"       : float(daily_df.loc(axis=0)[day,'PROCESSING','CARD'].sum()),
                "registration_fpx"      : float(daily_df.loc(axis=0)[day,'REGISTRATION','FPX'].sum()),
                "registration_card"     : float(daily_df.loc(axis=0)[day,'REGISTRATION','CARD'].sum()),
                "processing_amount"     : float(daily_df.loc(axis=0)[day,'PROCESSING','FPX'].sum()) + float(daily_df.loc(axis=0)[day,'PROCESSING','CARD'].sum()),
                "registration_amount"   : float(daily_df.loc(axis=0)[day,'REGISTRATION','FPX'].sum()) + float(daily_df.loc(axis=0)[day,'REGISTRATION','CARD'].sum()),
                "fpx_amount"            : float(daily_df.loc(axis=0)[day,'PROCESSING','FPX'].sum()) + float(daily_df.loc(axis=0)[day,'REGISTRATION','FPX'].sum()),
                "card_amount"           : float(daily_df.loc(axis=0)[day,'PROCESSING','CARD'].sum()) + float(daily_df.loc(axis=0)[day,'REGISTRATION','CARD'].sum())
            }
            pivot_data.append(daily)
        return pivot_data

    def create_razerpay_dataset(self):
        start_time  = datetime.now()
        ws_name     = "RAZERPAY_TRANSACTION"
        print('-- {} --'.format(ws_name))
        print('-- start query----')
        dataset = {
            "datatable" : self.read_month_transaction_summary(),
            "cockpit"   : self.month_transaction_to_pivot_summary() 
        }
        print('-- end query-----')
        end_time    = datetime.now()
        input = {
            "ws_name"           : "{}".format(ws_name.replace(' ','_')),
            "ws_is_active"      : "1",
            "ws_desc"           : "{} as at {}".format(ws_name, date.today().strftime("%d %B %Y")),
            "ws_group"          : self.GROUP,
            "ws_start_execute"  : start_time,
            "ws_end_execute"    : end_time,
            "ws_duration"       : int((end_time-start_time).total_seconds()),
            "ws_data"           : json.dumps(dataset),
            "ws_created_at"     : datetime.now(),
            "ws_updated_at"     : datetime.now(),
            "ws_status"         : "SUCCESS",
            "ws_error"          : ""
        }
        Common_Query().Register_New_Ws(input)
        return dataset

    def load_ws_data(self, ws_name):
        response = Common_Query().get_latest_ws_data(ws_name)[0]['ws_data']
        return json.loads(response)