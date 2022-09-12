import sqlite3
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from airtable_project import Project
import matplotlib.pyplot as plt
import math
import requests
from PyPDF2 import PdfMerger, PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

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
customer = project.customer

n = 1
subs = []
subnums = []
sub_qtys = []
for subassembly in subassemblies:
    sub = getattr(subassembly[0], "Sub Assembly")
    sub_items = sorted(subassembly, key=lambda x: x.id)
    sub_qty = []
    subnum = []
    subs.append(sub)
    for item in sub_items:
        try:
            print(item.Code)
            print(item.Part)
            url = item.Attachments
            print(url)
            print(item.Qty)
            sub_qty.append(str(item.Qty))
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
    sub_qtys.append(sub_qty)
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

def original_packets():
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


def works():
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(35, 45, "Advanced Airfoil")
    can.drawString(35, 35, "1-BASE BOTTOM")
    can.drawString(35, 565, "QTY: " + str(20))
    can.save()
    #move to the beginning of the StringIO buffer
    packet.seek(0)
    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    fname = os.path.join(imdir, '1.pdf')
    existing_pdf = PdfFileReader(open(fname, "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    fname = os.path.join(imdir, '1-test.pdf')
    outputStream = open(fname, "wb")
    output.write(outputStream)
    outputStream.close()

for i in range(0, len(pdfs_all)):
    pdfs = pdfs_all[i]
    sub = subs[i]
    sub_qty = sub_qtys[i]
    print(sub)
    print(pdfs)
    fname = os.path.join(imdir, sub + '.pdf')
    print(fname)
    merger = PdfMerger()
    for j in range(0, len(pdfs)):
        pdf = pdfs[j]
        qty = sub_qty[j]
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawString(35, 45, project.customer)
        can.drawString(35, 35, sub)
        can.drawString(35, 565, "QTY: " + qty)
        can.save()
        # move to the beginning of the StringIO buffer
        packet.seek(0)
        # create a new PDF with Reportlab
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(open(pdf, "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # finally, write "output" to a real file
        #fname = os.path.join(imdir, '1-test.pdf')
        fname = os.path.join(imdir, pdf.split(".pdf")[0] + '_mod.pdf')
        outputStream = open(fname, "wb")
        output.write(outputStream)
        outputStream.close()
        merger.append(fname)

    fname = os.path.join(imdir, sub + '.pdf')
    merger.write(fname)
    merger.close()



