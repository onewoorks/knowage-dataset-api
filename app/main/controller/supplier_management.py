from datetime import datetime

import werkzeug
import os
from flask_restplus import Namespace, Resource, reqparse
from ..service.sm_performance_update import SM_Performance_Update
from ..service.sm.razorpay import RazorPayServices

api = Namespace('SM', 'Summary dataset of performance update for Supplier Management')

sm_pu = SM_Performance_Update()

file_upload = reqparse.RequestParser()
file_upload.add_argument('xls_file',  
                         type=werkzeug.datastructures.FileStorage, 
                         location='files', 
                         required=True, 
                         help='XLS file')

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
        data = sm_pu.SMDashboardSummary(None)
        return data 

@api.route('/dashboard-summary-module/<module_name>')
class DashboardSummaryModule(Resource):
    def get(self, module_name):
        data = sm_pu.SMDashboardSummary(module_name)
        return data

@api.route('/prediction/lr')
class PredictionLRRoute(Resource):
    def get(self):
        data = sm_pu.MOF_Predict()
        return data

@api.route('/razorpay-consolidation')
class RazorPayConsolidationRoute(Resource):
    @api.expect(file_upload)
    def post(self):
        
        args = file_upload.parse_args()
        if args['xls_file'].mimetype == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            file_name =  args['xls_file'].filename
            xls_file = '%s%s' % (os.getcwd()+'/upload_media/', file_name)
            args['xls_file'].save(xls_file)
            data = RazorPayServices().ProcessUploadFile(file_name)
            
            return data