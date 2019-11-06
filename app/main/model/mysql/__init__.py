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

    def register_archived_ws(self, ws_data, year):
        self.update_previous_ws(ws_data['ws_name'])
        query = "INSERT INTO ws_data_archived (ws_name, archived_year, ws_is_active, ws_desc, ws_group, ws_start_execute, ws_end_execute, ws_duration, ws_data, ws_created_at, ws_updated_at, ws_status, ws_error) "
        query += "VALUES ("
        query += "'{}', ".format(ws_data['ws_name'])
        query += "'{}', ".format(year)
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

    def get_latest_ws_data(self, ws_name):
        query = "SELECT ws_data "
        query += "FROM ws_data "
        query += "WHERE ws_name = `{}` ".format(ws_name)
        query += "AND ws_is_active = 1 "
        query += "ORDER BY ws_id DESC LIMIT 1 ;"
        resp = execute_query(query)
        return resp

    def get_archived_ws_dataset(self, ws_name, year):
        query = "SELECT ws_data "
        query += "FROM ws_data_archived "
        query += "WHERE ws_name = '{}' ".format(ws_name)
        query += "AND ws_is_active = 1 AND archived_year = `{}` ".format(year.replace("'",""))
        query += "ORDER BY ws_id DESC LIMIT 1"
        print(query)
        resp = execute_query(query)
        return resp