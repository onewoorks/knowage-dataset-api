from datetime import datetime

from flask_restplus import Namespace, Resource
from ..service.sm_performance_update import SM_Performance_Update
api = Namespace('SM', 'Summary dataset of performance update for Supplier Management')

sm_pu = SM_Performance_Update()

@api.route('/supplier-revenue-summary/mof-registration')
class SupplierRevenueSummary(Resource):
    def get(self):
        data = sm_pu.SupplierRevenueSummary()
        return data

@api.route('/supplier-revenue-summary/mof-registration-pivot')
class SupplierRevenueSummaryPivot(Resource):
    def get(self):
        data = sm_pu.SupplierRevenueSummaryPivot()
        return data

@api.route('/supplier-revenue-summary/training')
class SRS_Training(Resource):
    def get(self):
        data = sm_pu.SupplierRevenueSummaryTraining()
        return data

@api.route('/supplier-revenue-summary/soft-cert')
class SRS_SoftCert(Resource):
    def get(self):
        data = sm_pu.SoftCertSummary()
        return data

@api.route('/supplier-revenue-summary/mof-registration-renewal-conversion-performance')
class SRS_RegistrationRenewalConversionPerformance(Resource):
    def get(self):
        return {
            "record":"Renewal Conversion Performance summary"
        }
    
@api.route('/dashboard-summary')
class DashboardSummary(Resource):
    def get(self):
        # data = sm_pu.SMDashboardSummary(None)
        # return data 
        return "ok"

@api.route('/dashboard-summary-module/<module_name>')
class DashboardSummaryModule(Resource):
    def get(self, module_name):
        data = sm_pu.SMDashboardSummary(module_name)
        return data

@api.route('/prediction/lr')
class PredictionLR(Resource):
    def get(self):
        data = sm_pu.MOF_Predict()
        return data