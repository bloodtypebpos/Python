import sqlite3
import openpyxl
import os
import datetime
import texttable
import matplotlib.pyplot as plt
from airtable import Airtable


dbdir = r'C:\Users\Matt Tigrett\Desktop'

fname = os.path.join(dbdir, 'airtabledata.db')

conn = sqlite3.connect(fname)
c = conn.cursor()

query = 'SELECT * FROM airtabledata'

crows = c.execute(query)
rows = []
for row in crows:
    rows.append(row)

allofit = len(rows)
codevals = []
codecomps = []

query = 'SELECT DISTINCT CODE FROM airtabledata'
crows = c.execute(query)
codes = []
for row in crows:
    codes.append(row[0])




for code in codes:
    query = 'SELECT * FROM airtabledata WHERE CODE = "' + code +'"'
    crows = c.execute(query)
    rows = []
    for row in crows:
        rows.append(row)
    total = len(rows)
    completes = []
    query = 'SELECT * FROM airtabledata WHERE CODE IS "' + code +'" AND COMPLETE IS NOT NULL'
    crows = c.execute(query)
    for row in crows:
        completes.append(row)
    completed = len(completes)
    codevals.append(total)
    codecomps.append(completed)


tcomp = 0


for i in range(0, len(codes)):
    code = codes[i]
    print(code)
    tcomp = tcomp + codecomps[i]
    pcomp = round(codecomps[i]/codevals[i], 2)
    print(codevals[i])
    print(codecomps[i])
    pcomp = pcomp*100
    print(str(pcomp) + "%")
    print("--------------------------------------------------")

print("=========================================================")
print("TOTAL: " + str(allofit))
print("COMPLETED: " + str(tcomp))
ccomp = round(tcomp/allofit, 2)
ccomp = ccomp*100
print(str(ccomp) + "%")


print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

query = 'SELECT QTY FROM airtabledata WHERE CODE = "Machine"'
crows = c.execute(query)
rows = []
for row in crows:
    rows.append(row[0])

val = 0
for row in rows:
    val = val + int(row)

print(val)

query = 'SELECT QTY FROM airtabledata WHERE CODE = "Machine" AND COMPLETE = "checked"'
crows = c.execute(query)
rows = []
for row in crows:
    rows.append(row[0])

val = 0
for row in rows:
    val = val + int(row)

print(val)
