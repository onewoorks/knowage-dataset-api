from ...model.mysql.government_management import MYSQL_GM_QUERY

import json

mysql_query = MYSQL_GM_QUERY()

class GM_Revenue():
    def PV_Summary(self):
        data = mysql_query.Get_Latest_WS('GM_REVENUE')
        return json.loads(data[0]['ws_data'])
        