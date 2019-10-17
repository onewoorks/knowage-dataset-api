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
                    content[str(start_no)] = month_count['total'][(month+1)] if month+1 in month_count['total'] else 0
                    start_no += 1
                content['114'] = grand_total
                response.append(content)
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
        dataset = {
            "datatable" : {
                "cbt"   : self.__training_summary_report_cbt(),
                "latihan_dalam_kelas" : self.__training_summary_report_latihan()
            },
            "cockpit"   : {
                "cbt"                   : {},
                "latihan_dalam_kelas"   : {}
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