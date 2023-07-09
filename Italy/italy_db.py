import os
import sqlite3
import openpyxl

dbdir = r'C:\Users\Matt\Desktop\Italy'
os.chdir(dbdir)

alphas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
conn = sqlite3.connect('italy.db')
c = conn.cursor()
query = f'SELECT title FROM italy GROUP BY title HAVING COUNT(*) > 1'
crows = c.execute(query)
titles = []
for row in crows:
    titles.append(row[0])
fields = []
attrs = []
crows = c.execute(f'PRAGMA table_info(italy)')
for row in crows:
    fields.append(row[1])
for field in fields:
    print(field)
print("-------------------------")
for i in range(6, 20):
    attrs.append(fields[i])
query_attrs = '"title", '
for attr in attrs:
    print(attr)
    query_attrs = query_attrs + f'"{attr}", '
query_attrs = query_attrs[:-2]
print(query_attrs)
print("==========================")
for title in titles:
    try:
        #print(title)
        query = f'SELECT {query_attrs} FROM italy WHERE title = "{title}"'
        crows = c.execute(query)
        rows = []
        for row in crows:
            rows.append(row)
        entry = [title]
        for i in range(0, 14):
            entry.append('')
        for row in rows:
            #print(row)
            for i in range(1, len(row)):
                if row[i] == '1':
                    entry[i] = 1
        #print(entry)
    except:
        print(f'ISSUE WITH: {title}')

    #print("------------------------------------------------------")
