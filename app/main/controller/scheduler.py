from flask_restplus import Namespace, Resource

from ..service.sm.razerpay import RazerPayServices

api = Namespace('scheduler','Retrieve latest etl and construct json file for quick response query')

@api.route('/generate')
class SchedularGenerate(Resource):
    def get(self):
        RazerPayServices().create_razerpay_dataset()
        return {
            "status" : "scheduler run completed"
        }