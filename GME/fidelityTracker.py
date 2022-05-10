import json
from bs4 import BeautifulSoup as bs
import urllib.request
import time
import openpyxl
import os
import matplotlib.pyplot as plt
import sqlite3

dbDir = r'C:\Users\Matt\Desktop\GME\FidelityBuyRatios'

fname = os.path.join(dbDir, 'WeeboWaboGME.db')
conn = sqlite3.connect(fname)
c = conn.cursor()

fname = os.path.join(dbDir,'fidelity.xlsx')
wb = openpyxl.load_workbook(fname)
linkSheet = wb['linkSheet']
dataSheet = wb['dataSheet']

urls = []
for i in range(2,89):
    urls.append(linkSheet["B"+str(i)].value)

def get_page(url,rowNum):
    print('url:', url)
    time.sleep(1)
    ranks = [] # first
    tickers = [] # second
    companies = [] # third
    deltaPrice = []
    buys = [] # fifth
    sells = [] # seventh
    theData = [ranks,tickers,companies,buys,sells]
    tdClasses = ['first','second','third','fifth','seventh']
    alphaCols = ['B','C','D','E','F']
    rNum = rowNum

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = str(html)
        soup = bs(html, features='lxml')
        html = soup.prettify()
        #print(html)
        spans = soup.find_all('span', {'class': 'source'})

        date = url.split('/web/')[1]
        yr = date[0:4]
        mn = date[4:6]
        dy = date[6:8]
        date = mn + '/' + dy + '/' + yr
        print(date)

        #for span in spans:
        #    date = str(span)
        #    date = date.split("  ")[1]
        #    date = date.split("<")[0]
        #    print(date)

        for i in range(0,len(tdClasses)):
            tds = soup.find_all('td', {'class': tdClasses[i]})
            for td in tds:
                theData[i].append(str(td))

        for i in range(0,len(ranks)):
            rNum = rNum + 1
            dataSheet["A"+str(rNum)].value = date
            for j in range(0,len(theData)):
                val = theData[j][i].split('">')[-1]
                val = val.split('<')[0]
                dataSheet[alphaCols[j]+str(rNum)].value = val
    return rNum


def get_page2(url):
    print('url:', url)
    time.sleep(1)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = str(html)
        soup = bs(html, features='lxml')
        html = soup.prettify()
        print(html)

#get_page2("https://web.archive.org/web/*/https://eresearch.fidelity.com/eresearch/gotoBL/fidelityTopOrders.jhtml")

def goGetem():
    rowNum = 1
    for url in urls:
        try:
            rowNum = get_page(url,rowNum)
        except:
            pass
    fname = os.path.join(dbDir,'fidelityOut.xlsx')
    wb.save(fname)
    wb.close()


rows = []
query = "SELECT * FROM fidelityOut WHERE SYMBOL = 'GME'"
crows = c.execute(query)
for row in crows:
    rows.append(row)
X = []
Y = []
Z = []
for i in range(0,len(rows)):
    X.append(i)
    Y.append(rows[i][7])
    Z.append(rows[i][1])

plt.plot(X,Y)
plt.plot([0,0],[0,max(Y)])
plt.plot([0,max(X)],[0,0])
plt.plot([0,max(X)],[50,50],linestyle='--')
plt.show()
