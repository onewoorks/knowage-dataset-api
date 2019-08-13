from datetime import datetime
from ..common import CommonMethod

common = CommonMethod()

class PendingPaymentCycle:
    PENDING_PAYMENT_CYCLE = (
        'MONTH PV',
        'ACTUAL PV',
        'PO CANCEL',
        'PV EXPECTED',
        'RANGE OF MONTHS',
        'GRAND TOTAL',
        'BALANCE PV'
    )

    SAMPLE_PENDING_PAYMENT = [
        {
            "MONTH PV": "JAN",
            "ACTUAL PV": "1045150285",
            "PO CANCEL": "29708391",
            "PV EXPECTED": "1015441894",
            "JANUARY": "214034397",
            "FEBRUARY": "395917315",
            "MARCH": "198440390",
            "APRIL": "66508112",
            "MAY": "48288505",
            "JUNE": "17091680",
            "JULY": "15110793",
            "GRAND TOTAL": "955391192",
            "BALANCE PV": "60050702"
        },
        {
            "MONTH PV": "FEB",
            "ACTUAL PV": "122160949",
            "PO CANCEL": "35243958",
            "PV EXPECTED": "1086916991",
            "JANUARY": "",
            "GRAND TOTAL": "1026791085",
            "BALANCE PV": "60125906",
            "FEBRUARY": "185082661",
            "MARCH": "573281",
            "APRIL": "143399539",
            "MAY": "82244613",
            "JUNE": "28611163",
            "JULY": "14171177"
        },
        {
            "MONTH PV": "MARCH",
            "ACTUAL PV": 1536076055,
            "PO CANCEL": 43461344,
            "PV EXPECTED": 1492614,
            "JANUARY": "",
            "FEBRUARY": "",
            "MARCH": 506616,
            "APRIL": 581781485,
            "MAY": 174880868,
            "JUNE": 44954742,
            "JULY": 39366982,
            "GRAND TOTAL": 1347600940,
            "BALANCE PV": 145013770
        },
        {
            "MONTH PV": "APRIL",
            "ACTUAL PV": 1487857129,
            "PO CANCEL": 39562940,
            "PV EXPECTED": 1448294189,
            "JANUARY": "",
            "FEBRUARY": "",
            "MARCH": "",
            "APRIL": 541680646,
            "MAY": 519033346,
            "JUNE": 98484203,
            "JULY": 59913284,
            "GRAND TOTAL": 129111480,
            "BALANCE PV": 229182710
        },
        {
            "MONTH PV": "MAY",
            "ACTUAL PV": 1523744310,
            "PO CANCEL": 25324673,
            "PV EXPECTED": 1498419637,
            "JANUARY": "",
            "FEBRUARY": "",
            "MARCH": "",
            "APRIL": "",
            "MAY": 578954746,
            "JUNE": 411456596,
            "JULY": 171039743,
            "GRAND TOTAL": 1161451085,
            "BALANCE PV": 333968552
        },
        {
            "MONTH PV": "JUNE",
            "ACTUAL PV": 1049899436,
            "PO CANCEL": 6767267,
            "PV EXPECTED": 960600197,
            "JANUARY": "",
            "FEBRUARY": "",
            "MARCH": "",
            "APRIL": "",
            "MAY": "",
            "JUNE": 263541788,
            "JULY": 310747718,
            "GRAND TOTAL": 574289506,
            "BALANCE PV": 456449278
        },
        {
            "MONTH PV": "JULY",
            "ACTUAL PV": 967367464,
            "PO CANCEL": 676267,
            "PV EXPECTED": 960600197,
            "JANUARY": "",
            "FEBRUARY": "",
            "MARCH": "",
            "APRIL": "",
            "MAY": "",
            "JUNE": "",
            "JULY": 213246259,
            "GRAND TOTAL": 213246259,
            "BALANCE PV": 747353937
        },
        {
            "MONTH PV": "GRAND TOTAL",
            "ACTUAL PV": 8732255628,
            "PO CANCEL": 199229225,
            "PV EXPECTED": 853026402,
            "JANUARY": 214034397,
            "FEBRUARY": 580999975,
            "MARCH": 1278339185,
            "APRIL": 1333369783,
            "MAY": 1403402079,
            "JUNE": 823595957,
            "JULY": 213246259,
            "GRAND TOTAL": 213246259,
            "BALANCE PV": 747353937
        }
    ]

    def MonthUntilToday(self):
        current_month = datetime.now().month
        i = 1
        header = []
        while i <= current_month:
            month = common.GetMonthName(i)
            header.append(month)
            i += 1
        return header

    def CycleTableTopic(self):
        new_table_headers = []
        for a in self.PENDING_PAYMENT_CYCLE:
            if a.upper() == 'RANGE OF MONTHS':
                for h in self.MonthUntilToday():
                    new_table_headers.append(h.upper())
            else:
                new_table_headers.append(a)
        return new_table_headers

    def TemplateCycleBuilder(self,cycle_data):
        content_body = []
        topic_header = self.ContentKeyValue(self.CycleTableTopic(), True)
        content_body.append(topic_header)
        for i in cycle_data:
            content_in = {}
            no = 97
            for j in self.CycleTableTopic():
                cur_no = chr(no)
                content_in[cur_no] = i[j]
                no += 1
            content_body.append(content_in)
        return content_body

    def ContentKeyValue(self, value_header, value_data=False):
        content = {}
        no = 97
        for w in value_header:
            index = chr(no)
            if value_data == False:
                w = ""
            content[index] = w
            no += 1
        return content


class PendingPaymentCyclePerformanceUpdate(PendingPaymentCycle):
    def PendingPaymentCycle(self,mode):
        print(mode)
        return self.TemplateCycleBuilder(self.SAMPLE_PENDING_PAYMENT)

    def PendingPaymentCycleMilFix(self, returned_data):
        fixData = []
        for i in returned_data[2:]:
            inn = self.ConvertValue(i)
            fixData.append(inn)
        return fixData

    def ConvertValue(self,dict_values):
        clean = {}
        for i in dict_values:
            
            if i != 'a' and dict_values[i] != "":
                print("{} -> {}".format(i,dict_values[i]))
                val = format(dict_values[i],',d')
            else:
                val = dict_values[i]
            clean[i] = val
        return clean



            
