import requests
import os
import datetime
from airtable import Airtable
from PIL import Image, ImageDraw
import PIL_tools
import airtable_project
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus.tables import Table, TableStyle
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches



dbdir = r'C:\Users\Sad_Matt\Desktop\Python\Ergotronix\reports'
base_key = "appW9SUX8ihLsY2YV"
api_key = "keyszzdobucJcnVXx"


class SubDatesData:
    def __init__(self, sub, time_0):
        self.sub = sub
        self.time_0 = time_0
        self.time_1 = time_0
        self.time_bool = True


def get_items(base_key, api_key, table_name, view):
    items = Airtable(base_key, table_name, api_key).get_all(view=view)
    fields = set()
    for item in items:
        for field in list(item['fields'].keys()):
            fields.add(field)
    fields = list(fields)
    rows = []
    for item in items:
        row = []
        for field in fields:
            try:
                row.append(item['fields'][field])
            except:
                row.append("NA")
        rows.append(row)
    items = airtable_project.Project4(fields, rows)
    items = items.items
    return fields, items


def print_items(fields, items):
    for item in items:
        for field in fields:
            print(f'{field}: {getattr(item, field)}')
        print("=======================================")


def column_widths(width_total, columns, rows):
    col_widths = []
    for col in columns:
        col_widths.append(len(col))
    for row in rows:
        for i in range(0, len(col_widths)):
            if len(row[i]) > col_widths[i]:
                col_widths[i] = len(row[i])
    for i in range(0, len(col_widths)):
        col_widths[i] = ((col_widths[i] / sum(col_widths)) * width_total)
    return col_widths


def num2num(old_value, old_min, old_max, new_min, new_max):
    return (((float(old_value) - float(old_min)) * (float(new_max) - float(new_min))) /
            (float(old_max) - float(old_min))) + float(new_min)


def fix_machine_dates_start(some_date):
    global weekday_hours
    begin_time = str(f'{some_date.date()} {weekday_hours[some_date.weekday()][0]}')
    begin_time = datetime.datetime.strptime(begin_time, '%Y-%m-%d %H:%M:%S')
    end_time = str(f'{some_date.date()} {weekday_hours[some_date.weekday()][1]}')
    end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    if some_date > end_time:
        some_date = some_date + datetime.timedelta(days=1)
        some_date = str(f'{some_date.date()} {weekday_hours[some_date.weekday()][0]}')
        some_date = datetime.datetime.strptime(some_date, '%Y-%m-%d %H:%M:%S')
    elif begin_time > some_date:
        some_date = begin_time
    return some_date


def move_machine_time(some_date, some_time):
    # machine_date_1 = move_machine_time(machine_date_1, 1.75) #  What it looks like in use where 1.75 hrs = 60 + 45 min
    global weekday_hours
    hrs = int(some_time)
    mins = int((some_time - hrs) * 60)
    some_date = some_date + datetime.timedelta(hours=hrs)
    some_date = some_date + datetime.timedelta(minutes=mins)
    end_time = str(f'{some_date.date()} {weekday_hours[some_date.weekday()][1]}')
    end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    if some_date > end_time:
        some_time = some_date - end_time
        hrs = int(str(some_time).split(":")[0])
        mins = int(str(some_time).split(":")[1])
        some_date = some_date + datetime.timedelta(days=1)
        some_date = str(f'{some_date.date()} {weekday_hours[some_date.weekday()][0]}')
        some_date = datetime.datetime.strptime(some_date, '%Y-%m-%d %H:%M:%S')
        some_date = some_date + datetime.timedelta(hours=hrs)
        some_date = some_date + datetime.timedelta(minutes=mins)
    return some_date


def make_sales_order(sonum):
    global e_items
    global o_items
    global s_items
    global moi_codes
    global tn_items
    project = [e_item for e_item in e_items if getattr(e_item, 'Reference No') == sonum]
    p_data = next(o_item for o_item in o_items if getattr(o_item, 'SO No') == sonum)
    s_data = next(s_item for s_item in s_items if getattr(s_item, 'SO No') == sonum)
    moi = []
    subs = []
    for project_item in project:
        if getattr(project_item, 'Sub Assembly') not in subs:
            subs.append(getattr(project_item, 'Sub Assembly'))
    subs = sorted(subs)
    sub_assemblies = []
    sub_dates_data = []
    for moi_code in moi_codes:
        moi.append([project_item for project_item in project if getattr(project_item, 'Code') == moi_code])
    for sub in subs:
        sub_assemblies.append([project_item for project_item in project
                               if getattr(project_item, 'Sub Assembly') == sub])
        sub_dates_data.append(SubDatesData(sub, machine_date_2))
    data = []
    info = airtable_project.Item()
    for p_field in p_fields:
        data.append((p_field, getattr(p_data, p_field)))
        setattr(info, p_field, getattr(p_data, p_field))
    for s_field in s_fields:
        setattr(info, s_field, getattr(s_data, s_field))
    try:
        url = next(t_item for t_item in tn_items if getattr(t_item, 'Reference No' == sonum))
        print(url)
    except:
        url = img_na
    sonum_sales_order = airtable_project.SalesOrder \
        (sonum, project, p_data, s_data, moi, subs, sub_assemblies, data, info, url, sub_dates_data)
    return sonum_sales_order


def make_datetime_date(item, attr):
    if getattr(item, attr) != "NA":
        return datetime.datetime.strptime(getattr(item, attr), '%Y-%m-%d')
    return "NA"

# ##############################################################################
#                       GENERAL VARIABLES
# ##############################################################################

weekday_hours = [['8:00:00', '15:00:00'],
                 ['8:00:00', '15:00:00'],
                 ['8:00:00', '15:00:00'],
                 ['8:00:00', '15:00:00'],
                 ['8:00:00', '15:00:00'],
                 ['10:00:00', '15:00:00'],
                 ['10:00:00', '15:00:00'],
                 ]


datetime_begin = datetime.datetime.today()
#datetime_begin = datetime.datetime.strptime('2022-10-05', '%Y-%m-%d') #  If you wanna specify date

machine_date_1 = fix_machine_dates_start(datetime_begin)  # VMX30
machine_date_2 = fix_machine_dates_start(datetime_begin)  # VM30
finish_date_1 = datetime_begin
weld_date_1 = datetime_begin

img_na = 'https://t3.ftcdn.net/jpg/00/36/94/26/240_F_36942622_9SUXpSuE5JlfxLFKB1jHu5Z07eVIWQ2W.jpg'

# ##############################################################################
#                       PDF SIZE INFO
# ##############################################################################

pagesize = (792.0, 612.0)
page_width = pagesize[0]
page_height = pagesize[1]
pad = 15
page_width_half = (page_width) / 2
page_height_half = (page_height) / 2

# ##############################################################################
#                       FULL AIRTABLE INFO FOR ALL SONUMS
# ##############################################################################
e_fields, e_items = get_items(base_key, api_key, 'Procurement and Fabrication', 'Engineering')
o_fields, o_items = get_items(base_key, api_key, 'Order Status', 'Grid view')
s_fields, s_items = get_items(base_key, api_key, 'Approval Drawings and Packets', 'Engineering')
tn_fields, tn_items = get_items(base_key, api_key, 'Procurement and Fabrication', 'Engineering')
p_fields = ['Quote No',
            'Customer Name',
            'Ship To Name',
            'SO No',
            'PO No',
            'SO Date',
            'Ship By',
            'ETA'
            ]
s_fields = ['Sent',
            'Date Sent',
            'Rcvd',
            'Date Rcvd',
            'Packet',
            'Packet Date'
            ]
moi_codes = ['Weld',
             'Finish',
             'Machine',
             'Order',
             'Inventory'
             ]

e_items = [item for item in e_items if getattr(item, 'Complete') == 'NA']
tn_items = [item for item in tn_items if getattr(item, 'Sub Assembly') == '0-IMAGE']
tn_item = next(item for item in tn_items if getattr(item, 'Reference No') == 'ET-14217-TK')
print(getattr(tn_items[0], 'Attachments')[0]['url'])
for item in e_items:
    setattr(item, 'start_date', datetime.datetime.now())
    setattr(item, 'end_date', datetime.datetime.now())

e_fields.extend(['start_date', 'end_date'])

# ##############################################################################
#                       GET ALL SONUMS - SORT BY PRIORITY, SHIP BY, SONUM
# ##############################################################################

# pr_fields = ['SO No', 'ETA', 'SO Date', 'Ship By', 'Customer Name', 'Ship To Name', 'Priority']
for item in o_items:
    if getattr(item, 'Priority') == "NA": setattr(item, 'Priority', 0)
    if getattr(item, 'Ship By') == "NA": setattr(item, 'Ship By', '2100-1-1')
o_items = sorted(o_items, key=lambda item: (-getattr(item, 'Priority'),
                                            datetime.datetime.strptime(getattr(item, 'Ship By'), '%Y-%m-%d'),
                                            getattr(item, 'SO No')))
o_sonums = [getattr(item, 'SO No') for item in o_items]
e_sonums = []
for item in e_items:
    if getattr(item, 'Reference No') not in e_sonums: e_sonums.append(getattr(item, 'Reference No'))

# ##############################################################################
#                       MAKE SALES ORDER OBJECTS AND FILL INTO PROJECTS
# ##############################################################################
skinny = ['Sub Assembly',
          'Code',
          'Part',
          'Qty',
          'Description',
          'start_date',
          'end_date']
sales_orders = [make_sales_order(sonum) for sonum in o_sonums if sonum in e_sonums]

# ##################################################################################
#           1: THE WELD PARTS THAT NEED TO BE MACHINED
#           Note: Loop through all Sales Orders to get all weld parts up to front

for sales_order in sales_orders:
    for sub_assembly in sales_order.sub_assemblies:
        sub = next(getattr(item, 'Sub Assembly') for item in sub_assembly)
        welds = [item for item in sub_assembly
                 if getattr(item, 'Code') == 'Weld' and 'weldment' not in getattr(item, 'Notes').lower()]
        sub_dates = next(item for item in sales_order.sub_dates_data if getattr(item, 'sub') == sub)
        for weld in welds:
            if sub_dates.time_bool:
                sub_dates.time_0 = machine_date_2
                sub_dates.time_1 = machine_date_2
                sub_dates.time_bool = False
            weld.start_date = machine_date_2
            machine_date_2 = move_machine_time(machine_date_2, 2)
            weld.end_date = machine_date_2
        sub_dates.time_1 = machine_date_2

# ##################################################################################
#           2: THE WELDMENTS AND PARTS THAT NEED TO BE WELDED/FINISHED (PAINT ETC)
#           Note: Might need to rethink how the weldment dates are tracked...
#           Note: Again, loop through all Sales Orders to get parts to welding/painting
weldments = 0
finishes = 0
for sales_order in sales_orders:
    welds = [item for item in sales_order.project
             if 'weldment' in getattr(item, 'Notes').lower()
             and getattr(item, 'Code') == 'Weld']
    fins = [item for item in sales_order.project
            if getattr(item, 'Code') == 'Finish']
    welds = len(welds) + 3
    fins = len(fins) + 4
    if welds > 3:
        weld_date_1 = max([weld_date.time_1 for weld_date in sales_order.sub_dates_data]) + \
                      datetime.timedelta(days=welds)
        for sub_assembly in sales_order.sub_assemblies:
            sub = next(getattr(item, 'Sub Assembly') for item in sub_assembly)
            sub_dates = next(item for item in sales_order.sub_dates_data if getattr(item, 'sub') == sub)
            sub_dates.time_1 = weld_date_1

    if fins > 4:
        finish_date_1 = max(finish_date_1, weld_date_1) + \
                      datetime.timedelta(days=fins)
        for sub_assembly in sales_order.sub_assemblies:
            sub = next(getattr(item, 'Sub Assembly') for item in sub_assembly)
            sub_dates = next(item for item in sales_order.sub_dates_data if getattr(item, 'sub') == sub)
            sub_dates.time_1 = finish_date_1

# ##################################################################################
#           3: ALL MACHINED PARTS IN EACH ORDERS SUB ASSEMBLIES AND ORDERED PARTS
for sales_order in sales_orders:
    for sub_assembly in sales_order.sub_assemblies:
        sub = next(getattr(item, 'Sub Assembly') for item in sub_assembly)
        mac_parts = [item for item in sub_assembly if getattr(item, 'Code') == 'Machine']
        sub_dates = next(item for item in sales_order.sub_dates_data if getattr(item, 'sub') == sub)
        for mac_part in mac_parts:
            if sub_dates.time_bool:
                if machine_date_1 < machine_date_2:
                    setattr(sub_dates, 'time_0', machine_date_1)
                    setattr(sub_dates, 'time_1', machine_date_1)
                    setattr(sub_dates, 'time_bool', False)
                else:
                    setattr(sub_dates, 'time_0', machine_date_2)
                    setattr(sub_dates, 'time_1', machine_date_2)
                    setattr(sub_dates, 'time_bool', False)
            if machine_date_1 < machine_date_2:
                machine_date_1 = move_machine_time(machine_date_1, 2)
            else:
                machine_date_2 = move_machine_time(machine_date_2, 2)
            if sub_dates.time_1 < machine_date_1:
                sub_dates.time_1 = machine_date_1
            elif sub_dates.time_1 < machine_date_2:
                sub_dates.time_1 = machine_date_2
        for item in sub_assembly:
            if item.ETA != "NA":
                if datetime.datetime.strptime(item.ETA, '%Y-%m-%d') > sub_dates.time_1:
                    sub_dates.time_1 = datetime.datetime.strptime(item.ETA, '%Y-%m-%d')


# ##############################################################################
#                       GANTT CHART FULL
#                       Note: Save the figure as: gantt.png
# ##############################################################################
early_date = datetime.datetime.strptime('2100-01-01', '%Y-%m-%d')
late_date = datetime.datetime.strptime('2020-01-01', '%Y-%m-%d')
for sales_order in sales_orders:
    for sub_assembly in sales_order.sub_assemblies:
        sub = next(getattr(item, 'Sub Assembly') for item in sub_assembly)
        sub_dates = next(item for item in sales_order.sub_dates_data if getattr(item, 'sub') == sub)
        if sub_dates.time_0 < early_date:
            early_date = sub_dates.time_0
        if sub_dates.time_1 > late_date:
            late_date = sub_dates.time_1

sub_colors = ['pink', 'blue', 'green', 'yellow', 'orange', 'cyan']
txt_colors = ['pink', 'blue', 'green', 'yellow', 'orange', 'cyan']
fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.xlim([mdates.date2num(early_date) - 1, mdates.date2num(late_date) + 1])

sub_val = 0
sub_space = 0.2
pval = 0
legend = []
for sales_order in sales_orders:
    for sub_assembly in sales_order.sub_assemblies:
        sub = next(getattr(item, 'Sub Assembly') for item in sub_assembly)
        sub_dates = next(item for item in sales_order.sub_dates_data if getattr(item, 'sub') == sub)
        x_0 = mdates.date2num(sub_dates.time_0)
        x_1 = mdates.date2num(sub_dates.time_1)
        y_0 = sub_val + sub_space
        y_1 = 1 - 2 * sub_space
        box = patches.Rectangle((x_0, y_0),
                                x_1 - x_0,
                                y_1, color=sub_colors[pval % len(sub_colors)])
        sub_val = sub_val + 1
        ax.add_patch(box)
        plt.text(x_0 + 0.125, y_0 + 0.125, sub, color='black')
    legend.append(patches.Patch(color=sub_colors[pval % len(sub_colors)],
                                label=getattr(sales_order.info, 'Customer Name')))
    pval = pval + 1

plt.ylim([-1, sub_val + 1])
plt.legend(handles=legend[::-1])  # [::-1] puts this in reverse order
plt.tight_layout()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_yaxis().set_ticks([])
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.gcf().autofmt_xdate()
figure = plt.gcf()  # get current figure
figure.set_size_inches(12, 8)  # set figure's size manually to your full screen (32x18)
plt.savefig(os.path.join(dbdir, 'gantt.png'), bbox_inches='tight', dpi=300)


# ##############################################################################
#                       PROJECT THUMBNAIL (TOP LEFT IMAGE)
# ##############################################################################
e_sonums = [sonum for sonum in o_sonums if sonum in e_sonums]

#sales_order = next(order for order in sales_orders if 'ET-14181-TK' == getattr(order.info, 'SO No'))

for sales_order in sales_orders:
    info = sales_order.info
    sonum = getattr(info, 'SO No')
    so_date_fields = ['SO Date', 'DWG Sent', 'DWG Signed', 'Production', 'Ship By', 'ETA']
    son_date = make_datetime_date(info, 'SO Date')
    dwg_sent = make_datetime_date(info, 'Date Sent')
    dwg_sign = make_datetime_date(info, 'Date Rcvd')
    pkt_date = make_datetime_date(info, 'Packet Date')
    shp_date = make_datetime_date(info, 'Ship By')
    eta_date = make_datetime_date(info, 'ETA')
    so_dates = [son_date, dwg_sent, dwg_sign, pkt_date, shp_date, eta_date]

    early_date = datetime.datetime.strptime('2100-01-01', '%Y-%m-%d')
    late_date = datetime.datetime.strptime('2020-01-01', '%Y-%m-%d')
    for sub_date in so_dates:
        try:
            if sub_date < early_date:
                early_date = sub_date
            if sub_date > late_date:
                late_date = sub_date
        except:
            pass

    for sub_assembly in sales_order.sub_assemblies:
        sub = next(getattr(item, 'Sub Assembly') for item in sub_assembly)
        sub_date = next(item for item in sales_order.sub_dates_data if getattr(item, 'sub') == sub)
        if sub_date.time_0 < early_date:
            early_date = sub_date.time_0
        if sub_date.time_1 > late_date:
            late_date = sub_date.time_1

    # ##############################################################################
    #                       SALES ORDER HISTORY PLOT
    # ##############################################################################
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    plt.xlim([mdates.date2num(early_date) - 1, mdates.date2num(late_date) + 1])

    sub_val = 1
    sub_space = 0.1
    sub_height = 0.3
    pval = 1
    legend = []
    y_max = len(sales_order.subs) * 0.5
    y_text = 0
    #print("------------------------------------------------------------")
    #print(sonum)
    for i in range(0, len(so_dates)):
        try:
            #print(so_dates[i])
            x_0 = mdates.date2num(so_dates[i]) - 0.1
            x_1 = mdates.date2num(so_dates[i]) + 0.1
            y_0 = 0
            y_1 = y_max
            box = patches.Rectangle((x_0, y_0),
                                    x_1 - x_0,
                                    y_1, color=txt_colors[i % len(txt_colors)])
            ax.add_patch(box)
            try:
                if (mdates.date2num(so_dates[i+1]) - x_0) < \
                        (0.05 * (mdates.date2num(late_date) - mdates.date2num(early_date))):
                    x_0 = x_0 - (0.05 * (mdates.date2num(late_date) - mdates.date2num(early_date)))
            except:
                pass
            if i % 2 == 0:
                plt.text(x_0 + 0.125, y_max + 0.25, so_date_fields[i], color=txt_colors[i % len(txt_colors)])
            else:
                plt.text(x_0 + 0.125, y_max + 0.125, so_date_fields[i], color=txt_colors[i % len(txt_colors)])
        except:
            pass

    for sub_assembly in sales_order.sub_assemblies:
        sub = next(getattr(item, 'Sub Assembly') for item in sub_assembly)
        sub_dates = next(item for item in sales_order.sub_dates_data if getattr(item, 'sub') == sub)
        x_0 = mdates.date2num(sub_dates.time_0)
        x_1 = mdates.date2num(sub_dates.time_1)
        y_0 = sub_val * (sub_space + sub_height)
        y_1 = sub_height
        box = patches.Rectangle((x_0, y_0),
                                x_1 - x_0,
                                y_1, color=sub_colors[pval % len(sub_colors)])
        sub_val = sub_val + 1
        ax.add_patch(box)
        plt.text(x_0 + 0.125, y_0 + 0.125, sub, color='black')
        legend.append(patches.Patch(color=sub_colors[pval % len(sub_colors)], label=sub))
        pval = pval + 1

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_yaxis().set_ticks([])
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    plt.gcf().autofmt_xdate()
    plt.ylim([0, y_max + 1])
    plt.tight_layout()
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(12, 3)  # set figure's size manually to your full screen (32x18)
    plt.savefig(os.path.join(dbdir, f'hist_{sonum}.png'), bbox_inches='tight', dpi=300)

    moi_info = []
    moi_fields = []




    # ##############################################################################
    #                       PROJECT THUMBNAIL (TOP LEFT IMAGE)
    # ##############################################################################
    url = sales_order.url
    print(url)
    tn = Image.open(requests.get(url, stream=True).raw)
    tn = PIL_tools.crop_img(tn, (255, 255, 255))
    scale_x = page_width_half / tn.size[0]
    scale_y = page_height_half / tn.size[1]
    if scale_x < scale_y:
        tn = PIL_tools.scale_img(tn, scale_x)
    else:
        tn = PIL_tools.scale_img(tn, scale_y)
    tn.save(os.path.join(dbdir, 'tn.png'))

    # ##############################################################################
    #                       TIMELINE (BOTTOM)
    # ##############################################################################

    time_x_width = int(pagesize[0]) - 2 * pad
    time_y_height = int(page_height_half) - 3 * pad
    #x_inch = int(time_x_width / 11)
    #time_img = Image.new("RGB", (time_x_width, time_y_width), 'white')
    #time_img1 = ImageDraw.Draw(time_img)

    # ##############################################################################
    #                       CREATING THE PDF
    # ##############################################################################
    fname = os.path.join(dbdir, f'{sonum}.pdf')
    # c = canvas.Canvas(fname, pagesize=letter)  # original
    c = canvas.Canvas(fname, pagesize=pagesize)  # letter = (612.0, 792.0) so maybe this is landscape?
    # c.drawImage(os.path.join(dbdir, 'tn.png'), x_left, y_bottom, x_width, y_height)  # gist of image placement
    c.drawImage(os.path.join(dbdir, 'tn.png'), pad, pagesize[1] - tn.size[1] - pad, tn.size[0], tn.size[1])
    c.drawImage(os.path.join(dbdir, f'hist_{sonum}.png'), pad, pad, time_x_width, time_y_height)
    # data = [(1, 2), (3, "This is just a test")]
    data = sales_order.data
    table = Table(data)  # , colWidths=page_width_half / 3, rowHeights=10)
    table.setStyle(TableStyle([('ALIGN', (0, 0), (1, len(data)), 'LEFT'),
                               ('VALIGN', (0, 0), (1, len(data)), 'MIDDLE'),
                               ('TEXTCOLOR', (0, 0), (1, len(data)), colors.black),
                               ('INNERGRID', (0, 0), (1, len(data)), 0.25, colors.black),
                               ('BOX', (0, 0), (1, len(data)), 0.25, colors.black)
                               ]))
    table.wrapOn(c, 100, 100)
    table.drawOn(c, page_width_half + 2 * pad, page_height - len(data) * 18 - 20)
    #c.showPage()
    c.save()

