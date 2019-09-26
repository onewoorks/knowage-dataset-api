from ...model.mysql.government_management import MYSQL_GM_QUERY
from .pv_status import PVStatus
from ..common import CommonMethod

from datetime import datetime, date

import pandas as pd
import json

gm_query = MYSQL_GM_QUERY()
common = CommonMethod()

class TOP_PTJ_SETTER:
    WS_NAME = {
        "PTJ_TOP_100" : "GM_PTJ_TOP_100"
    }

class GM_TopPtj(TOP_PTJ_SETTER):
    
    def TopPtjList(self, mode = 'birt'):
        dataset = self.__CheckWS()
        if mode == 'birt':
            dataset = self.__BirtDataset(dataset)
        return dataset

    def TopPtjListSummary(self):
        dataset = self.__DatasetSummary(self.__CheckWS())
        return dataset

    def __CheckWS(self):
        ws_name = self.WS_NAME['PTJ_TOP_100']
        existed = gm_query.Get_Latest_WS(ws_name)
        if len(existed) > 0:
            dataset = json.loads(existed[0]['ws_data'])
        else:
            dataset = self.__CreateWSData()
        return dataset

    def __PtjProfile(self):
        ptjs = gm_query.Read_PTJ_Profile()
        return ptjs

    def __PtjMinistry(self):
        ministries = gm_query.Read_All_PTJ_Ministry()
        return ministries

    def __TopPtjs(self):
        top_ptjs = gm_query.top_ptj()
        return top_ptjs

    def __StateZone(self):
        dd = pd.DataFrame(PVStatus.MINISTY_LOCATION)
        clean_dd = dd.state.apply(pd.Series) \
            .merge(dd, left_index= True, right_index = True) \
            .drop(['state'],axis=1) \
            .melt(id_vars= ['zone'], value_name = "state") \
            .drop(['variable'], axis = 1) \
            .dropna()
        return clean_dd

    def __CreateNewTopPtjList(self):
        df_ptj_profile              = pd.DataFrame(self.__PtjProfile())
        df_ptj_ministries           = pd.DataFrame(self.__PtjMinistry())
        df_top_ptjs                 = pd.DataFrame(self.__TopPtjs())
        df_current_target           = pd.DataFrame(gm_query.ReadPVTargetAsNow())
        df_current_actual           = pd.DataFrame(gm_query.pv_status_actual_pv_by_ptj())
        detail_top_ptj_100          = []
        target_year                 = "target {}".format(datetime.today().year).upper()
        total_target_as_month_year  = "total target as of {} {}".format(datetime.now().strftime("%B"), datetime.now().year).upper()
        total_actual_as_month_year  = "total actual as of {} {}".format(datetime.now().strftime("%B"), datetime.now().year).upper()
        variance_as_month_year      = "variance as of {} {}".format(datetime.now().strftime("%B"), datetime.now().year).upper()
        state_zone = self.__StateZone()
        for i in df_top_ptjs.to_dict('records'):
            target                  = df_top_ptjs[df_top_ptjs['ptj_code'] == i['ptj_code']].to_dict('records')[0]['target']
            ptj_info                = df_ptj_ministries[df_ptj_ministries['ptj_code'] == i['ptj_code']].to_dict('records')[0]
            ptj_state               = df_ptj_profile[df_ptj_profile['org_code'] == i['ptj_code']].to_dict('records')[0]
            current_target          = df_current_target[df_current_target['ptj_code'] == i['ptj_code']].to_dict('records')[0]['target']
            current_actual          = df_current_actual[df_current_actual['ptj_id'] == ptj_state['org_profile_id']]
            current_actual_value    = float(current_actual.to_dict('records')[0]['total']) if current_actual.empty == False else 0
            content = {
                "ZONE"                      : state_zone[state_zone['state'] == ptj_state['state_name']].to_dict('records')[0]['zone'],
                "PTJ STATE"                 : ptj_state['state_name'],
                "PTJ NAME"                  : "{} - {}".format(ptj_info['kementerian_name'], ptj_info['ptj_name']),
                target_year                 : common.NumberToFormat(float(target)),
                total_target_as_month_year  : common.NumberToFormat(float(current_target)),
                total_actual_as_month_year  : common.NumberToFormat(float(current_actual_value)),
                variance_as_month_year      : common.NumberToFormat(float(current_actual_value) - float(current_target))
            }
            detail_top_ptj_100.append(content)
        return detail_top_ptj_100

    def __CreateWSData(self ):
        start_time = datetime.now()
        ws_name = "GM PTJ TOP 100"
        print('-- {} --'.format(ws_name))
        print('-- start query----')
        dataset = self.__CreateNewTopPtjList()
        print('-- end query-----')
        end_time = datetime.now()
        input = {
            "ws_name": "{}".format(ws_name.replace(' ','_')),
            "ws_is_active": "1",
            "ws_desc": "{} as at {}".format(ws_name, date.today().strftime("%d %B %Y")),
            "ws_group": "GM",
            "ws_start_execute": start_time,
            "ws_end_execute": end_time,
            "ws_duration": int((end_time-start_time).total_seconds()),
            "ws_data": json.dumps(dataset),
            "ws_created_at": datetime.now(),
            "ws_updated_at": datetime.now(),
            "ws_status": "SUCCESS",
            "ws_error": ""
        }
        gm_query.create_new_ws(input)
        return dataset

    def __BirtDataset(self, dataset):
        birt_dataset = []   
        for index,p in enumerate(dataset):
            start_no = 100
            content = {}
            for col in p:
                content[start_no] = p[col] if index > 0 else col
                start_no += 1
            birt_dataset.append(content)
            
        return birt_dataset
    
    def __ZoneStateSummary(self, dataset):
        df_zs_s = dict(tuple(dataset.groupby('ZONE')))
        data_zone_state = []
        for i in df_zs_s:
            content = {}
            content['ZONE'] = i.upper()
            content['STATES'] = []
            states = dict(tuple(df_zs_s[i].groupby('PTJ STATE')))
            for ss in states:
                content_1 = {}
                content_1['PTJ STATE'] = ss
                for sss in states[ss]:
                    content_1[sss] = "{0:.2f}".format(states[ss][sss].values[0])
                content['STATES'].append(content_1)
            data_zone_state.append(content)

        return data_zone_state
    
    def __DatasetSummary(self, dataset):
        df = pd.DataFrame(dataset)
        df_loc = df.iloc[:,2:-1]
        for l in df_loc:
            df[l] = df[l].apply(lambda x : x.replace(',','')).astype('float')
        new_columns_order = [6,1,0,2,3,4,5]
        df              = df[df.columns[new_columns_order]]
        by_zone         = df.groupby('ZONE').sum().round(2)
        by_state        = df.groupby('PTJ STATE').sum().round(2)
        by_zone_state   = df.groupby(['ZONE','PTJ STATE']).sum().round(2)
        summary = {
            "by_zone"       : by_zone.to_dict('records'),
            "by_state"      : by_state.to_dict('records'),
            "by_zone_state" : self.__ZoneStateSummary(by_zone_state),
            "test_je"       : [
                                {
                                    "zone": "KV",
                                    "ptj" : "ptj a",
                                    "target a" : "20",
                                    "target b" : "10",
                                    "target c" : "9",
                                    "target d" : "1"
                                },
                                {
                                    "zone": "KV",
                                    "ptj" : "ptj a",
                                    "target a" : "20",
                                    "target b" : "10",
                                    "target c" : "9",
                                    "target d" : "1"
                                },
                                {
                                    "zone": "KV",
                                    "ptj" : "ptj a",
                                    "target a" : "20",
                                    "target b" : "10",
                                    "target c" : "9",
                                    "target d" : "1"
                                },
                                {
                                    "zone": "KV",
                                    "ptj" : "ptj a",
                                    "target a" : "20",
                                    "target b" : "10",
                                    "target c" : "9",
                                    "target d" : "1"
                                }
                                ]
        }
        return summary
