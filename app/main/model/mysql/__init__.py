from .. import execute_query

class Common_Query():

    def Get_Latest_WS_Data(self, ws_name):
        query = "SELECT ws_data "
        query += "FROM ws_data "
        query += "WHERE ws_name = '{}' ".format(ws_name)
        query += "AND ws_is_active = 1 "
        query += "ORDER BY ws_id DESC LIMIT 1"
        resp = execute_query(query)
        return resp