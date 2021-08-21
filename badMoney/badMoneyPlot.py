import os
import sqlite3
import matplotlib.pyplot as plt


dbDir = r'C:\Users\Matt\Desktop\BadMoney'

fname = os.path.join(dbDir,'badMoney.db')
conn = sqlite3.connect(fname)
c = conn.cursor()

query = 'select closeBalanceToday,datecode from badMoney where account = "Federal Reserve Account" order by datecode'
rows = []
crows = c.execute(query)
for row in crows:
    rows.append(row)

X = []
Y = []
Z = []

dBool = True
for i in range(0,len(rows)):
    X.append(i)
    Y.append(rows[i][0])
    dNum = str(rows[i][1])
    dNum = int(dNum[4])
    if dNum == 0:
        if dBool:
            Z.append(rows[i][1])
            dBool = False
        else:
            Z.append("")
    else:
        dBool = True
        Z.append("")



lineColors = ["yellow","orange","green"]

for i in range(0,len(X)):
    if Z[i] != "":
        znum = int(str(Z[i])[:2]) - 19
        print(znum)
        plt.plot([i,i],[min(Y),max(Y)], lineColors[znum], alpha=0.2)


plt.plot(X,Y,color="white",linewidth=10)
plt.plot(X,Y,linewidth=2)
plt.title("Federal Reserve Account")
plt.xticks(X, Z, rotation='vertical')

plt.show()




