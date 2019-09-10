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

    def Target_Sampling_Pivotal(self):
        data = self.Target_Sampling()
        pivot_data = {}
        pivot_data['monthly'] = self.Pivot_Construct(data['monthly'])
        pivot_data['monthly_commulative'] = self.Pivot_Commulative_Construct(data['monthly'])
        pivot_data['zone_pivot'] = self.Pivot_Month_Construct(data['zone'])
        pivot_data['kementerian_pivot'] = self.Birt_Construct(data['kementerian'])
    
        return pivot_data
    
    def Pivot_Month_Construct(self, data):
        month = range(12)
        zone_list = []
        for zl in data:
            zone_list.append(zl)

        zone_pivot = []

        for m in month:
            m = m + 1
            content = {}
            content['index'] = m
            content['month'] = common_method.GetMonthName(m) 
            for zm in zone_list:
                content[zm] = str(data[zm][common_method.GetMonthName(m)])
            zone_pivot.append(content)
    
        return  zone_pivot

    def Pivot_Construct(self, data):
        pivot_data = []
        index = 1
        for p in data:
            content = {}
            content['index'] = index
            content['month'] = p
            content['value'] = data[p]
            pivot_data.append(content)
            index += 1
        return pivot_data
    
    def Birt_Construct(self, data):
        month = range(12)
        data_list = []

        header = {}
        header[100] = 'KEMENTERIAN'
        for m in month:
            index = 101 + m
            header[index] = common_method.GetMonthName(m+1) 

        data_list.append(header)

        for kl in data:
            content = {}
            content[100] = kl
            for m in month:
                index = 101 + m
                content[index] = data[kl][common_method.GetMonthName(m+1)]
            data_list.append(content)
        return data_list

    def Pivot_Commulative_Construct(self, data):
        commulate_value = 0
        pivot_data = []
        index = 1
        for p in data:
            content = {}
            commulate_value += float(data[p])
            content['index'] = index
            content['month'] = p
            content['value'] = str(commulate_value)
            pivot_data.append(content)
            index += 1
        return pivot_data


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
