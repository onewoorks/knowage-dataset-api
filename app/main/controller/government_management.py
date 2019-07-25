from flask_restplus import Namespace, Resource
from ..service.gm_performance_update import GM_Performance_Update

api = Namespace('GM', 'Summary dataset of performance update for Government Management')

gm_pu = GM_Performance_Update()

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
        data = gm_pu.TestCommon()
        return data

@api.route('/pending-payment-cycle')
class GM_PendingPaymentCycle(Resource):
    def get(self):
        return {
            "record": "Pending Payment Cycle"
        }

@api.route('/contribution-of-pv-by-ptj')
class GM_ContributionOfPVByPtj(Resource):
    def get(self):
        return {
            "record": "Contribution of PV By PTJ"
        }

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
