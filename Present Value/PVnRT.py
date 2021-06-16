import matplotlib.pyplot as plt

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

def checkWholeNumber(r):
    rn = int(r)
    if r-rn != 0:
        return False
    else:
        return True

def getFloat(inputString):
    rBool = True
    while rBool:
        r = input(inputString)
        try:
            r = float(r)
            rBool = False
        except:
            print("' " + str(r) + " ' is not a valid input. Please try again...")
    return r

def getInt(inputString):
    rBool = True
    while rBool:
        r = input(inputString)
        try:
            r = float(r)
            if checkWholeNumber(r):
                r = int(r)
                rBool = False
            else:
                print("' " + str(r) + " ' is not a valid input. Please try again...")
        except:
            print("' " + str(r) + " ' is not a valid input. Please try again...")
    return r

def getNaturalNum(inputString):
    rBool = True
    while rBool:
        r = input(inputString)
        try:
            r = float(r)
            if checkWholeNumber(r):
                r = int(r)
                if r > 0:
                    rBool = False
                else:
                    print("' " + str(r) + " ' is not a valid input. Please try again...")
            else:
                print("' " + str(r) + " ' is not a valid input. Please try again...")
        except:
            print("' " + str(r) + " ' is not a valid input. Please try again...")
    return r

def getOp(inputString,sOp,fOp):
    rBool = True
    while rBool:
        r = input(inputString)
        try:
            r = float(r)
            if checkWholeNumber(r):
                r = int(r)
            else:
                r = sOp-1
        except:
            print("' " + str(r) + " ' is not a valid input. Please try again...")
        if r >= sOp and r<=fOp:
            rBool = False
        else:
            print("' " + str(r) + " ' is not a valid input. Please try again...")
    return r

def CalculateVolume(P,n,T):
    #Calculates Volume (V) from equation: PV=nRT
    R = 0.0821 #SI value for R is 8.31441 J K^-1 mol^-1 
    V = (n*R*T)/P
    return V

def getTemp(op):
    inputString = "Enter your value for Temperature:  "
    T = getFloat(inputString)
    if(op==1):
        T=T+273.15
    elif(op==2):
        c=(5*(T-32))/9
        T=c+273
    elif(op==3):
        T=T;
    return T

def getPressure(op):
    inputString = "Enter your value for Pressure:  "
    P = getFloat(inputString)
    if(op==1):
        P=P;
    elif(op==2):
        P=0.03342*P
    elif(op==3):
        P=0.06804*P
    return P

def example():
    pressure = [0.8, 0.9, 1.0, 1.1, 1.2] # Array of pressure
    volume = []
    n = 1
    T = 473
    for p in pressure: 
        volume.append(CalculateVolume(p, T, n))
    plt.scatter(pressure, volume)
    plt.xlabel("Pressure (atm)")
    plt.ylabel("Volume (liters")
    plt.scatter(pressure, volume)
    plt.show()
    
def makeEm():
    inputString = "Enter the number of points you would like to plot:  "
    numPoints = getNaturalNum(inputString)
    pressure = []
    Temps = []
    volume = []
    n=1
    T = 473
    P = 0.8
    print("----------------------------------------")
    pop = 3
    top = 3
    inputString = "Is the pressure constant? \n1. No \n2. Yes "
    ppop = getOp(inputString, 1, 2)
    inputString = "Enter units for pressure of gas in \n1. atm \n2. Hg \n3. psi "
    pop = getOp(inputString, 1, 3)
    if ppop != 1:
        P = getPressure(pop)
    inputString = "Is the Temperature constant? \n1. No \n2. Yes "
    ttop = getOp(inputString, 1, 2)
    inputString = "Select your Temperature scale \n1. Celsius \n2. Fahrenheit \n3. Kelvin \n"
    top = getOp(inputString, 1, 3)    
    if ttop != 1:
        T = getTemp(top)   
    for i in range(0,numPoints):
        print("Values for Point: " + str(i+1))
        if ppop != 1:
            pressure.append(P)
            print("Value for Pressure: " + str(P))
        else:
            pressure.append(getPressure(pop))
        if ttop != 1:
            Temps.append(T)
            print("Value for Temperature: " + str(T))
        else:
            Temps.append(getTemp(top))
        print("- - - - - - - - - - - - - - - - - - - - - - -")
    for i in range(0,numPoints):
        volume.append(CalculateVolume(pressure[i],n,Temps[i]))
    hdr = ["Point","Pressure","Temp","Volume"]
    theRows = []
    for i in range(0,numPoints):
        theRows.append([i+1,round(pressure[i],2),round(Temps[i],2),round(volume[i],2)])
    makeTable(hdr, theRows)
    plt.scatter(pressure, volume)
    plt.xlabel("Pressure (atm)")
    plt.ylabel("Volume (liters")
    plt.scatter(pressure, volume)
    plt.show()

makeEm()


