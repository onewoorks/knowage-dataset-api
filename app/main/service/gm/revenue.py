from ...model.mysql.government_management import MYSQL_GM_QUERY
from ..predictions.linear_regression import Lr_Predict

import json

mysql_query = MYSQL_GM_QUERY()

class GM_Revenue():
    def Revenue_Summary(self):
        data = mysql_query.Get_Latest_WS('GM_REVENUE')
        return json.loads(data[0]['ws_data'])
        
    def Revenue_Pivot(self):
        data = mysql_query.Get_Latest_WS('GM_REVENUE_TARGET_ACTUAL')
        pivot_data = json.loads(data[0]['ws_data'])
        x_value = []
        y_value = []
        scale = 100000
        for d in pivot_data:
            if d['actual_cumulative'] != "":
                x_value.append(d['index'])
                y_value.append(float(d['actual_cumulative'])/scale)

        pred_lr = Lr_Predict()
        predict = pred_lr.simple_prediction_pivot(x_value, y_value, 12)
        
        for p in pivot_data:
            pivot_data[p['index']-1]['predict'] = str(predict[p['index']-1]*scale)
        
        return pivot_data