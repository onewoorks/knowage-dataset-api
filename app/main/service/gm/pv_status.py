import collections

from ..common import CommonMethod

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
    def PVStatusSummary(self, ministry):
        data = []
        for i in ministry:
            info = {}
            info['ministry']        = i['kementerian_name']
            info['actual_pv']       = ''
            info['other_status']    = ''
            info['cancel']          = ''
            info['pending_payment'] = ''
            data.append(info)
        return data

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