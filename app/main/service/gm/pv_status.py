import collections
import pandas as pd
import json

from ..common import CommonMethod
from ...model.mysql.government_management import MYSQL_GM_QUERY
from datetime import datetime,date

common = CommonMethod()

class PVStatus: 
    PV_STATUS = (
        'MINISTRY',
        'ACTUAL PV',
        'ORDER STATUS',
        'CANCEL',
        'PENDING PAYMENT'
    )
    MINISTY_LOCATION = [{
        'zone': 'KV',
        'state': [
            'WILAYAH PERSEKUTUAN KUALA LUMPUR',
            'SELANGOR',
            'WILAYAH PERSEKUTUAN PUTRAJAYA'
        ]
    },
    {
        'zone': 'OKV',
        'state': [
            'JOHOR',
            'PERAK',
            'KELANTAN',
            'TERENGGANU',
            'PAHANG',
            'KEDAH',
            'NEGERI SEMBILAN',
            'PULAU PINANG',
            'MELAKA',
            'PERLIS'
        ]
    },
    {
        'zone': 'em',
        "state":[
            'SARAWAK',
            'SABAH',
            'WILAYAH PERSEKUTUAN LABUAN'
        ]
    }]

class PVStatusPerformanceUpdate(PVStatus):

    def PVStatusSummaryFromETL(self):
        ws_name = "GM_PV_STATUS"
        gm_query = MYSQL_GM_QUERY()
        existed = gm_query.Get_Latest_WS(ws_name)
        if len(existed) > 0:
            dataset = json.loads(existed[0]['ws_data'])
        else:
            dataset = self.__CreatePVStatus()
        return dataset

    def __CreatePVStatus(self):
        start_time = datetime.now()
        print('-- GM PV STATUS --')
        print('-- start query----')
        dataset = self.__PVStatusSummaryNew()
        print('-- end query-----')
        end_time = datetime.now()
        input = {
            "ws_name": "GM_PV_STATUS",
            "ws_is_active": "1",
            "ws_desc": "GM PV Status as at {}".format(date.today().strftime("%d %B %Y")),
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
        gm_query = MYSQL_GM_QUERY()
        gm_query.create_new_ws(input)
        return dataset

    def __PVStatusSummaryNew(self):
        gm_model = MYSQL_GM_QUERY()
        ministry = gm_model.ReadMinistryActive()
        data = []
        actual_pvs = self.__PvStatusActualPV()
        cancel = self.__PVStatusPOCancel()
        pending_payment_pvs = self.__PVStatusPendingPayment()
        for i in ministry:
            actual_pv = self.__PVStatusByMinistry(actual_pvs,'ministry_id', i['org_profile_id'])
            cancel_pv = self.__PVStatusByMinistry(cancel,'ministry_id', i['org_profile_id'])
            pending_payment = self.__PVStatusByMinistry(pending_payment_pvs,'ministry_id',i['org_profile_id'])
            other_status = actual_pv - cancel_pv - pending_payment
            info = {}
            info['ministry']        = i['kementerian_name']
            info['actual_pv']       = common.NumberToFormat(actual_pv)
            info['other_status']    = common.NumberToFormat(other_status)
            info['cancel']          = common.NumberToFormat(cancel_pv)
            info['pending_payment'] = common.NumberToFormat(pending_payment)
            data.append(info)
        output = {
            'tabular': data,
            'pivot': {}
        }
        return output

    def __PvStatusActualPV(self):
        gm_model = MYSQL_GM_QUERY()
        actual_pv_list = gm_model.pv_status_actual_pv()
        data = []
        for i in actual_pv_list:
            content = {}
            content['ministry_id'] = i['ministry_id']
            content['total'] = float(i['total'])
            data.append(content)
        df = pd.DataFrame(data)
        return df

    def __PVStatusPOCancel(self):
        gm_model = MYSQL_GM_QUERY()
        cancel = gm_model.pv_status_cancel()
        data = []
        for i in cancel:
            content = {}
            content['ministry_id'] = i['ministry_id']
            content['total'] = float(i['total'])
            data.append(content)
        df = pd.DataFrame(data)
        return df

    def __PVStatusPendingPayment(self):
        gm_model = MYSQL_GM_QUERY()
        pending_payment = gm_model.pv_status_pending_payment()
        data = []
        for i in pending_payment:
            content = {}
            content['ministry_id'] = i['ministry_id']
            content['total'] = float(i['total'])
            data.append(content)
        df = pd.DataFrame(data)
        return df

    def __PVStatusByMinistry(self, data_frame, column, ministry_id):
        df = data_frame[data_frame[column] == ministry_id].loc[:,['total']]
        return df.to_dict('records')[0]['total'] if df.empty == False else 0

    def NumberOFPTJsByLocation(self, query_result):
        data = []
        kv = {
            'zone':'kv',
            'rows':[]
        }
        okv = {
            'zone':'okv',
            'rows':[]
        }
        em = {
            'zone':'em',
            'rows':[]
        }

        for i in query_result:
            if i['state'] in self.MINISTY_LOCATION[0]['state']:
                d = {
                    "zone":"kv",
                    "state": i['state'],
                    "no_of_ptj": i['no_of_ptj']
                }
                kv['rows'].append(d)
            if i['state'] in self.MINISTY_LOCATION[1]['state']:
                d = {
                    "zone":"kv",
                    "state": i['state'],
                    "no_of_ptj": i['no_of_ptj']
                }
                okv['rows'].append(d)
            
            if i['state'] in self.MINISTY_LOCATION[2]['state']:
                d = {
                    "zone":"kv",
                    "state": i['state'],
                    "no_of_ptj": i['no_of_ptj']
                }
                em['rows'].append(d)

        data = [kv,okv,em]
        return data

    def NumberOfPtjByMinistry(self,query_result):
        data = []
        for i in query_result:
            data.append(i)
        return data