from flask_restplus import Namespace, Resource
from ..service.training.epol import EpolServices

api = Namespace('training','Training dataset')

@api.route('/statistic/<mode>')
class StatisicRoute(Resource):
    def get(self, mode = 'datatable'):
        data = EpolServices().load_ws_data('EPOL_STATISTIC')
        if mode == 'datatable':
            data = data['datatable']
        if mode == 'pivot':
            data = data['cockpit']
        return data

@api.route('/latihan-dalam-kelas')
class LatihanDalamKelasRoute(Resource):
    def get(self):
        data = EpolServices().get_training_summary_report_latihan()
        return data

@api.route('/cbt')
class CbtRoute(Resource):
    def get(self):
        data = EpolServices().get_training_summary_report_cbt()
        return data

@api.route('/update-latest-data')
class UpdateLatestData(Resource):
    def get(self):
        data = EpolServices().create_epol_dataset()
        return {
            "status"    : "performed latest data for training module",
            "response"  : data
        }