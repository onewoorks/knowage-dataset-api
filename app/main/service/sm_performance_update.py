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

    def SMDashboard(self):
        dashboard = [{
            "monthly": {
                "mof_registration": {
                    "target": 2010000,
                    "actual": 1020000,
                    "variance": 990000
                },
                "training":{
                    "target":359000,
                    "actual": 141000,
                    "variance": 218000
                },
                "soft_cert":{
                    "target":"",
                    "actual":8760,
                    "variance":""
                }
            },
            "year_to_date": {
                "mof_registration": {
                    "target": 11360000,
                    "actual": 10490000,
                    "variance": 870000
                },
                "training":{
                    "target":1690000,
                    "actual":1020000,
                    "variance":670000
                },
                "soft_cert":{
                    "target":"",
                    "actual":78840,
                    "variance":""
                }
            }
        }]
        return dashboard
