from datetime import datetime

import werkzeug
import os
import flask, json

from flask import request
from flask import current_app as app
from flask_restplus import Namespace, Resource, reqparse
from ..service.sm_performance_update import SM_Performance_Update
from ..service.sm.razerpay import RazerPayServices
from ..service.sm.epol import EpolServices

api = Namespace('SM', 'Summary dataset of performance update for Supplier Management')

sm_pu = SM_Performance_Update()
cors_allow_origin = {'Access-Control-Allow-Origin': '*'}

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


file_upload = reqparse.RequestParser()
file_upload.add_argument('razer_file',  
                         type=werkzeug.datastructures.FileStorage, 
                         location='files', 
                         required=True, 
                         help='Razer Transaction file is required!')
@api.route('/razerpay-consolidation')
class RazorPayConsolidationRoute(Resource):
    @api.expect(file_upload)
    def post(self):
        print(request.form.to_dict())
        args        = file_upload.parse_args()
        razer_file  = 'razer_file'
        if args[razer_file].mimetype == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            file_name   =  args[razer_file].filename
            user_profile = request.form.to_dict()['user_profile']
            xls_file    = '%s%s' % (os.getcwd() + app.config['UPLOAD_MEDIA'], file_name)
            args[razer_file].save(xls_file)
            data        = RazerPayServices().ProcessUploadFile(xls_file, user_profile)
            return data,  200, cors_allow_origin
        else:
            return { "status" : "error..."}

@api.route('/razerpay-upload-history')
class RazerPayUploadHistoryRoute(Resource):
    def get(self):
        data = RazerPayServices().UploadHistory()
        return data

@api.route('/razerpay-transaction-detail/<razer_id>')
class RazerPayTransactionDetailRoute(Resource):
    def get(self, razer_id):
        data = RazerPayServices().ReadTransactionDetail(razer_id)
        return data

@api.route('/razerpay-transaction-overwrite')
class RazerPayTransactionOverwriteRoute(Resource):
    def post(self):
        input_data  = json.loads(request.data)
        data = RazerPayServices().RazerTransactionOverwrite(filename=input_data['filename'], user_profile=input_data['user_profile'])
        return data
    
@api.route('/razerpay-summary/<mode>')
class RazerPaySummaryRoute(Resource):
    def get(self, mode = 'datatable'):
        data = RazerPayServices().load_ws_data('RAZERPAY_TRANSACTION')
        if mode == 'datatable':
            data = data['datatable']
        if mode == 'pivot':
            data = data['cockpit']
        return data


@api.route('/epol-training/')
class EpolTrainingRoute(Resource):
    def get(self):
        data = EpolServices().get_training_summary_report()
        return data