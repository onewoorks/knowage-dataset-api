from . import CommonMethod

common = CommonMethod()

class SM_Performance_Setter:
    SOFTCERT_SUMMARY = (
        'Date',
        'Working Days',
        'Actual',
        'Actual Cumulative'
    )
    SUPPLIER_REVENUE_SUMMARY_MOF_REGISTRATION = (
        'Date',
        'Working Days',
        'Target New',
        'Target Renew',
        'Total Daily Target',
        'Total Cumulative Target',
        'Actual New',
        'Actual Renew',
        'Total Daily Actual',
        'Total Cumulative Actual',
        'Variance New',
        'Variance Renew',
        'Total Daily Variance',
        'Total Cumulative Variance',
        'Daily Actual',
        'Daily Target To Achieve'
    )
    SUPPLIER_REVENUE_SUMMARY_TRAINING = (
        'Date',
        'Working Day',
        'Target',
        'Cumulative',
        'CDC Sales',
        'CASB Sales',
        'CDCi Sales',
        'Total Actual',
        'Cumulative Actual',
        'Variance',
        'Cumulative Variance',
        'Daily Actual',
        'Daily Target To Achieve'
    )


class SM_Performance_Update(SM_Performance_Setter):

    def SupplierRevenueSummary(self):
        return common.TemplateBuilder(self.SUPPLIER_REVENUE_SUMMARY_MOF_REGISTRATION)

    def SoftCertSummary(self):
        return common.TemplateBuilder(self.SOFTCERT_SUMMARY)

    def SupplierRevenueSummaryTraining(self):
        return common.TemplateBuilder(self.SUPPLIER_REVENUE_SUMMARY_TRAINING)
