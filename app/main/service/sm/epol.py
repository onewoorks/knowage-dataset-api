from ...model.mysql import Common_Query
from ...model.mysql.sm_epol import SmEpolModel

class EpolServices:

    def get_training_summary_report(self):
        data = SmEpolModel().read_training_summary_report()
        return data