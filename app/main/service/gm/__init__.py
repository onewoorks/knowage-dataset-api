from ...model.mysql.government_management import MYSQL_GM_QUERY

class GM_Lovs:

    def available_fulfilment_year(self):
        fulfilment_years = MYSQL_GM_QUERY().list_of_available_fulfilment_year()
        years = []
        for y in reversed(fulfilment_years):
            year = y['Tables_in_cdccms (ep_fulfilment_dtl_%)'].split('_')
            years.append(year[-1])
        return years