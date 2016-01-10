import urllib2
import re
#connect to a URL
alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
y = []
j = 0


while j < len(alphabet):
    site = "http://www.charitynavigator.org/index.cfm?bay=search.alpha&ltr="
    website = urllib2.urlopen(site + alphabet[j])
    #read html code
    html = website.read()
    #use re.findall to get all the links
    x = re.findall('"((http|ftp)s?://.*?)"', html)
    i = 0
    z = []
    w = []
    sub = "http://www.charitynavigator.org/index.cfm?bay=search.summary&orgid"
    
    while i < len(x):
        z.append(x[i][0])
        i+=1  
    i = 0
    
    while i < len(z):
        z[i] = z[i].replace(" ('","")
        z[i] = z[i].replace("amp;","")
        z[i] = z[i].replace("'","")
        if sub in z[i]:
            w.append(z[i])
        i+=1   
        
    y.append(w)
         
    j+=1


myFile = open('File.txt', 'w')
myFile.truncate()
theNextLine = "\n"

i = 0
j = 0
while i < len(y):
    while j < len(y[i]):
        myFile.write(y[i][j] + theNextLine)
        j+=1
    j=0
    i+=1
    
myFile.close()   
