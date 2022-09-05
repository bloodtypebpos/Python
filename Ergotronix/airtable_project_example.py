import sqlite3
import os
from airtable import Airtable
from airtable_project import Project, Item
import requests

sonum = 'ET-14073-H'
table = 'airtable'

base_key = "appW9SUX8ihLsY2YV"
api_key = "keyszzdobucJcnVXx"

db_dir = r'C:\Users\Sad_Matt\Desktop\Python\Ergotronix\reports'
fname = os.path.join(db_dir, 'airtabledata.db')
conn = sqlite3.connect(fname)
c = conn.cursor()

project = Project(base_key, api_key, conn, table, sonum)
#project = Project(base_key, api_key, conn, table, "NA")


print(project.customer)
print(project.sonum)
for i in range(0, len(project.codes)):
    code = project.codes[i][0]
    code_items = project.code_items[i]
    complete_code_items = project.completed_code_items[i]
    print(code)
    print(len(code_items))
    print(len(complete_code_items))
    print("=========================================================")


img_data = requests.get(project.image_url).content
fname = os.path.join(db_dir, 'output.png')
with open(fname, 'wb') as handler:
    handler.write(img_data)
