import urllib2
import re
import urllib
import csv


f = open('File.txt', 'r')
x = f.readlines()


urls = x
i = 0
regex = '<td align="right">(.+?)</td>'
regex2 = '<h1 class="charityname">(.+?)</h1>'

y = []

pattern = re.compile(regex)
pattern2 = re.compile(regex2)


while i < 100:
    argh = 0
    htmlfile = urllib.urlopen(urls[i])
    htmltext = htmlfile.read()
    titles = re.findall(pattern2, htmltext)
    information = re.findall(pattern,htmltext)
    while argh < len(information):
        information[argh] = information[argh].replace("'","")
        information[argh] = information[argh].replace(",","")
        information[argh] = information[argh].replace("%","")
        information[argh] = information[argh].replace("<strong>","")
        information[argh] = information[argh].replace("</strong>","")
        information[argh] = information[argh].replace("$","")
        information[argh] = information[argh].replace(" ","")
        information[argh] = information[argh].replace("&nbsp","")
        information[argh] = information[argh].replace(";","")
        titles.append(information[argh])
        argh+=1
    y.append(titles)
    i+=1

i = 0
while i < len(y):
    print(y[i])
    i+=1
    
    
myFile = open('File.csv', 'w')
myFile.truncate()
theNextLine = "\n"
myFile.close() 

i = 0

with open('File.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL, quotechar='|')
    while i<len(y):
        spamwriter.writerow(y[i])
        i+=1

