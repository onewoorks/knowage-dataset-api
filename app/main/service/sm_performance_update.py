import math
import json
from datetime import date, datetime

from .common import CommonMethod
from ..model.sm_query import SM_Query
from ..model.common import Common_Query

common = CommonMethod()
sm_query = SM_Query()
common_query = Common_Query()


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

    def date_column(self, working_days):
        content = {' topic': 'Date'}
        no = 97
        for i in working_days:
            cur_no = chr(no)
            content[cur_no] = i
            no += 1
        return content

    def content_builder(self, topic, arrayData, scale=1):
        content = {' topic': topic}
        no = 97
        for i in arrayData:
            cur_no = chr(no)
            content[cur_no] = str(round(i['total']/scale))
            no += 1
        return content

    def total_daily(self, mode, topic, working_days, target_new, target_renew):
        content = {' topic': topic}
        no = 97
        for i in working_days:
            cur_no = chr(no)
            content[cur_no] = int(target_new[cur_no]) + \
                int(target_renew[cur_no])
            no += 1
        return content

    def total_commulative(self, mode, topic, working_days, target_new, target_renew):
        content = {' topic': topic}
        no = 97
        commulative = 0
        for i in working_days:
            cur_no = chr(no)
            commulative = int(commulative) + \
                int(target_new[cur_no]) + int(target_renew[cur_no])
            content[cur_no] = commulative
            no += 1
        return content

    def variance(self, topic, working_days, actual_new, target_new):
        content = {' topic': topic}
        no = 97
        for i in working_days:
            cur_no = chr(no)
            variance = int(actual_new[cur_no]) - int(target_new[cur_no])
            content[cur_no] = variance
            no += 1
        return content

    def variance_commulative(self, mode, topic, working_days, target_new, target_renew):
        content = {' topic': topic}
        no = 97
        commulative = 0
        for i in working_days:
            cur_no = chr(no)
            commulative = int(commulative) + \
                int(target_new[cur_no]) + int(target_renew[cur_no])
            content[cur_no] = commulative
            no += 1
        return content

    def total_variance(self, topic, working_days, variance_new, variance_renew):
        content = {' topic': topic}
        no = 97
        for i in working_days:
            cur_no = chr(no)
            variance = int(variance_new[cur_no]) + int(variance_renew[cur_no])
            content[cur_no] = variance
            no += 1
        return content

    def total_commulative_variance(self, mode, topic, working_days, variance_new, variance_renew):
        content = {' topic': topic}
        no = 97
        commulative = 0
        for i in working_days:
            cur_no = chr(no)
            commulative = int(
                commulative) + int(variance_new[cur_no]) + int(variance_renew[cur_no])
            content[cur_no] = commulative
            no += 1
        return content

    def dailySupplierRevenueMOF(self):
        working_days = common.GetWorkingDay()
        date = self.date_column(working_days)
        target_new = self.content_builder('Target New', sm_query.union_supplier_revenue(
            working_days, 'TARGET_NEW_SUPPLIER_WORKING_DAY'))
        target_renew = self.content_builder('Target Renew', sm_query.union_supplier_revenue(
            working_days, 'TARGET_RENEW_SUPPLIER_WORKING_DAY'))
        total_daily_target = self.total_daily(
            'total', 'Total Daily Target', working_days[:-1], target_new, target_renew)
        total_commulative_target = self.total_commulative(
            'commulative', 'Total Commulative Target', working_days[:-1], target_new, target_renew)
        actual_new = self.content_builder(
            'Actual New', sm_query.ora_actual_supplier_revenue(working_days[:-1], 'N'), 1)
        actual_renew = self.content_builder(
            'Actual Renew', sm_query.ora_actual_supplier_revenue(working_days[:-1], 'R'), 1)
        total_daily_actual = self.total_daily(
            'total', 'Total Daily Actual', working_days[:-1], actual_new, actual_renew)
        total_commulative_actual = self.total_commulative(
            'commulative', 'Total Commulative Actual', working_days[:-1], actual_new, actual_renew)
        variance_new = self.variance(
            'Variance New', working_days[:-1], actual_new, target_new)
        variance_renew = self.variance(
            'Variance Renew', working_days[:-1], actual_renew, target_renew)
        total_daily_variance = self.total_variance(
            'Total Daily Variance', working_days[:-1], variance_new, variance_renew)
        total_commulative_variance = self.total_commulative_variance(
            'commulative', 'Total Commulative Variance', working_days[:-1], variance_new, variance_renew)
        dataset = [
            date,
            target_new,
            target_renew,
            total_daily_target,
            total_commulative_target,
            actual_new,
            actual_renew,
            total_daily_actual,
            total_commulative_actual,
            variance_new,
            variance_renew,
            total_daily_variance,
            total_commulative_variance
        ]
        return dataset

    def createMOFRegistrationDataset(self):
        start_time = datetime.now()
        print('----start query----')
        dataset = self.dailySupplierRevenueMOF()
        print('----end query-----')
        end_time = datetime.now()

        input = {
            "ws_name": "MOF_REGISTRATION",
            "ws_is_active": "1",
            "ws_desc": "Supplier Revenue Summary - MOF Registration as at {}".format(date.today().strftime("%d %B %Y")),
            "ws_group": "SM",
            "ws_start_execute": start_time,
            "ws_end_execute": end_time,
            "ws_duration": int((end_time-start_time).total_seconds()),
            "ws_data": json.dumps(dataset),
            "ws_created_at": datetime.now(),
            "ws_updated_at": datetime.now(),
            "ws_status": "SUCCESS",
            "ws_error": ""
        }
        common_query.register_ws(input)
        return dataset

    def SupplierRevenueSummaryPivot(self):
        ws_name = "MOF_REGISTRATION"
        existed = sm_query.get_today_ws_name(ws_name, str(date.today()))
        if len(existed) > 0:
            dataset = json.loads(existed[0]['ws_data'])
        else:
            dataset = self.createMOFRegistrationDataset()
        return self.MofRegistrationPivot(dataset)

    def pivot_construct(self, rows):
        data = {}
        for i in rows:
            data[i] = rows[i]
        return data

    def MofRegistrationPivot(self, dataset):
        working_days = dataset[0]
        days = []
        for b in dataset:
            if b[' topic'] == "Date":
                column_date = self.pivot_construct(b)

            if b[' topic'] == "Total Daily Target":
                total_daily_target = self.pivot_construct(b)

            if b[' topic'] == "Total Commulative Target":
                total_commulative_target = self.pivot_construct(b)

            if b[' topic'] == "Total Daily Actual":
                total_daily_actual = self.pivot_construct(b)

            if b[' topic'] == "Total Commulative Actual":
                total_commulative_actual = self.pivot_construct(b)

        for d in working_days:
            if working_days[d] != "Date" and working_days[d] != 'TOTAL':
                days.append(d)

        pivot_data = []
        for i in days:
            content = {
                "Date": column_date[i],
                "Total Daily Target": total_daily_target[i],
                "Total Commulative Target": total_commulative_target[i],
                "Total Daily Actual": total_daily_actual[i],
                "Total Commulative Actual" : total_commulative_actual[i]
            }
            pivot_data.append(content)
        return pivot_data

    def SupplierRevenueSummary(self):
        ws_name = "MOF_REGISTRATION"
        existed = sm_query.get_today_ws_name(ws_name, str(date.today()))
        if len(existed) > 0:
            dataset = json.loads(existed[0]['ws_data'])
        else:
            dataset = self.createMOFRegistrationDataset()
        return common.TemplateBuilderData(dataset)

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
                "training": {
                    "target": 359000,
                    "actual": 141000,
                    "variance": 218000
                },
                "soft_cert": {
                    "target": "",
                    "actual": 8760,
                    "variance": ""
                }
            },
            "year_to_date": {
                "mof_registration": {
                    "target": 11360000,
                    "actual": 10490000,
                    "variance": 870000
                },
                "training": {
                    "target": 1690000,
                    "actual": 1020000,
                    "variance": 670000
                },
                "soft_cert": {
                    "target": "",
                    "actual": 78840,
                    "variance": ""
                }
            }
        }]
        return dashboard

    def CalculateActualPercentage(self, target, actual):
        diff = target - actual
        result = 100
        if diff > 0:
            result = (diff/target)*100
        return result

    def SMDashboardSummary(self):
        dashboard = [
            {
                "category": "MOF REGISTRATION",
                "target": 2010000,
                "actual": 1020000,
                "variance": 990000,
                "actual_percentage": self.CalculateActualPercentage(target=2010000, actual=1020000)
            },
            {
                "category": "TRAINING",
                "target": 359000,
                "actual": 141000,
                "variance": 218000,
                "actual_percentage": self.CalculateActualPercentage(target=359000, actual=141000)
            },
            {
                "category": "SOFT CERT",
                "target": 0,
                "actual": 8760,
                "variance": "",
                "actual_percentage": self.CalculateActualPercentage(target=0, actual=8760)
            }
        ]
        return dashboard
