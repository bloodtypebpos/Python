import sqlite3
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from airtable_project import Project
import matplotlib.pyplot as plt
import math
import requests

page_width = 300 * 8
page_height = int(300 * 10.5)

sonum = 'EI-13946-TK'
table = 'airtable'
base_key = "appW9SUX8ihLsY2YV"
api_key = "keyszzdobucJcnVXx"
dbdir = r'F:\PYTHON SCRIPTS\Support Files'
imdir = r'F:\PYTHON SCRIPTS\Support Files\Project Cost Files'
fname = os.path.join(dbdir, 'airtabledata.db')
conn = sqlite3.connect(fname)
c = conn.cursor()

projects_total = Project(base_key, api_key, conn, table, "NA")
project = Project(base_key, api_key, conn, table, sonum)
code_stats_total = [project.code_stats_total[i] for i in project.moi]
code_stats_complete = [project.code_stats_complete[i] for i in project.moi]
moi_codes = project.moi_codes

####################################################################
#      BELOW GETS THE BARS AND TICKS FOR THE MOI FIELDS            #
####################################################################
code_colors = ['red', 'blue', 'green']
code_colors_completed = ['pink', 'cyan', 'lime']
max_rows = max(code_stats_total)
margin_val = 25
img_height = int(page_height / 3)
row_height = int((img_height - 2 * margin_val) / max_rows)
row_width = int((page_width - 4 * margin_val) / len(project.moi))
img = Image.new("RGBA", (page_width, img_height + 100), color="white")
img_draw = ImageDraw.Draw(img)
font_path = r'C:\Windows\Fonts\calibrib.ttf'
font = ImageFont.truetype(font_path, 50)

tick_width = int(((page_width - 2 * margin_val) / projects_total.code_stats_total[-1]) / 2)
offset = int(((page_width - 2 * margin_val) - tick_width * 2 * projects_total.code_stats_total[-1]) / 2)

for i in range(0, len(project.moi)):
    comp_val = code_stats_complete[i]
    code = moi_codes[i]
    for j in range(0, code_stats_total[i]):
        fill_color = 'white'
        if comp_val > 0:
            fill_color = code_colors_completed[i]
            comp_val = comp_val - 1
        shape = [(margin_val + i * margin_val + i * row_width,
                  img_height - (margin_val + j * row_height)),
                 (margin_val + i * margin_val + i * row_width + row_width,
                  img_height - (margin_val + (j + 1) * row_height))]
        img_draw.rectangle(shape, fill=fill_color, outline=code_colors[i])
    try:
        p_val = round(100 * (code_stats_complete[i] / code_stats_total[i]), 2)
        code_str = (code + ":  (" +
                    str(code_stats_complete[i]) + "/" +
                    str(code_stats_total[i]) + ")  " +
                    str(p_val) + "% COMPLETE")
        img_draw.text((margin_val + i * margin_val + i * row_width,
                       img_height - (margin_val + (code_stats_total[i]) * row_height)),
                      code_str,
                      (0, 0, 0),
                      font=font)
    except:
        pass

full_val = projects_total.code_stats_total[-1]
comp_val = projects_total.code_stats_complete[-1]
lval = comp_val - project.code_stats_complete[-1]
rval = lval + project.code_stats_total[-1]
for i in range(0, full_val):
    color = 'green'
    tick_height = 50
    if i < comp_val:
        color = 'green'
    else:
        color = 'red'
    if lval < i < rval:
        tick_height = 70
    else:
        tick_height = 35
    if i % 100 == 0:
        tick_height = tick_height - 10
    shape = [(offset + margin_val + 2 * i * tick_width,
              img_height + margin_val),
             (offset + margin_val + 2 * i * tick_width + tick_width,
              img_height + margin_val + tick_height)]
    img_draw.rectangle(shape, fill=color)
fname = os.path.join(imdir, 'moi.png')
img.save(fname)

####################################################################
#             BELOW GETS THE COST VISUALIZATIONS                   #
####################################################################

sub_costs = []
sub_labels = []
sub_counts = []
sub_labels_counts = []
sub_nums = []
sub_qty = []
for subassembly in project.subassemblies:
    if 'image' in getattr(subassembly[0], 'Sub Assembly').lower():
        pass
    else:
        val = 0
        num = 0
        for item in subassembly:
            sub_qty.append(item.Qty)
            val = val + (item.Price * item.Qty)
            num = num + item.Qty
        sub_costs.append(round(val, 2))
        sub_labels.append((getattr(subassembly[0], 'Sub Assembly').split('-')[1]) + ": $" + str(round(val, 2)))
        sub_counts.append(len(subassembly))
        sub_nums.append(num)
        sub_labels_counts.append((getattr(subassembly[0], 'Sub Assembly').split('-')[1]) +
                                 " #Items: " + str(len(subassembly)) +
                                 " #Parts: " + str(num)
                                 )

fig, ax = plt.subplots(frameon=False, figsize=(16, 10), facecolor='white')
plt.gca().set_aspect('equal', adjustable='box')
plt.tight_layout()
plt.margins(x=0, y=0)
plt.axis('off')
plt.pie(sub_costs, labels=sub_labels, startangle=90, counterclock=False)
plt.legend(title="Sub Assemblies:")
ax.set_xlim(-1, 1)
ax.set_ylim(-1.25, 1.5)
plt.text(-1, 1.4, project.customer)
plt.text(-1, 1.35, project.sonum)
plt.text(-1, 1.3, "Project Cost Total: $" + str(sum(sub_costs)))
fname = os.path.join(imdir, 'sub1.png')
plt.savefig(fname)
plt.cla()

####################################################################

fig, ax = plt.subplots(frameon=False, figsize=(16, 10), facecolor='white')
plt.gca().set_aspect('equal', adjustable='box')
plt.tight_layout()
plt.margins(x=0, y=0)
plt.axis('off')

plt.pie(sub_nums, labels=sub_labels_counts, startangle=90, counterclock=False)

circle1 = plt.Circle((0, 0), 0.75, fill=False, edgecolor='black')
circle2 = plt.Circle((0, 0), 1, fill=False, edgecolor='black')
circle3 = plt.Circle((0, 0), 0.5, fill=False, edgecolor='black')
ax.add_patch(circle1)
ax.add_patch(circle2)
ax.add_patch(circle3)

theta = 0
val = 0
num = 0
r = 1
n = 0
endval = sum(sub_nums)
d_theta = 360 / endval

for i in range(0, len(sub_counts)):
    for j in range(0, sub_nums[i]):
        x = [(r - 0.25) * math.sin(math.radians(theta)), r * math.sin(math.radians(theta))]
        y = [(r - 0.25) * math.cos(math.radians(theta)), r * math.cos(math.radians(theta))]
        if n % 25 == 0:
            plt.plot(x, y, color='red')
        else:
            plt.plot(x, y, color='black')
        theta = theta + d_theta
        n = n + 1

theta = 0
n = 0

for i in range(0, len(sub_qty)):
    x = [(r - 0.5) * math.sin(math.radians(theta)), (r - 0.25) * math.sin(math.radians(theta))]
    y = [(r - 0.5) * math.cos(math.radians(theta)), (r - 0.25) * math.cos(math.radians(theta))]
    theta = theta + d_theta * sub_qty[i]
    plt.plot(x, y, color='black')

plt.legend(title="Sub Assemblies:")
ax.set_xlim(-1, 1)
ax.set_ylim(-1.25, 1.5)
plt.text(-1, 1.4, project.customer)
plt.text(-1, 1.35, project.sonum)
plt.text(-1, 1.3, "Project Items Total: " + str(sum(sub_counts)))
plt.text(-1, 1.25, "Project Parts Total: " + str(sum(sub_nums)))
fname = os.path.join(imdir, 'sub2.png')
plt.savefig(fname, facecolor=fig.get_facecolor())
# plt.show()
plt.cla()
