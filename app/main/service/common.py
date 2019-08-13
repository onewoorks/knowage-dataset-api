from ..model import execute_query

class CommonMethod:
    def GetMonthName(self, month_int):
        month_name = ("January","February","March","April","May","June","July","August","September","October","November","December")
        return month_name[month_int-1]

    def GetWorkingDay(self):
        q = "SELECT DAY(DATE) as day, category FROM ep_yearly_calendar WHERE YEAR(DATE) = YEAR(NOW()) AND MONTH(DATE) = MONTH(NOW())"
        result = execute_query(q)
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
        working_day.append("TOTAL")
        return working_day

    def TemplateBuilder(self, report_format_constant):
            data_out = []
            working_day = self.GetWorkingDay()
            for i in report_format_constant:
                content = {" topic": i}
                no = 97
                for w in working_day:
                    cur_no = chr(no)
                    val = ""
                    if i == 'Date':
                        val = w
                    content[cur_no] = val
                    no = no + 1
                data_out.append(content)
            return data_out
