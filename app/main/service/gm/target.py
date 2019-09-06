from ...model.mysql.government_management import MYSQL_GM_QUERY
from ...service.common import CommonMethod

import pandas as pd 
import json

common_method = CommonMethod()
mysql_query = MYSQL_GM_QUERY()

class GM_Target():
    def Target_Sampling(self):
        target = mysql_query.detail_year_target_ws() 
        return  json.loads(target[0]['ws_data'])

    def Target_Sampling_New(self):
        print('------ collecting sample ------')
        detail_year_target = mysql_query.detail_year_target()
        print('------   end colleting   ------')
        target = pd.DataFrame(detail_year_target)
        
        gm_target = {}
        gm_target['year'] = {"2019": float(target['target_month'].sum())}

        monthly = {}
        month_target = target.groupby('month')['target_month'].sum()
        mt = month_target.to_dict()
        for i in mt:
            monthly[common_method.GetMonthName(i)] = float(mt[i])
        gm_target['monthly'] = monthly

        zone = {}
        zone_target = target.groupby(['zone','month'])['target_month'].sum()
        zt = zone_target.to_dict()
        for i in zt:
            if i[0] not in zone:
                zone_data = {}
                zone_data[common_method.GetMonthName(i[1])] = float(zt[i])
                zone[i[0]] = zone_data
            else:
                zone_data[common_method.GetMonthName(i[1])] = float(zt[i])
        gm_target['zone'] = zone

        zone = {}
        zone_target = target.groupby(['zone','month'])['target_month'].sum()
        zt = zone_target.to_dict()
        for i in zt:
            if i[0] not in zone:
                zone_data = {}
                zone_data[common_method.GetMonthName(i[1])] = float(zt[i])
                zone[i[0]] = zone_data
            else:
                zone_data[i[1]] = float(zt[i])
        gm_target['zone'] = zone

        kementerian = {}
        kementerian_target = target.groupby(['kementerian_name','month'])['target_month'].sum()
        kt = kementerian_target.to_dict()

        for key, value in kt.items():
            kementerian_name = key[0]
            
            if kementerian_name in kementerian:
                month = common_method.GetMonthName(key[1])
                kementerian_data[month] = float(value)
            else:
                kementerian_data = {}
                month = common_method.GetMonthName(key[1])
                kementerian_data[month] = float(value)
                kementerian[kementerian_name] = kementerian_data
        gm_target['kementerian'] = kementerian

        return gm_target
