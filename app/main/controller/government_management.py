from flask_restplus import Namespace, Resource
from ..service.gm_performance_update import GM_Performance_Update
from ..service.gm.contribution_of_pv import ContributionOfPVPerformanceUpdate
from ..service.gm.pending_payment_cycle import PendingPaymentCyclePerformanceUpdate

api = Namespace('GM', 'Summary dataset of performance update for Government Management')

gm_pu = GM_Performance_Update()
gm_contrubution_of_pv = ContributionOfPVPerformanceUpdate()
gm_pending_payment_cycle = PendingPaymentCyclePerformanceUpdate()

@api.route('/pv-summary')
class GM_PVSummary(Resource):
    def get(self):
        data = gm_pu.PVSummary()
        return data

@api.route('/tr-summary')
class GM_TRSummary(Resource):
    def get(self):
        data = gm_pu.TRSummary()
        return data

@api.route('/pv-status')
class GM_PVStatus(Resource):
    def get(self):
        return { 
            "data":"no data"
        }

@api.route('/pending-payment-cycle/<mode>/', endpoint= "pending-payment-cycle", defaults={ 'mode': 'amount'})
@api.param('mode',"amount, percentage")
class GM_PendingPaymentCycle(Resource):
    def show(self,mode):
        pass

    def get(self, mode):
        data = gm_pending_payment_cycle.PendingPaymentCycle(mode)
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
        return {
            "record": "Number of PTJ Location and Ministry"
        }
