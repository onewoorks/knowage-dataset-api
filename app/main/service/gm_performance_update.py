from . import CommonMethod
from datetime import datetime

common = CommonMethod()

class GM_Performance_Setter:
    PV_TR_SUMMARY = (
        'Date',
        'Working Days',
        'Target Daily',
        'Target Cumulative',
        'Actual Daily',
        'Actual Cumulative',
        'Variance Daily',
        'Variance Cumulative',
        'Average Daily',
        'Daily Target To Achieve'
    )

class GM_Performance_Update(GM_Performance_Setter):

    def PVSummary(self):
        return common.TemplateBuilder(self.PV_TR_SUMMARY)

    def TRSummary(self):
        return common.TemplateBuilder(self.PV_TR_SUMMARY)