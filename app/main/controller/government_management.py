
from flask import request

from flask_restplus import Namespace, Resource, fields
from ..service.gm.contribution_of_pv import ContributionOfPVPerformanceUpdate
from ..service.gm.pending_payment_cycle import PendingPaymentCyclePerformanceUpdate
from ..service.gm.pv_tr_summary import PvTrSummaryPerformanceUpdate
from ..service.gm.pv_status import PVStatusPerformanceUpdate
from ..service.gm.target import GM_Target
from ..service.gm.revenue import GM_Revenue
from ..service.gm.top_ptj import GM_TopPtj

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
        data = gm_pv_status.PVStatusSummaryFromETL()
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
        data = gm_pending_payment_cycle.PendingPaymentCycleFromETL()
        return data

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

@api.route('/year-target')
class GM_YearTarget(Resource):
    def get(self):
        gm_target = GM_Target()
        data = gm_target.Target_Sampling()
        return data

@api.route('/year-target-pivot')
class GM_YearTargetPivot(Resource):
    def get(self):
        gm_target = GM_Target()
        data = gm_target.Target_Sampling_Pivotal()
        return data

@api.route('/revenue')
class GM_RevenueRoute(Resource):
    def get(self):
        gm_revenue = GM_Revenue()
        data = gm_revenue.Revenue_Summary()
        return data

@api.route('/revenue-pivot')
class GM_RevenuePivot(Resource):
    def get(self):
        gm_revenue = GM_Revenue()
        data = gm_revenue.Revenue_Pivot()
        return data

@api.route('/top-ptj')
class GM_TopPtjRoute(Resource):
    def get(self):
        gm_top = GM_TopPtj()
        data = gm_top.TopPtjList('birt')
        return data

@api.route('/top-ptj-summary')
class GM_TopPtjSummaryRoute(Resource):
    def get(self):
        # print(flask.request.args.get("name"))
        summary = GM_TopPtj()
        data = summary.TopPtjListSummary()
        return data