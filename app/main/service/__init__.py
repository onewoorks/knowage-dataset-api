
class CommonMethod:
    def GetWorkingDay(self):
        working_day = ('1', '2', '3', '4', '5-7', '8', '9', '10', '11', '12-14', '15', '16',
                       '17', '18', '19-21', '22', '23', '24', '25', '26-28', '29-30', '31', 'Total')
        return working_day

    def TemplateBuilder(self,report_format_constant):
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