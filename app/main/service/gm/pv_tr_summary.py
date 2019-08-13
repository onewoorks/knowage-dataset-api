from ..common import CommonMethod

common = CommonMethod()

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
        return common.TemplateBuilder(self.PV_TR_SUMMARY)

    def TRSummary(self):
        return common.TemplateBuilder(self.PV_TR_SUMMARY)
    
    def TRSummarize(self):
        pass 