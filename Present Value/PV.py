def makeTable(hdr,theRows):
    colWidths = []
    for i in range(0,len(hdr)):
        colWidths.append(len(str(hdr[i])))
    for i in range(0,len(theRows)):
        for j in range(len(theRows[i])):
            if len(str(theRows[i][j])) > colWidths[j]:
                colWidths[j] = len(str(theRows[i][j]))
    tblLine = "+-"
    for i in range(0,len(colWidths)):
        for j in range(0,colWidths[i]):
            tblLine = tblLine + "-"
        tblLine = tblLine + "-+-"
    tblLine = tblLine[:-1]
    print(tblLine)
    theRow = "| "
    for i in range(0,len(hdr)):
        theRow = theRow + str(hdr[i])
        for j in range(0,colWidths[i]-len(hdr[i])):
            theRow = theRow + " "
        theRow = theRow + " | "
    theRow = theRow[:-1]
    print(theRow)
    hdrLine = "+="
    for i in range(0,len(colWidths)):
        for j in range(0,colWidths[i]):
            hdrLine = hdrLine + "="
        hdrLine = hdrLine + "=+="
    hdrLine = hdrLine[:-1]
    print(hdrLine)
    for i in range(0,len(theRows)):
        theRow = "| "
        for j in range(0,len(hdr)):
            theRow = theRow + str(theRows[i][j])
            for k in range(0,colWidths[j]-len(str(theRows[i][j]))):
                theRow = theRow + " "
            theRow = theRow + " | "
        theRow = theRow[:-1]
        print(theRow)
        print(tblLine)

def getRate(n):
    rBool = True
    while rBool:
        r = input("Please enter the interest rate. Note: 5 = 5%    ")
        try:
            r = float(r)
            print("The interest rate you entered is: " + str(round(r,1)) + "%")
            print("The number of years is: " + str(n))
            r = r/100
            rBool = False
        except:
            print("' " + str(r) + " ' is not a valid input. Please try again...")
    return r

def PV(FV,r,n):
    val = FV/((1+r)**n)
    return val

def AV(C,r,n):
    val = 0
    while n>0:
        val = val + (C/((1+r)**n))
        n = n-1
    return val

#n = how many iterations (years)
n = 10
r = getRate(n)

hdr = ["Resale Amount","Annual Revenue","PV of Resale","PV of Revenue","Total PV"]
FVs = [10000,9000,5000,3000,0]
Cs  = [500,600,1000,1200,1500]
FVPV  = []
CsPV  = []
Total = []
theRows = []

for i in range(0,len(FVs)):
    FV = FVs[i]
    C = Cs[i]
    p1 = PV(FV, r, n)
    p2 = AV(C, r, n)
    p = round(p1+p2,2)
    ############################ However you want to use the data... I use rows...
    FVPV.append(round(p1,2))
    CsPV.append(round(p2,2))
    Total.append(p)
    theRows.append([FV,C,round(p1,2),round(p2,2),p])

makeTable(hdr, theRows)
