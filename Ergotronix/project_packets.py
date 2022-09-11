import sqlite3
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from airtable_project import Project
import matplotlib.pyplot as plt
import math
import requests
from PyPDF2 import PdfMerger

sonum = 'EH-14076-H'
table = 'airtable'
base_key = "appW9SUX8ihLsY2YV"
api_key = "keyszzdobucJcnVXx"
dbdir = r'F:\PYTHON SCRIPTS\Support Files'
imdir = r'F:\PYTHON SCRIPTS\Support Files\Project Cost Files'
fname = os.path.join(dbdir, 'airtabledata.db')
conn = sqlite3.connect(fname)
c = conn.cursor()
project = Project(base_key, api_key, conn, table, sonum)

subassemblies = project.subassemblies

n = 1
subs = []
subnums = []
for subassembly in subassemblies:
    sub = getattr(subassembly[0], "Sub Assembly")
    sub_items = sorted(subassembly, key=lambda x: x.id)
    subnum = []
    subs.append(sub)
    for item in sub_items:
        try:
            print(item.Code)
            print(item.Part)
            url = item.Attachments
            print(url)
            fname = os.path.join(imdir, str(n) + '.pdf')
            n = n + 1
            img_data = requests.get(url).content
            with open(fname, 'wb') as handler:
                handler.write(img_data)
            print("---------")
            subnum.append(n-1)
        except:
            print("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(item.Code)
            print(item.Part)
            print("-----------")
    subnums.append(subnum)
    print("===========================")


pdfs_all = []
for i in range(0, len(subnums)):
    pdfs = []
    for j in range(0, len(subnums[i])):
        subnum = subnums[i][j]
        fname = os.path.join(imdir, str(subnum) + '.pdf')
        pdfs.append(fname)
    pdfs_all.append(pdfs)


print("=================================================================================")
print("=================================================================================")
print("=================================================================================")

for i in range(0, len(pdfs_all)):
    pdfs = pdfs_all[i]
    sub = subs[i]
    print(sub)
    print(pdfs)
    fname = os.path.join(imdir, sub + '.pdf')
    print(fname)
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(fname)
    merger.close()
