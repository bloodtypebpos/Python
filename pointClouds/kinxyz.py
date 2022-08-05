import os
import matplotlib.pyplot as plt
import sqlite3
import openpyxl
import numpy as np

dbdir = r'C:\Users\Sad_Matt\Desktop\Python\Murdock'
fname = os.path.join(dbdir, 'kinxyz.txt')

colors = ['BLACK', 'RED', 'BLUE', 'GREEN', 'ORANGE', 'PURPLE', 'CYAN', 'PINK']

X = [0]
Y = [0]
Z = [0]
cluster = []

xlims = [100000, -10000]
ylims = [100000, -10000]
zlims = [100000, -10000]

with open(fname) as file:
    for line in file:
        if 'R' in line.rstrip():
            cluster.append([X, Y, Z])
            X = []
            Y = []
            Z = []
        else:
            pnt = line.rstrip().split(',')
            x = float(pnt[0])
            y = float(pnt[1])
            z = float(pnt[2])
            if x < xlims[0]:
                xlims[0] = x
            if x > xlims[1]:
                xlims[1] = x
            if y < ylims[0]:
                ylims[0] = y
            if y > ylims[1]:
                ylims[1] = y
            if z < zlims[0]:
                zlims[0] = z
            if z > zlims[1]:
                zlims[1] = z
            X.append(x)
            Y.append(y)
            Z.append(z)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(0, len(cluster)):
    xyz = cluster[i]
    ax.scatter(xyz[0], xyz[1], xyz[2], color=colors[i % len(colors)])
    for x in xyz:
        print(x)
    print("========================================")

print(xlims)
print(ylims)
print(zlims)

ax.set_xlim(xlims[0], xlims[1])
ax.set_ylim(ylims[0], ylims[1])
ax.set_zlim(zlims[0], zlims[1])

ax.set_box_aspect((np.ptp(xlims), np.ptp(ylims), np.ptp(zlims)))

plt.show()
