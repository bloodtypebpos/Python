import sqlite3
import openpyxl
import os
import datetime
import texttable
from airtable import Airtable

base_key = "appW9SUX8ihLsY2YV"
api_key = "keyszzdobucJcnVXx"

alphaCols = ['Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']

years = ["2015", "2016", "2017", "2018"]
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']
dbDir = r"C:\Users\Matt Tigrett\Desktop\Desktop Backup"
templateDir = "F:/PYTHON SCRIPTS/Support Files/Forms/Templates"
dwgDir = "E:/Staff/Tigrett, Matt/Drawings"

fname = os.path.join(dbDir, 'partSort.db')
conn = sqlite3.connect(fname)
c = conn.cursor()

dbColumns = ['SONum', 'SODate', 'ShipByDate', 'Customer', 'ShipTo']
airColumns = ['SO No', 'SO Date', 'Ship By', 'Customer Name', 'Ship To Name']


def updateOrderStatus():
    airtable = Airtable(base_key, 'Order Status', api_key)
    records = airtable.get_all()
    airOrders = []
    counter = 2
    for rec in records:
        print(rec['fields'].keys())


#updateOrderStatus()

def getDBorders():
    query = "SELECT * FROM sqlite_master WHERE type='table'"
    query = "SELECT * FROM openOrders"
    query = "PRAGMA table_info(openOrders);"
    query = "SELECT DISTINCT "
    for col in dbColumns:
        query = query + col + ","
    query = query[:-1] + " FROM openOrders"
    print(query)
    rows = []
    crows = c.execute(query)
    for row in crows:
        rows.append(row)
    return rows

updateOrderStatus()
