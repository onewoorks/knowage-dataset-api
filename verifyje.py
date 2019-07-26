import pymysql
import json
from datetime import datetime

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

PENDING_PAYMENT_CYCLE = (
        'MONTH PV',
        'ACTUAL PV',
        'PO CANCEL',
        'PV EXPECTED',
        'RANGE OF MONTHS',
        'GRAND TOTAL',
        'BALANCE PV'
    )

def GetMonthName(month_int):
        month_name = ("January","February","March","April","May","June","July","August","September","October","November","December")
        return month_name[month_int-1]

def CylceTable():
        current_month = datetime.now().month
        i = 1
        header = []
        while i <= current_month:
            month = GetMonthName(i)
            header.append(month)
            i += 1
        new_table_headers = []
        for a in PENDING_PAYMENT_CYCLE:
            if a == 'RANGE OF MONTHS':
                for h in header:
                    new_table_headers.append(h.upper())
            new_table_headers.append(a)

        return new_table_headers

print(CylceTable())