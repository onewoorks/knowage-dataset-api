from ...model.mysql import Common_Query
from ...model.mysql.training import TrainingEpolModel

import pandas as pd 
from datetime import datetime, date
import json

class EpolSetter:
    WS_NAME : {
        "EPOL_STATISTIC" : "EPOL STATISTIC"
    }
    GROUP = "SM"
    TRAINING_SUMMARY_CBT_HEADER = {
        "100" : "User Type",
        "101" : "Self-Learned (CBT)",
        "102" : "January",
        "103" : "February",
        "104" : "March",
        "105" : "April",
        "106" : "May",
        "107" : "June",
        "108" : "July",
        "109" : "August",
        "110" : "September",
        "111" : "October",
        "112" : "November",
        "113" : "December",
        "114" : "Grand Total"
        }
    TRAINING_SUMMARY_LATIHAN_HEADER = {
        "100" : "User Type",
        "101" : "Latihan Dalam Kelas",
        "102" : "January",
        "103" : "February",
        "104" : "March",
        "105" : "April",
        "106" : "May",
        "107" : "June",
        "108" : "July",
        "109" : "August",
        "110" : "September",
        "111" : "October",
        "112" : "November",
        "113" : "December",
        "114" : "Grand Total"
        }

class EpolServices(EpolSetter):

    def get_training_summary_report_latihan(self):
        return self.__training_summary_report_latihan()

    def get_training_summary_report_cbt(self):
        return self.__training_summary_report_cbt()
    
    def __pivot_monthly(self, payloads):
        clean = pd.DataFrame(payloads)
        pivot = clean[clean['101'] == 'Total'].reset_index().drop('index',axis=1)
        monthly = []
        for i in range(12):
            data_monthly = {
                "id" : i+1,
                "month" : str(i+1)
            }
            for p in range(len(pivot)):
                data_monthly[pivot.loc[p]['100'].lower()] = float(pivot.loc[p][str(102+i)])
            monthly.append(data_monthly)
        return monthly
    
    def __pivot_cumulative(self, payloads):
        clean       = pd.DataFrame(payloads)
        pivot       = clean[clean['101'] == 'Total'].reset_index().drop(['index','101','114'],axis=1)
        type_user   = [ x.lower() for x in pivot['100']]
        for c in range(len(pivot.columns.values) - 1):
            pivot[str(102+c)] = pivot[str(102+c)].str.replace(",", "").astype(float)
        cumulative  = []
        cumsum      = []
        
        for u in range(len(pivot)):
            content = {
                u : pivot.loc[u].drop(labels=['100']).cumsum()
            }
            cumsum.append(content)
        for i in range(12):
            data_cumulative = {
                "id"    : i+1,
                "month" : str(i+1)
            }
            for p in range(len(pivot)):
                data_cumulative[type_user[p]] = cumsum[p][p][str(102+i)]
            cumulative.append(data_cumulative)
        return cumulative
        
    def __training_dataset_pivot(self, payloads):
        pivot_data = {
            "monthly" : self.__pivot_monthly(payloads),
            "cumulative" : self.__pivot_cumulative(payloads)
        }
        return pivot_data
       
    def __training_dataset_total(self, payloads):
        type_user_summary = pd.DataFrame(payloads).drop('101',axis=1)
        for c in range(len(type_user_summary.columns.values) - 1):
            type_user_summary[str(102+c)] = type_user_summary[str(102+c)].str.replace(",", "").astype(float)
        summary = type_user_summary.groupby('100').sum()
        total = []
        for s in range(len(summary)):
            content = {}
            content['100'] = summary.iloc[s].name
            content['101'] = 'Total'
            start_no = 102
            for t in summary.iloc[s].to_dict():
                content[str(start_no)] = "{:,.0f}".format(summary.iloc[s][t])
                start_no += 1
            total.append(content)
        return total

    def __training_construct_dataset(self, payloads):
        aa = payloads.sum()
        ab = aa.loc[:,['total']].to_dict()
        response = []
        for i in ab['total']:
            content = {}
            content['100'] = i[0]
            if not any(d.get('101',None) == i[1] for d in response):
                content['101'] = i[1]
                start_no = 102
                month_count = aa.loc[i[0],i[1]].to_dict()
                grand_total = 0
                for month in range(12):
                    grand_total += month_count['total'][(month+1)] if month+1 in month_count['total'] else 0
                    content[str(start_no)] = "{0:,.0f}".format(month_count['total'][(month+1)]) if month+1 in month_count['total'] else "0"
                    start_no += 1
                content['114'] = "{0:,.0f}".format(grand_total)
                response.append(content)
        response = response + self.__training_dataset_total(response) 
        return response

    def __training_summary_report_cbt(self):
        raw         = TrainingEpolModel().read_training_cbt_summary()
        payloads    = pd.DataFrame(raw)
        data        = payloads.groupby(['type_user','course_name','month'])
        dataset     = self.__training_construct_dataset(data)
        dataset.insert(0, self.TRAINING_SUMMARY_CBT_HEADER)
        return dataset
    
    def __training_summary_report_latihan(self):
        raw         = TrainingEpolModel().read_training_latihan_summary()
        payloads    = pd.DataFrame(raw)
        data        = payloads.groupby(['type_user','course_name','month'])
        dataset     = self.__training_construct_dataset(data)
        dataset.insert(0, self.TRAINING_SUMMARY_LATIHAN_HEADER)
        return dataset

    def create_epol_dataset(self):
        start_time  = datetime.now()
        ws_name     = "EPOL STATISTIC"
        print('-- {} --'.format(ws_name))
        print('-- start query----')
        cbt = self.__training_summary_report_cbt()
        latihan_dalam_kelas = self.__training_summary_report_latihan()
        dataset = {
            "datatable" : {
                "cbt"                   : cbt,
                "latihan_dalam_kelas"   : latihan_dalam_kelas
            },
            "cockpit"   : {
                "cbt"                   : self.__training_dataset_pivot(cbt),
                "latihan_dalam_kelas"   : self.__training_dataset_pivot(latihan_dalam_kelas)
            }
        }
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
        response = Common_Query().Get_Latest_WS_Data(ws_name)[0]['ws_data']
        return json.loads(response)