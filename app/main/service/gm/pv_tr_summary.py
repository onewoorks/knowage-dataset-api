from ..common import CommonMethod
from ...model.gm_query import GM_Query

common = CommonMethod()
gm_query = GM_Query()

class PvTrSummary:
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
    TR_SUMMARIZE = (
        'TR Target',
        'TR YTD Target',
        'TR Actual',
        'TR YTD Actual',
        'Variance',
        'YTD Variance'
    )


class PvTrSummaryPerformanceUpdate(PvTrSummary):
    def PVSummary(self):
        tr_data = self.dailyPvSummaryDate()
        return common.TemplateBuilder(self.PV_TR_SUMMARY,tr_data)

    def TRSummary(self):
        return common.TemplateBuilder(self.PV_TR_SUMMARY)

    def TRSummarize(self):
        pass

    def dailyPvSummaryDate(self):
        PV_working_days = common.GetWorkingDay()
        print(PV_working_days)
        dataset = {
            'Working Days': 1,
            'Target Daily': 80,
            'Target Cumulative':0,
            'Actual Daily':0,
            'Actual Cumulative':0,
            'Variance Daily':0,
            'Variance Cumulative':0,
            'Average Daily':0,
            'Daily Target To Achieve':0
        }
        return dataset
