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

def execute_oracle_query(query):
    connection = cx_Oracle.connect("ngep_cms/ng3p_cms@rac-cluster-scan.eperolehan.com.my:1521/ngepsit")
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor
