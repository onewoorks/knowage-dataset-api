import requests

from flask_restplus import Namespace, Resource
from ..service.gm.contribution_of_pv import ContributionOfPVPerformanceUpdate
from ..service.gm.pending_payment_cycle import PendingPaymentCyclePerformanceUpdate
from ..service.gm.pv_tr_summary import PvTrSummaryPerformanceUpdate
from ..service.gm.pv_status import PVStatusPerformanceUpdate

from ..model.gm_query import GM_Query

gm_query = GM_Query()

api = Namespace('GM', 'Summary dataset of performance update for Government Management')

gm_contrubution_of_pv = ContributionOfPVPerformanceUpdate()
gm_pending_payment_cycle = PendingPaymentCyclePerformanceUpdate()
gm_pv_tr_summary = PvTrSummaryPerformanceUpdate()
gm_pv_status = PVStatusPerformanceUpdate()

@api.route('/pv-summary')
class GM_PVSummary(Resource):
    def get(self):
        data = gm_pv_tr_summary.PVSummary()
        return data

@api.route('/tr-summary')
class GM_TRSummary(Resource):
    def get(self):
        data = gm_pv_tr_summary.TRSummary()
        return data

@api.route('/pv-status')
class GM_PVStatus(Resource):
    def get(self):
        ministry = gm_query.get_pv_status()
        data = gm_pv_status.PVStatusSummary(ministry)
        return data

# @api.route('/pending-payment-cycle/<mode>/', endpoint= "pending-payment-cycle", defaults={ 'mode': 'amount'})
# @api.param('mode',"amount, percentage")
# class GM_PendingPaymentCycle(Resource):
#     def show(self,mode):
#         pass

#     def get(self, mode):
#         data = gm_pending_payment_cycle.PendingPaymentCycle(mode)
#         return data

@api.route('/pending-payment-cycle')
class GM_PendingPaymentCycle(Resource):
    def get(self):
        data = requests.get('http://192.168.62.138:5155/rest/ep/fl/cycle-pending-payment')
        return data.json()

@api.route('/contribution-of-pv-by-ptj')
class GM_ContributionOfPVByPtj(Resource):
    def get(self):
        data = gm_contrubution_of_pv.ContributionOfPVByPtj()
        return data

@api.route('/top-100-ptj-details')
class GM_Top100PtjDetails(Resource):
    def get(self):
        return {
            "record": "Top 100 PTJ Details"
        }

@api.route('/number-of-ptj-by-location-and-ministry')
class GM_NumberOfPtjLocationMinistry(Resource):
    def get(self):
        query_result = gm_query.get_ministry_location_count()
        data = gm_pv_status.NumberOFPTJsByLocation(query_result)
        return data

@api.route('/number-of-ptj-by-ministry')
class GM_NumberOfPtjByMinistry(Resource):
    def get(self):
        query_result = gm_query.get_ministry_no_of_ptj()
        data = gm_pv_status.NumberOfPtjByMinistry(query_result)
        return data