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