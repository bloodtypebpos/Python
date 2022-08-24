import sqlite3
import openpyxl
import os
import datetime
import texttable
import matplotlib.pyplot as plt
from airtable import Airtable

reference_no = 'ET-14073-H'

base_key = "appW9SUX8ihLsY2YV"
api_key = "keyszzdobucJcnVXx"

db_dir = 'F:\PYTHON SCRIPTS\Support Files'
fname = os.path.join(db_dir, 'partSort.db')
conn = sqlite3.connect(fname)
c = conn.cursor()

air_f = ['Reference No',
         'Customer',
         'Part',
         'Description',
         'PO Number',
         'Vendor',
         'Qty',
         'Code',
         'Price',
         'Sub Assembly',
         'Complete']

tab_f = ['sonum',
         'customer',
         'pid',
         'description',
         'ponum',
         'vendor',
         'qty',
         'code',
         'price',
         'sub',
         'complete'
         ]


def make_table():
    c.execute('DROP TABLE IF EXISTS projcost')
    conn.commit()
    c.execute('CREATE TABLE projcost ('
              'id INTEGER PRIMARY KEY, '
              'sonum TEXT, '
              'customer TEXT, '
              'pid TEXT, '
              'description TEXT, '
              'ponum TEXT, '
              'vendor TEXT, '
              'qty INTEGER, '
              'code TEXT, '
              'price REAL, '
              'sub TEXT, '
              'complete TEXT'
              ')')
    conn.commit()


make_table()

airtable = Airtable(base_key, 'Procurement and Fabrication', api_key)
records = airtable.get_all(view='Engineering', formula="FIND('Inventory', {Code})=1")
query = "FIND('" + reference_no + "', {'Reference No'})=1"
# records = airtable.get_all(view="Engineering", formula=query)
records = airtable.get_all(view='Engineering', formula="FIND('" + reference_no + "', {Reference No})=1")

recs = []
for record in records:
    rec = []
    for fld in air_f:
        try:
            rec.append(record['fields'][fld])
        except:
            rec.append(0)
    recs.append(rec)

for rec in recs:
    query = "INSERT INTO projcost(sonum, customer, pid, description, ponum, vendor, qty, code, price, sub, complete) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
    c.execute(query, rec)

conn.commit()

crows = c.execute('SELECT DISTINCT sub FROM projcost')
subs = []
for row in crows:
    subs.append(row[0])

assemblies = []
for sub in subs:
    assembly = []
    crows = c.execute('SELECT qty, price, pid, description, sub, complete FROM projcost WHERE sub = "' + sub + '"')
    for row in crows:
        assembly.append(row)
    assemblies.append(assembly)

costs = []
completes = []
for assembly in assemblies:
    cost = 0
    completion = 0
    for part in assembly:
        price = part[0] * part[1]
        cost = cost + price
        completion = completion + int(part[5])
    completes.append(completion)
    costs.append(cost)

labels = []
tparts = 0
tcost = 0

for i in range(0, len(subs)):
    label = [subs[i] + " | $" + str(round(costs[i], 2)) + " | " + str(len(assemblies[i])) + " | " + str(round(100*(completes[i]/ len(assemblies[i])), 1)) + "%"]
    labels.append(label)
    tparts = tparts + len(assemblies[i])
    tcost = tcost + costs[i]

for label in labels:
    for l in label:
        print(l)
    print("- - - - - - - - - - - - - - - - - - -")

print("Total # unique parts: " + str(tparts))
print("Total Cost: $" + str(round(tcost, 2)))


fig1, ax1 = plt.subplots()
ax1.pie(costs,  labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
