import pymysql

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
