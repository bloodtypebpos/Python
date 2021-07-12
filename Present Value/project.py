import pint
from pint import UnitRegistry

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
            if r > 0:
                rBool = False
            else:
                print("' " + str(r) + " ' is not a valid input. Dimension must be greater than 0. Please try again...")
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


def convertUnits(inputValue,inputUnit,outputUnit):
    ureg = UnitRegistry()    
    home = inputValue * ureg.parse_expression(inputUnit)        
    return home.to(outputUnit)

def optimalPackage(xyz):
    x = xyz[1]
    y = xyz[0]
    z = xyz[2]
    pWidth = x + (2*extraRoom) + y + (2*extraRoom)
    pLength = z + (2*extraRoom) + y + (2*extraRoom)
    return pWidth, pLength

# Roll Widths are the common widths, in inches, the the rolls of film commonly come in
rollWidths = [5,9,12,18,24,36,40]
rollWidthUnits = []

lenUnits = ["in (inches)", "mm (millimeter)", "cm (centemeter)", "meter (meter)"]
print("FILM PACKAGE MAKER V1.0")
print(" ")

inputString = "Please select the units of measurement you will be inputing from the list below: "
for i in range(0,len(lenUnits)):
    inputString = inputString + "\n[" + str(i+1) + "] " + lenUnits[i]
inputString = inputString + "\n"

uOp = getOp(inputString, 1, len(lenUnits) + 1) -1

print("You selected: [" + str(uOp + 1) + "] " + lenUnits[uOp])
print("------------------------------------------------------")
 
inputUnit = lenUnits[uOp].split("(")[0][:-1]
ureg = UnitRegistry()

xyz = []
dimStrings = ["Length", "Width", "Height"]
print("Please enter the dimensions of your box in "  + inputUnit +  " (L x W x H): ")
for i in range(0, len(dimStrings)):
    inputValue = getFloat("Enter " + dimStrings[i] + ": ")
    xyz.append(inputValue * ureg.parse_expression(inputUnit) )
xyz = sorted(xyz)

print(xyz)

extraRoom = getFloat("Please enter the amount of space on each side of the object in " + inputUnit + ": ")
extraRoom = extraRoom * ureg.parse_expression(inputUnit)


pWidth, pLength = optimalPackage(xyz)
print(pWidth)
print(pLength)

for i in range(0,len(rollWidths)):
    rollWidthUnits.append(rollWidths[i]*ureg.inch)

dpW = pWidth
dpL = pLength
W = 0
L = 0

lwBool = False

for i in range(0,len(rollWidthUnits)):
    dVal = rollWidthUnits[i].to(inputUnit) - pWidth
    if dVal > 0:
        lwBool = True
        if dVal < dpW:
            dpW = dVal
            W = i
    dVal = rollWidthUnits[i].to(inputUnit) - pLength
    if dVal > 0:
        lwBool = True
        if dVal < dpL:
            dpL = dVal
            L = i

print("--------------------------------------------")
print("dpL: " + str(dpL))
print("dpW: " + str(dpW))
print("L: " + str(L))
print("W: " + str(W))
print("L Roll Width: " + str(rollWidthUnits[L]))
print("W Roll Width: " + str(rollWidthUnits[W]))

print("--------------------------------------------")

inputString = "Please select the units of measurement you will be outputting from the list below: "
for i in range(0,len(lenUnits)):
    inputString = inputString + "\n[" + str(i+1) + "] " + lenUnits[i]
inputString = inputString + "\n"

outOp = getOp(inputString, 1, len(lenUnits) + 1) -1
outputUnit = lenUnits[outOp].split("(")[0][:-1]
print("You selected: [" + str(outOp + 1) + "] " + lenUnits[outOp])
print("------------------------------------------------------")


if lwBool:
    if dpW < dpL:
        print("The rolls of film you should use for this object is   : " + str(rollWidthUnits[W].to(outputUnit)) + " (" + str(rollWidthUnits[W]) + ")")
        #print("The rolls of film you should use for this object is   : " + str(rollWidthUnits[W]) + " (" + str(rollWidthUnits[W].to(outputUnit)) + ")")
        print("The length of film you should use to cover the object : " + str(pLength.to(outputUnit)))
    else:
        print("The rolls of film you should use for this object is   : " + str(rollWidthUnits[L].to(outputUnit)) + " (" + str(rollWidthUnits[L]) + ")")
        #print("The rolls of film you should use for this object is   : " + str(rollWidthUnits[L]) + " (" + str(rollWidthUnits[L].to(outputUnit)) + ")")
        print("The length of film you should use to cover the object : " + str(pWidth.to(outputUnit)))
else:
    print("The object is too big for any of the rolls of film to go around...")
