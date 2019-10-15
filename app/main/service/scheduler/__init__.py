from ..sm.razerpay import RazerPayServices
from ...model.mysql import Common_Query

class SchedulerService:

    def generate_json_data(self, parameter_list):
        self.__razerpay_transaction()

    def __razerpay_transaction(self):
        RazerPayServices().create_razerpay_dataset()
        