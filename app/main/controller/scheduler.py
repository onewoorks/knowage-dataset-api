from flask_restplus import Namespace, Resource
from dotenv import load_dotenv
import os, json, flask, time
from datetime import datetime

import random, names

from ..service.sm.razerpay import RazerPayServices
from ..service.gm.pending_payment_cycle import PendingPaymentCyclePerformanceUpdate
from ..service.training.epol import EpolServices

api = Namespace('scheduler','Retrieve latest etl and construct json file for quick response query')

@api.route('/generate')
class SchedularGenerate(Resource):
    def get(self):
        RazerPayServices().create_razerpay_dataset()
        PendingPaymentCyclePerformanceUpdate().create_new_pending_payment_cycle_dataset()
        EpolServices().create_epol_dataset()
        return {
            "status" : "scheduler run completed"
        }

@api.route('/stream-test')
class SchedularStreamTestRoute(Resource):
    def get(self):
        return flask.Response(self.event_stream(), mimetype="text/event-stream")

    def event_stream(self):
        while True:
            time.sleep(2)
            zone_a = random.randint(1,40)
            zone_b = random.randint(1,90)
            zone_c = random.randint(1,100)
            zone_d = random.randint(1,70)
            total_zone = zone_a + zone_b + zone_c + zone_d
            message = {
                "attendance" : {
                    "name" : names.get_full_name(),
                    "counter" : random.randint(1,15),
                    "time"  : "2019-10-22 10:47:00",
                    "zone" : chr(random.randrange(65,68))
                },
                "zone" : {
                    "A" : {
                        "present" : zone_a,
                        "total" : 40
                    },
                    "B" : {
                        "present" : zone_b,
                        "total" : 90,
                    },
                    "C" : {
                        "present" : zone_c,
                        "total" : 100
                    },
                    "D" : {
                        "present" : zone_d,
                        "total" :70
                    },
                    "TOTAL" : {
                        "present" : total_zone,
                        'total'     : 40 + 90 + 100 + 70
                    }

                }
            }
            print("Sending {}".format(json.dumps(message)))
            yield "data: {}\n\n".format(json.dumps(message))


  