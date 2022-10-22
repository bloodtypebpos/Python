import os
import airtable_project
from airtable import Airtable
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches

base_key = "appW9SUX8ihLsY2YV"
api_key = "keyszzdobucJcnVXx"
dbdir = r'C:\Users\Sad_Matt\Desktop\Python\Ergotronix\reports'
fname = os.path.join(dbdir, 'partSort.db')

weekday_hours = [['8:00:00', '15:00:00'],
                 ['8:00:00', '15:00:00'],
                 ['8:00:00', '15:00:00'],
                 ['8:00:00', '15:00:00'],
                 ['8:00:00', '15:00:00'],
                 ['10:00:00', '15:00:00'],
                 ['10:00:00', '15:00:00'],
                 ]


class Sub_Assembly:
    def __init__(self, sub_assembly, time_0):
        self.sub_assembly = sub_assembly
        self.time_0 = time_0
        self.time_1 = time_0
        self.time_bool = True


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


def get_items(tab, view):
    airtable = Airtable(base_key, tab, api_key)
    records = airtable.get_all(view=view)
    fields = set()
    for record in records:
        for field in list(record['fields'].keys()):
            fields.add(field)
    fields = list(fields)
    rows = []
    for record in records:
        row = []
        for field in fields:
            try:
                row.append(record['fields'][field])
            except:
                row.append('NA')
        rows.append(row)
    items = airtable_project.Project4(fields, rows)
    items = [item for item in items.items]
    return [fields, items]


def print_items(fields, items):
    for item in items:
        for field in fields:
            print(f'{field}: {getattr(item, field)}')
        print("================================================")


def get_compared_lists(items1, items2, field1, field2):
    items1_arr = []
    items2_arr = []
    for item in items1[1]:
        if getattr(item, field1) not in items1_arr:
            items1_arr.append(getattr(item, field1))
    for item in items2[1]:
        if getattr(item, field2) not in items2_arr:
            items2_arr.append(getattr(item, field2))
    return items1_arr, items2_arr


def set_item_dates(items, field, new_field):
    for item in items:
        date_str = getattr(item, field)
        try:
            if getattr(item, field) != 'NA':
                date_str = getattr(item, field)
                date_str = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                setattr(item, new_field, date_str)
            else:
                setattr(item, new_field, datetime.datetime.strptime('2022-12-30', '%Y-%m-%d'))
        except:
            setattr(item, new_field, datetime.datetime.strptime('2022-12-30', '%Y-%m-%d'))


def set_item_priority(items):
    for item in items:
        try:
            if item.Priority == "NA":
                item.Priority = 0
            else:
                item.Priority = int(item.Priority)
        except:
            setattr(item, 'Priority', 0)


machine_date_1 = fix_machine_dates_start(datetime.datetime.now())  # VMX30
machine_date_2 = fix_machine_dates_start(datetime.datetime.now())  # VM30

e_items = get_items('Procurement and Fabrication', 'Engineering')
e_items = [e_items[0], [item for item in e_items[1] if item.Complete != 1]]
o_items = get_items('Order Status', 'Grid view')
e_sonums, o_sonums = get_compared_lists(e_items, o_items, 'Reference No', 'SO No')
o_items = [o_items[0], [item for item in o_items[1] if getattr(item, 'SO No') in e_sonums]]
set_item_dates(o_items[1], 'Ship By', 'Ship_Date')
set_item_priority(o_items[1])
o_items[1].sort(key=lambda itm: (-itm.Priority, itm.Ship_Date))

#  Weld / Machine / Order / Inventory (wmoi) Items
#  We're going to divide all the engineering items (e_items) by these groups
wld_items = []
mac_items = []
ord_items = []
inv_items = []
for item in e_items[1]:
    if 'weld' in getattr(item, 'Notes').lower() or 'weld' in getattr(item, 'Status').lower():
        if getattr(item, 'Code') == 'Machine':
            wld_items.append(item)
        elif getattr(item, 'Code') == 'Order':
            ord_items.append(item)
    elif getattr(item, 'Code') == 'Machine':
        mac_items.append(item)
    elif getattr(item, 'Code') == 'Order':
        ord_items.append(item)
    elif getattr(item, 'Code') == 'Inventory':
        inv_items.append(item)
    else:
        pass

#  New method for getting sub assembly names, items from all engineering items etc. Parsing the projects
#  Note: every item in o_items[1] is a project
for item in o_items[1]:
    subs = []
    itms = [itm for itm in e_items[1] if getattr(itm, 'Reference No') == getattr(item, 'SO No')]
    for itm in itms:
        if getattr(itm, 'Sub Assembly') not in subs:
            subs.append(getattr(itm, 'Sub Assembly'))
    setattr(item, 'items', itms)
    setattr(item, 'subs', subs)
    sub_assemblies = []
    for sub in subs:
        sub_assemblies.append(Sub_Assembly(sub, machine_date_2))
    setattr(item, 'sub_assemblies', sub_assemblies)

#  Handle the welds first - have to run through projects twice for this reason
#  Each o_item[1] is a project
#  1) Get the project info
#  2) Get the Sub-Assemblies
#  3) Run through welds items
#  4) Move the machine_2 times only (all welds on machine_2)
#  ---------------------------
#  1) Ger the project info
#  2) Get the Sub-Assemblies
#  3) Run through machine items
#  4) Move the machine_x times (whichever is open earlier, move that machine)

for project in o_items[1]:
    sonum = getattr(project, 'SO No')
    weld_parts = [item for item in wld_items if getattr(item, 'Reference No') == sonum]
    for sub in project.subs:
        for weld_part in weld_parts:
            if getattr(weld_part, 'Sub Assembly') == sub:
                sub_assembly = next(item for item in project.sub_assemblies if item.sub_assembly == sub)
                if sub_assembly.time_bool:
                    setattr(sub_assembly, 'time_0', machine_date_2)
                    setattr(sub_assembly, 'time_1', machine_date_2)
                    setattr(sub_assembly, 'time_bool', False)
                machine_date_2 = move_machine_time(machine_date_2, 2)
                setattr(sub_assembly, 'time_1', machine_date_2)

for project in o_items[1]:
    sonum = getattr(project, 'SO No')
    mac_parts = [item for item in mac_items if getattr(item, 'Reference No') == sonum]
    for sub in project.subs:
        for mac_part in mac_parts:
            if getattr(mac_part, 'Sub Assembly') == sub:
                sub_assembly = next(item for item in project.sub_assemblies if item.sub_assembly == sub)
                if sub_assembly.time_bool:
                    if machine_date_1 < machine_date_2:
                        setattr(sub_assembly, 'time_0', machine_date_1)
                        setattr(sub_assembly, 'time_1', machine_date_1)
                        setattr(sub_assembly, 'time_bool', False)
                    else:
                        setattr(sub_assembly, 'time_0', machine_date_2)
                        setattr(sub_assembly, 'time_1', machine_date_2)
                        setattr(sub_assembly, 'time_bool', False)
                if machine_date_1 < machine_date_2:
                    machine_date_1 = move_machine_time(machine_date_1, 2)
                    setattr(sub_assembly, 'time_1', machine_date_1)
                else:
                    machine_date_2 = move_machine_time(machine_date_2, 2)
                    setattr(sub_assembly, 'time_1', machine_date_2)

for project in o_items[1]:
    sonum = getattr(project, 'SO No')
    weld_parts = [item for item in wld_items if getattr(item, 'Reference No') == sonum]
    ord_parts = [item for item in ord_items if getattr(item, 'Reference No') == sonum]
    for sub in project.subs:
        for weld_part in weld_parts:
            if getattr(weld_part, 'Sub Assembly') == sub:
                sub_assembly = next(item for item in project.sub_assemblies if item.sub_assembly == sub)
                if not sub_assembly.time_bool:
                    time_1 = getattr(sub_assembly, 'time_1')
                    time_1 = time_1 + datetime.timedelta(days=10)
                    setattr(sub_assembly, 'time_1', time_1)
                    setattr(sub_assembly, 'time_bool', True)
        for ord_part in ord_parts:
            if ord_part.ETA != 'NA':
                time_1 = datetime.datetime.strptime(ord_part.ETA, '%Y-%m-%d')
                if getattr(ord_part, 'Sub Assembly') == sub:
                    sub_assembly = next(item for item in project.sub_assemblies if item.sub_assembly == sub)
                    if time_1 > sub_assembly.time_1:
                        setattr(sub_assembly, 'time_1', time_1)

early_date = datetime.datetime.strptime('2100-01-01', '%Y-%m-%d')
late_date = datetime.datetime.strptime('2020-01-01', '%Y-%m-%d')
for project in o_items[1]:
    for sub_assembly in project.sub_assemblies:
        if sub_assembly.time_0 < early_date:
            early_date = sub_assembly.time_0
        if sub_assembly.time_1 > late_date:
            late_date = sub_assembly.time_1

colors = ['pink', 'blue', 'green', 'yellow', 'orange', 'cyan']
fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.xlim([mdates.date2num(early_date) - 1, mdates.date2num(late_date) + 1])

sub_val = 0
sub_space = 0.2
pval = 0
legend = []
print(o_items[0])
for project in o_items[1]:
    print(getattr(project, 'Customer Name'))
    print(getattr(project, 'Ship By'))
    print("-- -- -- -- -- -- -- -- ")
    for sub_assembly in project.sub_assemblies:
        x_0 = mdates.date2num(sub_assembly.time_0)
        x_1 = mdates.date2num(sub_assembly.time_1)
        y_0 = sub_val + sub_space
        y_1 = 1 - 2 * sub_space
        box = patches.Rectangle((x_0, y_0),
                                x_1 - x_0,
                                y_1, color=colors[pval % len(colors)])
        sub_val = sub_val + 1
        ax.add_patch(box)
        plt.text(x_0 + 0.125, y_0 + 0.125, sub_assembly.sub_assembly, color='black')
    legend.append(patches.Patch(color=colors[pval % len(colors)], label=getattr(project, 'Customer Name')))
    pval = pval + 1

plt.ylim([-1, sub_val + 1])
plt.legend(handles=legend[::-1])  # [::-1] puts this in reverse order
plt.show()
