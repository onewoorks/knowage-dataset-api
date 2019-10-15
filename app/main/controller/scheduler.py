from flask_restplus import Namespace, Resource
from dotenv import load_dotenv
import os

from ..service.sm.razerpay import RazerPayServices
from ..service.gm.pending_payment_cycle import PendingPaymentCyclePerformanceUpdate

api = Namespace('scheduler','Retrieve latest etl and construct json file for quick response query')

@api.route('/generate')
class SchedularGenerate(Resource):
    def get(self):
        RazerPayServices().create_razerpay_dataset()
        PendingPaymentCyclePerformanceUpdate().create_new_pending_payment_cycle_dataset()
        return {
            "status" : "scheduler run completed"
        }