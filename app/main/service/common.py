from ..model import execute_query, insert_ws_data
from ..model.gm_query import GM_Query

gm_query = GM_Query()

class CommonMethod:
    def GetMonthName(self, month_int):
        month_name = ("January","February","March","April","May","June","July","August","September","October","November","December")
        return month_name[month_int-1]

    def GetWorkingDay(self, max_columns = 30):
        result = gm_query.get_working_days()
        working_day = []
        hold_day = "0"
        last_true = ""
        active_incr = True
        for i in result:
            if i['category'] == "WORKING DAY":
                if active_incr == False:
                    to = "{}-{}".format(str(last_true), str(hold_day))
                    if len(working_day) > 0:
                        del working_day[-1]
                        working_day.append(to)
                active_incr = True
                hold_day = str(i['day'])
                working_day.append(hold_day)
            else:
                active_incr = False
                if len(working_day) > 0:
                    last_true = working_day[-1]
                hold_day = str(i['day'])
        total_working_day = len(working_day)+1
        while total_working_day <= max_columns:
            working_day.append("null-{}".format(total_working_day))
            total_working_day += 1
        return working_day

    def TemplateBuilder(self, report_format_constant, dataset = {}):
        data_out = []
        working_day = self.GetWorkingDay()
        for i in report_format_constant:
            content = {" topic": i}
            no = 100
            for w in working_day:
                if i == 'Date':
                    val = w
                else:
                    val = 0
                content[no] = val
                no = no + 1
            data_out.append(content)
        return data_out
    
    def TemplateBuilderData(self, start_column, dataset = {}, number_format = "clean", skipped = "Date"):
        data_out = []
        data_out.append(dataset[0])
        for i in dataset[1:]:  
            formatted_data = {}
            for v in i:
                value = i[v]
                if int(v) >= start_column:
                    if str(i[v]) != "":
                        value = format(int(i[v]),',d')
                formatted_data[v] = value
            data_out.append(formatted_data)
        return data_out

    def DictToJson(self, data):
        final = {}
        for i in data:
            final[i] = float(data[i])
        return final