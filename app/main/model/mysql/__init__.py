from .. import execute_query, mysql_insert_query

class Common_Query():

    def update_previous_ws(self, ws_name):
        query = "UPDATE ws_data SET ws_is_active = 0 WHERE ws_name = '{}'".format(ws_name)
        mysql_insert_query(query)

    def Register_New_Ws(self, ws_data):
        self.update_previous_ws(ws_data['ws_name'])
        query = "INSERT INTO ws_data (ws_name, ws_is_active, ws_desc, ws_group, ws_start_execute, ws_end_execute, ws_duration, ws_data, ws_created_at, ws_updated_at, ws_status, ws_error) "
        query += "VALUES ("
        query += "'{}', ".format(ws_data['ws_name'])
        query += "'{}', ".format(ws_data['ws_is_active'])
        query += "'{}', ".format(ws_data['ws_desc'])
        query += "'{}', ".format(ws_data['ws_group'])
        query += "'{}', ".format(ws_data['ws_start_execute'])
        query += "'{}', ".format(ws_data['ws_end_execute'])
        query += "'{}', ".format(ws_data['ws_duration'])
        query += "'{}', ".format(ws_data['ws_data'].replace("'","''"))
        query += "'{}', ".format(ws_data['ws_created_at'])
        query += "'{}', ".format(ws_data['ws_updated_at'])
        query += "'{}', ".format(ws_data['ws_status'])
        query += "'{}'".format(ws_data['ws_error'])
        query += ")"
        mysql_insert_query(query)

    def Get_Latest_WS_Data(self, ws_name):
        query = "SELECT ws_data "
        query += "FROM ws_data "
        query += "WHERE ws_name = '{}' ".format(ws_name)
        query += "AND ws_is_active = 1 "
        query += "ORDER BY ws_id DESC LIMIT 1"
        resp = execute_query(query)
        return resp