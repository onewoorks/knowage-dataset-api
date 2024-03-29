import math
import json
from datetime import date, datetime

from .common import CommonMethod
from ..model.sm_query import SM_Query
from ..model.oracle.supplier_management import ORACLE_SM_QUERY
from ..model.mysql.supplier_management import SupplierManagementModel
from ..model.common import Common_Query

from .predictions.linear_regression import Lr_Predict

common = CommonMethod()
sm_query = SM_Query()
oracle_sm_query = ORACLE_SM_QUERY()
common_query = Common_Query()
mysql_sm_query = SupplierManagementModel()

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
    TOPIC = '100'
    START_NO = 101


class SM_Performance_Update(SM_Performance_Setter):

    def Dataset_MOF(self):
        ws_name = "MOF_REGISTRATION"
        existed = sm_query.get_today_ws_name(ws_name, str(date.today()))
        dataset = json.loads(existed[0]['ws_data']) if len(existed) > 0 else self.createMOFRegistrationDataset()
        return dataset

    def max_columns(self, cur_columns, columns = 30):
        empty_column = []
        while cur_columns <= columns:
            empty_column.append("")
            cur_columns += 1
        return empty_column

    def date_column(self, working_days):
        content = {'100': 'Date'}
        no = self.START_NO
        for i in working_days:
            content[no] = i
            no += 1
        return content

    def content_builder(self, topic, arrayData, scale=1, max_columns = 30):
        working_days = len(arrayData) + 1
        content = {'100': topic}
        no = self.START_NO
        for i in arrayData:
            content[no] = round(i['total']/scale)
            no += 1
        while working_days <= max_columns:
            content[no] = ""
            working_days += 1
            no += 1
        return content

    def total_daily(self, mode, topic, working_days, target_new, target_renew):
        content = {'100': topic}
        no = self.START_NO
        for i in working_days:
            if "null-" not in i:
                tn = target_new[no] if target_new[no] != "" else 0
                tr = target_renew[no] if target_renew[no] != "" else 0
                calc = tn + tr
                content[no] = int(calc) if calc > 0 else ""
            else:
                content[no] = ""
            no += 1
        return content

    def total_commulative(self, mode, topic, working_days, target_new, target_renew):
        content = {'100': topic}
        no = self.START_NO
        commulative = 0
        for i in working_days:
            if "null-" not in i:
                tn = target_new[no] if target_new[no] != "" else 0
                tr = target_renew[no] if target_renew[no] != "" else 0
                calc = tn + tr
                commulative = (int(commulative) + int(calc)) if calc != 0 else ""
                content[no] = commulative
            else:
                content[no] = ""
            no += 1
        return content

    def variance(self, topic, working_days, actual_new, target_new):
        content = {'100': topic}
        no = self.START_NO
        for i in working_days:
            if "null-" not in i:
                tn = target_new[no] if target_new[no] != "" else 0
                a_n = actual_new[no] if actual_new[no] != "" else 0
                variance = (int(a_n) - int(tn)) if actual_new[no] != "" else ""
                content[no] = variance
            else:
                content[no] = ""
            no += 1
        return content

    def variance_commulative(self, mode, topic, working_days, target_new, target_renew):
        content = {'100': topic}
        no = self.START_NO
        commulative = 0
        for i in working_days:
            if "null-" not in i:
                commulative = int(commulative) + \
                    int(target_new[no]) + int(target_renew[no])
                content[no] = commulative
            else:
                content[no] = ""
            no += 1
        return content

    def total_variance(self, topic, working_days, variance_new, variance_renew):
        content = {'100': topic}
        no = self.START_NO
        for i in working_days:
            if "null-" not in i:
                v_n = variance_new[no] if variance_new[no] != "" else 0
                v_r = variance_renew[no] if variance_renew[no] != "" else 0
                calc = int(v_n) + int(v_r)
                variance = calc if calc != 0 else ""
                content[no] = variance
            else:
                content[no] = ""
            no += 1
        return content

    def total_commulative_variance(self, mode, topic, working_days, variance_new, variance_renew):
        content = {'100': topic}
        no = self.START_NO
        commulative = 0
        for i in working_days:
            if "null-" not in i:
                v_n = variance_new[no] if variance_new[no] != "" else 0
                v_r = variance_renew[no] if variance_renew[no] != "" else 0
                calc = v_n + v_r
                commulative = int(commulative) + int(calc) if calc != 0 else ""
                content[no] = commulative
            else:
                content[no] = ""
            no += 1
        return content

    def daily_actual(self, topic, working_days, actual_cummulative):
        content = {'100': topic}
        no = self.START_NO
        index = 1
        for i in working_days: 
            if "null-" not in i:
                content[no] = int(actual_cummulative[no]/index) if actual_cummulative[no] != "" else ""
            else:
                content[no] = ""
            index += 1
            no += 1
        return content
    
    def daily_target_to_achieve(self,working_days, monthly_target, actual_cummulative):
        content = {'100':'Daily Target To Achieve'}
        no = self.START_NO
        not_null_day = [ x for x in working_days if "null-" not in x ]
        last_day_commulative = [ y for y in monthly_target if monthly_target[y] != "" ]
        month_target = monthly_target[last_day_commulative[-1]]
        working_days_in_month = len(not_null_day)
        no = self.START_NO
        index = 1
        for i in working_days:
            if "null-" not in i:
                content[no] = int((month_target - actual_cummulative[no])/(working_days_in_month)) if actual_cummulative[no] != "" else ""
                working_days_in_month -= 1
            else:
                content[no] = ""
            index += 1
            no += 1
        return content

    def empty_line(self, working_days):
        content = {'100':''}
        no = self.START_NO
        for i in working_days:
            content[no] = ""
        return content

    def dailySupplierRevenueMOF(self):
        working_days = common.GetWorkingDay()
        date = self.date_column(working_days)
        target_new = self.content_builder('Target New', sm_query.union_supplier_revenue(working_days, 'TARGET_NEW_SUPPLIER_WORKING_DAY'))
        target_renew = self.content_builder('Target Renew', sm_query.union_supplier_revenue(working_days, 'TARGET_RENEW_SUPPLIER_WORKING_DAY'))
        total_daily_target = self.total_daily('total', 'Total Daily Target', working_days, target_new, target_renew)
        total_commulative_target = self.total_commulative('commulative', 'Total Commulative Target', working_days, target_new, target_renew)
        # actual_new = self.content_builder('Actual New', oracle_sm_query.ora_actual_supplier_revenue(working_days, 'N'), 1)
        # actual_renew = self.content_builder('Actual Renew', oracle_sm_query.ora_actual_supplier_revenue(working_days, 'R'), 1)
        actual_new = self.content_builder('Actual New', mysql_sm_query.ActualSupplierRevenue(working_days, 'N'), 1)
        actual_renew = self.content_builder('Actual Renew', mysql_sm_query.ActualSupplierRevenue(working_days, 'R'), 1)
        total_daily_actual = self.total_daily('total', 'Total Daily Actual', working_days, actual_new, actual_renew)
        total_commulative_actual = self.total_commulative('commulative', 'Total Commulative Actual', working_days, actual_new, actual_renew)
        variance_new = self.variance('Variance New', working_days, actual_new, target_new)
        variance_renew = self.variance('Variance Renew', working_days, actual_renew, target_renew)
        total_daily_variance = self.total_variance('Total Daily Variance', working_days, variance_new, variance_renew)
        total_commulative_variance = self.total_commulative_variance('commulative', 'Total Commulative Variance', working_days, variance_new, variance_renew)
        daily_actual = self.daily_actual('Daily Actual',working_days, total_commulative_actual)
        daily_target_to_achieve = self.daily_target_to_achieve(working_days,total_commulative_target, total_commulative_actual)
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
            total_commulative_variance,
            self.empty_line(working_days),
            daily_actual,
            daily_target_to_achieve,
            self.MOF_Predict(working_days,total_commulative_actual)
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
        dataset = self.Dataset_MOF()
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
            if b[self.TOPIC] == "Date":
                column_date = self.pivot_construct(b)

            if b[self.TOPIC] == "Total Daily Target":
                total_daily_target = self.pivot_construct(b)

            if b[self.TOPIC] == "Total Commulative Target":
                total_commulative_target = self.pivot_construct(b)

            if b[self.TOPIC] == "Total Daily Actual":
                total_daily_actual = self.pivot_construct(b)

            if b[self.TOPIC] == "Total Commulative Actual":
                total_commulative_actual = self.pivot_construct(b)
            
            if b[self.TOPIC] == "Prediction":
                prediction = self.pivot_construct(b)
                        
        for d in working_days:
            if working_days[d] != "Date" and working_days[d] != 'TOTAL':
                days.append(d)
        pivot_data = []
        no = self.START_NO
        for i in days:
            if "null-" not in column_date[i]:
                content = {
                    "No": int(no),
                    "Date": column_date[i],
                    "Total Daily Target": total_daily_target[i],
                    "Total Commulative Target": total_commulative_target[i],
                    "Total Daily Actual": total_daily_actual[i],
                    "Total Commulative Actual" : total_commulative_actual[i],
                    "Prediction": prediction[i]
                }
                pivot_data.append(content)
            no += 1
            
        return pivot_data

    def SupplierRevenueSummary(self):
        ws_name = "MOF_REGISTRATION"
        existed = sm_query.get_today_ws_name(ws_name, str(date.today()))
        if len(existed) > 0:
            dataset = json.loads(existed[0]['ws_data'])
        else:
            dataset = self.createMOFRegistrationDataset()
        return common.TemplateBuilderData(101,dataset,"with comma")

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
        result = 100 - result
        return result

    def PerformanceMofRegistration(self):
        target = sm_query.mysql_module_target('MOF')
        actual = oracle_sm_query.actual_mof_registration()
        ytd_target = sm_query.mysql_module_ytd_target('MOF')
        ytd = oracle_sm_query.ytd_mof_registration()
        indicator = {}
        year = datetime.now().year
        indicator["GROUP_NAME"] = "MOF REGISTRATION"
        for i in target:
            code_name = i['code_name'].replace('_{}'.format(year),'')
            indicator[code_name] = float(i['amount'])
        actual_sr = 0

        indicator['ACTUAL_NEW_SUPPLIER'] = 0
        indicator['ACTUAL_RENEW_SUPPLIER'] = 0
            
        for a in actual:
            if a['APPLICATION_TYPE'] == 'N':
                indicator['ACTUAL_NEW_SUPPLIER'] += a['AMOUNT']
            if a['APPLICATION_TYPE'] == 'R':
                indicator['ACTUAL_RENEW_SUPPLIER'] += a['AMOUNT']
            actual_sr += a['AMOUNT']
        indicator['ACTUAL_SR'] = actual_sr

        indicator['ACTUAL_NEW_PERCENTAGE'] = self.CalculateActualPercentage(indicator['TARGET_NEW_SUPPLIER'], indicator['ACTUAL_NEW_SUPPLIER'])
        indicator['ACTUAL_RENEW_PERCENTAGE'] = self.CalculateActualPercentage(indicator['TARGET_RENEW_SUPPLIER'], indicator['ACTUAL_RENEW_SUPPLIER'])
        indicator['ACTUAL_MOF_PERCENTAGE'] = self.CalculateActualPercentage(indicator['TARGET_SR'], indicator['ACTUAL_SR'])
        for yt in ytd_target:
            code_name = yt['code_name'].replace('_SUPPLIER_WORKING_DAY','') + '_YTD'
            indicator[code_name] = float(yt['ytd_target'])
        for y in ytd:
            if y['APPLICATION_TYPE'] == "N":
                indicator['ACTUAL_NEW_YTD'] = y['AMOUNT']
            if y['APPLICATION_TYPE'] == "R":
                indicator['ACTUAL_RENEW_YTD'] = y['AMOUNT']
        return indicator

    def SMDashboardSummary(self, module = 'all'):
        if module == "mof_registration":
            data = self.PerformanceMofRegistration()
        if module == None:
            data = [
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
        return data

    def MOF_Predict(self, working_days, total_actual_cummulative):
        work_days = []
        day = 1
        for k in working_days:
            if "null-" not in k:
                work_days.append(day)
                day += 1
        actual_cummulative = []
        for i in total_actual_cummulative:
            if type(total_actual_cummulative[i]) == int:
                actual_cummulative.append(total_actual_cummulative[i])
        
        total_working_days = len(work_days)
        lr_pred = Lr_Predict()
        prediction = lr_pred.simple_prediction(work_days[:len(actual_cummulative)], actual_cummulative, total_working_days, self.START_NO)
        return prediction