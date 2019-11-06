
import flask

from flask_restplus import Namespace, Resource, fields
from ..service.gm.contribution_of_pv import ContributionOfPVPerformanceUpdate
from ..service.gm.pending_payment_cycle import PendingPaymentCyclePerformanceUpdate
from ..service.gm.pv_tr_summary import PvTrSummaryPerformanceUpdate
from ..service.gm.pv_status import PVStatusPerformanceUpdate
from ..service.gm.target import GM_Target
from ..service.gm.revenue import GM_Revenue
from ..service.gm.top_ptj import GM_TopPtj
from ..service.gm import GM_Lovs

from ..model.gm_query import GM_Query

gm_query = GM_Query()

api = Namespace('GM', 'Summary dataset of performance update for Government Management')

gm_contrubution_of_pv = ContributionOfPVPerformanceUpdate()
gm_pending_payment_cycle = PendingPaymentCyclePerformanceUpdate()
gm_pv_tr_summary = PvTrSummaryPerformanceUpdate()
gm_pv_status = PVStatusPerformanceUpdate()

@api.route('/pv-summary')
class GMPVSummary(Resource):
    def get(self):
        data = gm_pv_tr_summary.PVSummary()
        return data

@api.route('/tr-summary')
class GMTRSummary(Resource):
    def get(self):
        data = gm_pv_tr_summary.TRSummary()
        return data

@api.route('/pv-status')
class GMPVStatus(Resource):
    def get(self):
        data = gm_pv_status.PVStatusSummaryFromETL()
        return data

# @api.route('/pending-payment-cycle/<mode>/', endpoint= "pending-payment-cycle", defaults={ 'mode': 'amount'})
# @api.param('mode',"amount, percentage")
# class GMPendingPaymentCycle(Resource):
#     def show(self,mode):
#         pass

#     def get(self, mode):
#         data = gm_pending_payment_cycle.PendingPaymentCycle(mode)
#         return data

@api.route('/pending-payment-cycle')
class GMPendingPaymentCycle(Resource):
    def get(self):
        year = flask.request.args.get("year")
        data = gm_pending_payment_cycle.PendingPaymentCycleFromETL(year)
        return data

@api.route('/contribution-of-pv-by-ptj')
class GMContributionOfPVByPtj(Resource):
    def get(self):
        data = gm_contrubution_of_pv.ContributionOfPVByPtj()
        return data

@api.route('/top-100-ptj-details')
class GMTop100PtjDetails(Resource):
    def get(self):
        return {
            "record": "Top 100 PTJ Details"
        }

@api.route('/number-of-ptj-by-location-and-ministry')
class GMNumberOfPtjLocationMinistry(Resource):
    def get(self):
        query_result = gm_query.get_ministry_location_count()
        data = gm_pv_status.NumberOFPTJsByLocation(query_result)
        return data

@api.route('/number-of-ptj-by-ministry')
class GMNumberOfPtjByMinistry(Resource):
    def get(self):
        query_result = gm_query.get_ministry_no_of_ptj()
        data = gm_pv_status.NumberOfPtjByMinistry(query_result)
        return data

@api.route('/year-target')
class GMYearTarget(Resource):
    def get(self):
        gm_target = GM_Target()
        data = gm_target.Target_Sampling()
        return data

@api.route('/year-target-pivot')
class GMYearTargetPivot(Resource):
    def get(self):
        gm_target = GM_Target()
        data = gm_target.Target_Sampling_Pivotal()
        return data

@api.route('/revenue')
class GMRevenueRoute(Resource):
    def get(self):
        gm_revenue = GM_Revenue()
        data = gm_revenue.Revenue_Summary()
        return data

@api.route('/revenue-pivot')
class GMRevenuePivot(Resource):
    def get(self):
        gm_revenue = GM_Revenue()
        data = gm_revenue.Revenue_Pivot()
        return data

@api.route('/top-ptj')
class GMTopPtjRoute(Resource):
    def get(self):
        gm_top = GM_TopPtj()
        data = gm_top.TopPtjList('birt')
        return data

@api.route('/top-ptj-summary')
class GMTopPtjSummaryRoute(Resource):
    def get(self):
        year = flask.request.args.get("year")
        data = GM_TopPtj().top_ptj_list_summary(str(year).replace("'",""))
        return data

    
@api.route('/fulfilment-year')
class GMFulfilmentYearRoute(Resource):
    def get(self):
        return GM_Lovs().available_fulfilment_year()