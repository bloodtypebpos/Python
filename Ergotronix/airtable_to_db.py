import sqlite3
import os
from airtable import Airtable

base_key = "appW9SUX8ihLsY2YV"
api_key = "keyszzdobucJcnVXx"

dbdir = r'C:\Users\Sad_Matt\Desktop\Python\Ergotronix\reports'
fname = os.path.join(dbdir, 'airtabledata.db')
conn = sqlite3.connect(fname)
c = conn.cursor()


def make_air_table(fields, table_name, ints, floats, ignores):
    for i in range(0, len(fields)):
        if '"' in fields[i]:
            fields[i].replace('"', '``')
        if "'" in fields[i]:
            fields[i].replace("'", '`')
    c.execute('DROP TABLE IF EXISTS "' + table_name + '"')
    query = 'CREATE TABLE "' + table_name + '"(id INTEGER PRIMARY KEY,'
    for field in fields:
        if field in ints:
            query = query + ' "' + field + '" INTEGER,'
        elif field in floats:
            query = query + ' "' + field + '" REAL,'
        elif field in ignores:
            if field == 'Attachments':
                query = query + ' "' + field + '" TEXT,'
            else:
                pass
        else:
            query = query + ' "' + field + '" TEXT,'
    query = query[:-1] + ')'
    print(query)
    print(tuple(fields))
    c.execute(query)
    conn.commit()


def fill_air_table(fields, table_name, recs, ints, floats, ignores):
    for record in recs:
        query = 'INSERT INTO "' + table_name + '"('
        for def_i in range(0, len(fields)):
            field = fields[def_i]
            if field in ignores:
                if field == 'Attachments':
                    query = query + ' "' + field + '",'
                else:
                    pass
            else:
                query = query + ' "' + field + '",'
        query = query[:-1] + ') VALUES ('
        for def_i in range(0, len(fields)):
            field = fields[def_i]
            if field in ignores:
                if field == 'Attachments':
                    query = query + '?,'
                else:
                    pass
            else:
                query = query + '?,'
        query = query[:-1] + ')'
        c.execute(query, record)
    conn.commit()


airtable = Airtable(base_key, 'Procurement and Fabrication', api_key)
records = airtable.get_all(view='Engineering')

id_val = 0
field_val = 0

fields = set()
for record in records:
    for field in list(record['fields'].keys()):
        fields.add(field)

fields = list(fields)

ints = ['Qty']
floats = ['Price']
ignores = ['Attachments', 'Order Status 2'] # 'Attachments' is giving me a problem... this works
#ignores = ['Order Status 2']

recs = []
for record in records:
    rec = []
    for field in fields:
        try:
            if field in ints:
                rec.append(int(record['fields'][field]))
            elif field in floats:
                rec.append(float(record['fields'][field]))
            elif field in ignores:
                if field == 'Attachments':
                    rec.append(record['fields'][field][0]['url'])
                else:
                    pass
            else:
                rec.append(record['fields'][field])
        except:
            if field in ints:
                rec.append(0)
            elif field in floats:
                rec.append(0.0)
            elif field in ignores:
                if field == 'Attachments':
                    rec.append('NA')
                else:
                    pass
            else:
                rec.append("NA")
    recs.append(rec)



table_name = 'airtable'
make_air_table(fields, table_name, ints, floats, ignores)
fill_air_table(fields, table_name, recs, ints, floats, ignores)
