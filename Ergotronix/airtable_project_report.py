import sqlite3
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from airtable_project import Project, Airtable_DB
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
fname = os.path.join(dbdir, 'partSort.db')
conn = sqlite3.connect(fname)
c = conn.cursor()


def update_airtable_db(tab_name, view_name, table_name, ints, floats, ignores):
    Airtable_DB(base_key, api_key, conn, c, tab_name, view_name, table_name, ints, floats, ignores)


def quick_airtable_update():
    ints = ['Qty']
    floats = ['Price']
    ignores = ['Attachments', 'Order Status 2']
    update_airtable_db('Procurement and Fabrication', 'Engineering', 'airtable', ints, floats, ignores)

    ints = ['Qty']
    floats = ['Price']
    ignores = ['Attachments', 'Order Status 2', 'Procurement and Fabrication']
    update_airtable_db('Order Status', 'Grid view', 'airtable_orders', ints, floats, ignores)

def completion(items, code):
    val1 = len([item for item in items if item.Code == code])
    val2 = len([item for item in items if item.Code == code and item.Complete == '1'])
    cost = sum([item.Qty * item.Price for item in items if item.Code == code])
    parts = sum([item.Qty for item in items if item.Code == code])
    try:
        val3 = round(100 * (val2 / val1), 2)
    except:
        val3 = 0
    print(str(val3) + "% Completed")
    print("Number of Items: " + str(val1))
    print("Number of Completed Items: " + str(val2))
    print("Number of Items Left: " + (str(val1 - val2)))
    try:
        print("   AVG Cost Per Item: $" + str(round(cost/val1, 2)))
        print("   AVG Cost Per Part: $" + str(round(cost/parts, 2)))
    except:
        pass

def report(project):
    items = project.items
    print(" ")
    print("                               " + project.customer)
    print(sonum)
    print("TOTAL COST: $" + str(round(sum([item.Qty * item.Price for item in items]), 2)))
    print("Number of rows: " + str(len(items)))
    val1 = len(items)
    val2 = sum([1 for item in items if item.Complete == '1'])
    try:
        val3 = round(100 * (val2 / val1), 2)
    except:
        val3 = 0
    print(str(val3) + "% Completed")
    print("- - - - - - - - - - - - - - - - - - - - - - -")
    print("       MACHINED PARTS")
    print("Number of Machined Rows: " + str(len([item for item in items if item.Code == 'Machine'])))
    print("Number of Machined Parts: " + str(sum([item.Qty for item in items if item.Code == 'Machine'])))
    print("Cost of Machined Parts: $" + str(
        round(sum([item.Qty * item.Price for item in items if item.Code == 'Machine']), 2)))
    print("COMPLETION: ")
    completion(items, 'Machine')
    print("- - - - - - - - - - - - - - - - - - - - -")
    print("       ORDERED PARTS")
    print("Number of Order Rows: " + str(len([item for item in items if item.Code == 'Order'])))
    print("Number of Order Parts: " + str(sum([item.Qty for item in items if item.Code == 'Order'])))
    print("Cost of Order Parts: $" + str(
        round(sum([item.Qty * item.Price for item in items if item.Code == 'Order']), 2)))
    print("COMPLETION: ")
    completion(items, 'Order')
    print("- - - - - - - - - - - - - - - - - - - - -")
    print("       INVENTORY PARTS")
    print("Number of Inventory Rows: " + str(len([item for item in items if item.Code == 'Inventory'])))
    print("Number of Inventory Parts: " + str(sum([item.Qty for item in items if item.Code == 'Inventory'])))
    print("Cost of Inventory Parts: $" + str(
        round(sum([item.Qty * item.Price for item in items if item.Code == 'Inventory']), 2)))
    print("COMPLETION: ")
    completion(items, 'Inventory')
    print("- - - - - - - - - - - - - - - - - - - - -")
    print("       HARDWARE")
    print("Number of Hardware Rows: " + str(len([item for item in items if item.Code == 'Hardware'])))
    print("Cost of Hardware: $" + str(
        round(sum([item.Qty * item.Price for item in items if item.Code == 'Hardware']), 2)))
    print("==================================================================================")

def full_report():
    sonums = []
    crows = c.execute('SELECT DISTINCT "Reference No" FROM airtable')
    for row in crows:
        sonums.append(row[0])
    print("==================================================================================")
    projects = []
    for sonum in sonums:
        project = Project(base_key, api_key, conn, table, sonum)
        report(project)
    print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    projects = Project(base_key, api_key, conn, table, "NA")
    report(projects)


def make_packet(sonum):
    project_dir = os.path.join(imdir, sonum)
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
        print(f'Made: {project_dir}')
    files = os.listdir(project_dir)
    project = Project(base_key, api_key, conn, table, sonum)
    items = project.items
    items = [item for item in items if item.Code == 'Machine' or item.Status == 'Machine']
    items = [item for item in items if item.Complete != '1']
    items = [item for item in items if '.pdf' in item.Attachments]
    subs = []
    for item in items:
        if getattr(item, 'Sub Assembly') not in subs:
            subs.append(getattr(item, 'Sub Assembly'))
    n = 0
    packets = []
    sub_pdfs = []
    for sub in subs:
        pdfs = []
        sitems = [item for item in items if getattr(item, 'Sub Assembly') == sub]
        sitems = sorted(sitems, key=lambda x: x.id)
        merger = PdfMerger()
        for item in sitems:
            url = item.Attachments
            fname = os.path.join(project_dir, url.split('/')[-1])
            img_data = requests.get(url).content
            with open(fname, 'wb') as handler:
                handler.write(img_data)
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.drawString(35, 65, project.customer)
            can.drawString(35, 55, project.quote)
            can.drawString(35, 45, project.sonum)
            can.drawString(35, 35, sub)
            can.drawString(35, 565, "QTY: " + str(item.Qty))
            can.drawString(35, 555, "PART: " + str(item.Part))
            can.save()
            # move to the beginning of the StringIO buffer
            packet.seek(0)
            # create a new PDF with Reportlab
            new_pdf = PdfFileReader(packet)
            # read your existing PDF
            existing_pdf = PdfFileReader(open(fname, "rb"))
            output = PdfFileWriter()
            # add the "watermark" (which is the new pdf) on the existing page
            page = existing_pdf.getPage(0)
            page.mergePage(new_pdf.getPage(0))
            output.addPage(page)
            fname = os.path.join(project_dir, fname.split(".pdf")[0] + '_mod.pdf')
            outputStream = open(fname, "wb")
            output.write(outputStream)
            outputStream.close()
            merger.append(fname)
        fname = os.path.join(project_dir, sub + '.pdf')
        merger.write(fname)
        merger.close()
        packets.append(fname)
    files = os.listdir(project_dir)
    for file in files:
        fname = os.path.join(project_dir, file)
        if fname not in packets:
            try:
                os.remove(fname)
            except OSError as e:  ## if failed, report it back to the user ##
                print("Error: %s - %s." % (e.filename, e.strerror))


def split_packet(fname):
    inputpdf = PdfFileReader(open(fname, "rb"))
    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        outputpdf = fname.split('.pdf')[0] + '-' + str(i-1) + '.pdf'
        with open(outputpdf, "wb") as outputStream:
            output.write(outputStream)


#quick_airtable_update()
#full_report()


make_packet('ET-14217-TK')


#packet_dir = r'F:\PYTHON SCRIPTS\Support Files\Project Cost Files\ET-14137-K'
#fname = os.path.join(packet_dir, 'ET220310-WELDMENT.pdf')
#split_packet(fname)


#igus = Project(base_key, api_key, conn, 'airtable', "NA")
#igus = [item for item in igus.items if item.Vendor.lower() == 'igus' or 'igus' in item.Description.lower()]
#for item in igus:
#    print(f'{str(item.Qty)}     {item.Part}      {item.Description}     {item.Customer}')


def uh():
    items = Project(base_key, api_key, conn, 'airtable', 'ET-14073-H')
    items = [item for item in items.items]
    subs = []
    for item in items:
        if getattr(item, 'Sub Assembly') not in subs:
            subs.append(getattr(item, 'Sub Assembly'))

    for sub in subs:
        rows = [item for item in items if getattr(item, 'Sub Assembly') == sub]
        print(f'         {sub}')
        cost = sum([item.Qty*item.Price for item in rows])
        print(f'${str(cost)}')
        print("-------------------------------------------------")


    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    cost = sum([item.Qty*item.Price for item in items])
    print(cost)
