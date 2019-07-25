import pymysql

DB_HOST = "localhost"
DB_USER = "iwang"
DB_PASS = "Root@!234"
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
