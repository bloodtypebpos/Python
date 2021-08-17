import os
import openpyxl
import sqlite3

dbDir = r'C:\Users\Matt\Desktop\BadMoney'

fname = os.path.join(dbDir,'badMoney.db')
conn = sqlite3.connect(fname)
c = conn.cursor()

columns = ['section','sectionTitle','sectionDescription','account','closeBalanceToday','today','thisMonth','thisFiscalYear','datecode']


fnames = os.listdir(dbDir)
for fname in fnames:
    print(fname)
    if ".xlsx" in fname:
        datecode = fname.split(".")[0]
        fn = os.path.join(dbDir,fname)
        wb = openpyxl.load_workbook(fn)
        sht = wb['DTS Report']
        maxRow = sht.max_row + 1
        section = "NA"
        sectionTitle = "NA"
        sectionDescription = "NA"
        for i in range(3,maxRow):
            if sht["D"+str(i)].value == "Today":
                section = sht["A"+str(i)].value
                sectionTitle = sht["B"+str(i)].value
                sectionDescription = sht["B"+str(i-1)].value
            else:
                if sht["D"+str(i)].value == None:
                    pass
                else:
                    account = sht["B"+str(i)].value
                    closeBalanceToday = sht["C"+str(i)].value
                    today = sht["D"+str(i)].value
                    thisMonth = sht["E"+str(i)].value
                    thisFiscalYear = sht["F"+str(i)].value
                    row = [section,sectionTitle,sectionDescription,account,closeBalanceToday,today,thisMonth,thisFiscalYear,datecode]
                    query = 'insert into badMoney('
                    for j in range(0,len(columns)):
                        query = query + columns[j] + ','
                    query = query[:-1] + ") values ("
                    for j in range(0,len(columns)):
                        query = query + '?,'
                    query = query[:-1] + ")"
                    c.execute(query,row)
        conn.commit()
