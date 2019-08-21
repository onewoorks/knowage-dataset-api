import pymysql
import cx_Oracle

#mysql connection
DB_HOST = "192.168.62.136"
DB_USER = "epcmsadmin"
DB_PASS = "cDc@2019"
DB_DBASE = "cdccms"


def execute_query(query):
    db = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        db=DB_DBASE,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return data

def mysql_insert_query(query):
    db = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        db=DB_DBASE,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True)
    cursor = db.cursor()
    cursor.execute(query)

def execute_oracle_query(query):
    connection = cx_Oracle.connect("ngep_cms/ng3p_cms@rac-cluster-scan.eperolehan.com.my:1521/ngepsit")
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor
    return data

def insert_ws_data(input):
    update_previous_ws(input['ws_name'])
    query = "INSERT INTO ws_data (ws_name, ws_is_active, ws_desc, ws_group, ws_start_execute, ws_end_execute, ws_duration, ws_data, ws_created_at, ws_updated_at, ws_status, ws_error) "
    query += "VALUES ("
    query += "'{}', ".format(input['ws_name'])
    query += "'{}', ".format(input['ws_is_active'])
    query += "'{}', ".format(input['ws_desc'])
    query += "'{}', ".format(input['ws_group'])
    query += "'{}', ".format(input['ws_start_execute'])
    query += "'{}', ".format(input['ws_end_execute'])
    query += "'{}', ".format(input['ws_duration'])
    query += "'{}', ".format(input['ws_data'])
    query += "'{}', ".format(input['ws_created_at'])
    query += "'{}', ".format(input['ws_updated_at'])
    query += "'{}', ".format(input['ws_status'])
    query += "'{}'".format(input['ws_error'])
    query += ")"
    mysql_insert_query(query)

def update_previous_ws(ws_name):
    query = "UPDATE ws_data SET ws_is_active = 0 WHERE ws_name = '{}'".format(ws_name)
    mysql_insert_query(query)
