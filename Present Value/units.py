import pint
from pint import UnitRegistry

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
                if r >= sOp and r<=fOp:
                    rBool = False
                else:
                    print("' " + str(r) + " ' is not a valid input. Please try again...")                
            else:
                print("' " + str(r) + " ' is not a valid input. Please try again...")
        except:
            print("' " + str(r) + " ' is not a valid input. Please try again...")
    return r

def CalculateVolume(P,n,T):
    #Calculates Volume (V) from equation: PV=nRT
    R = 0.0821 #SI value for R is 8.31441 J K^-1 mol^-1 
    V = (n*R*T)/P
    return V

def getPressure():
    inputString = "Enter units for pressure of gas in \n1. atm \n2. in Hg \n3. psi \n"
    pop = getOp(inputString, 1, 3) -1
    inputString = "Please enter the value for Pressure in " + psTypes[pop] + ": "
    P = getFloat(inputString)
    return P, pop

def getTemp():
    inputString = "Select your Temperature scale \n1. Celsius \n2. Fahrenheit \n3. Kelvin \n"
    top = getOp(inputString, 1, 3) -1
    inputString = "Please enter the value for Temperature in " + tsTypes[top] + ": "
    T = getFloat(inputString)
    return T, top    


def convertTemp(T,top1,top2):
    #The 3 lines here for ureg are just setting the baseline for our temperature units
    ureg = UnitRegistry(autoconvert_offset_to_baseunit = True)
    ureg.default_format = '.3f'
    Q_ = ureg.Quantity
    if top1 == 0:
        home = Q_(T, ureg.degC)
    elif top1 == 1:
        home = Q_(T, ureg.degF)
    elif top1 == 2:
        home = Q_(T, ureg.degK)        
    return home.to(tTypes[top2])

def convertPressure(P,pop1,pop2):
    ureg = UnitRegistry()    
    home = P * ureg.parse_expression(pTypes[pop1])        
    return home.to(pTypes[pop2])

pTypes = ["atm", "inHg", "psi"]
psTypes = ["atm", "in Hg", "psi"]
tTypes = ['degC', 'degF', 'degK']
tsTypes = ['Celsius', 'Fahrenheit', 'Kelvin']

Ps = []
Ts = []

print("ENTER THE VALUES FOR PRESSURE AND TEMPERATURE FOR ALL THE POINTS")
for i in range(0,3):
    print("Enter values for point: " + str(i+1))
    T, top = getTemp()
    Ts.append([T,top])
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    P, pop = getPressure()
    Ps.append([P,pop])
    print("===================================================================")

hdr = ["Input Temperature","Temp in K", "Input Pressure","P in atm", "Volume in liters"]
rows = []

n = 1
#rounding is how many decimal places will show
rounding = 5

for i in range(0,len(Ts)):
    T = str(Ts[i][0]) + " " + tsTypes[Ts[i][1]]
    dT = convertTemp(Ts[i][0],Ts[i][1],2)
    P = str(Ps[i][0]) + " " + psTypes[Ps[i][1]]
    dP = convertPressure(Ps[i][0],Ps[i][1],0)
    V = CalculateVolume(dP.magnitude, n, dT.magnitude)
    rows.append([T,round(dT.magnitude,rounding),P,round(dP.magnitude,rounding),round(V,rounding)])    

print(" ")

makeTable(hdr,rows)



# Temps
##########
# 500 C = 773.150 K
# 100 F = 310.928 K
# 500 K = 500.000 K

#Pressures
##########
# 1 atm    = 1.00000 atm
# 30 in Hg = 1.00263 atm
# 5 psi    = 0.34023 atm

