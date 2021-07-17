import os
import pint
from pint import UnitRegistry
import pandas as pd
import numpy as np

# Directory for support files to be located in
# The file that contains the information for the packaging roll details is:
# packaging_roll_details.csv
dbDir = r"C:\Users\Sad_Matt\Desktop\James"

# Getting the filename
fname = os.path.join(dbDir, 'packaging_roll_details.csv')
# Making dataframe with pandas
df = pd.read_csv(fname)

def get_float_array_from_dataframe(df, col_name):
    # First we will get the column in col_name
    col = df[col_name]
    # Next we have to strip off the first row of text
    col = col.drop(col.index[0])
    # We can then return it as an array -
    # col.values is an array of strings, the following code
    # converts all of the values to float
    return [float(x) for x in col.values]

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

def optimalPackage(xyz,extraRoom):
    x = xyz[1]
    y = xyz[0]
    z = xyz[2]
    pWidth = x + (2*extraRoom) + y + (2*extraRoom)
    pLength = z + (2*extraRoom) + y + (2*extraRoom)
    return pWidth, pLength



def runTest():
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
    
    
    pWidth, pLength = optimalPackage(xyz,extraRoom)
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
        


def runTest2():
    # columns that need to be converted to floats
    cols = ['temperature_C','thickness_in','max_weight_lbs','seam_allowance_in','roll_width_in']
    # convert column values to floats
    for col in cols:
        df[col] = df[col].astype(float)
    
    l = 5
    w = 10
    h = 15
    weight = 6
    
    df2 = df[(df['max_weight_lbs'] > weight)]
    rollWidthsAll = get_float_array_from_dataframe(df2, 'roll_width_in')
    rollWidths = []
    for i in range(0, len(rollWidthsAll)):
        if rollWidthsAll[i] not in rollWidths:
            rollWidths.append(rollWidthsAll[i])
    
    for i in range(0, len(rollWidths)):
        print(rollWidths[i])



def runTest3():
    # Roll Widths are the common widths, in inches, the the rolls of film commonly come in
    rollWidths = [5,9,12,18,24,36,40]
    rollWidthUnits = []
    
    lenUnits = ["in (inches)", "mm (millimeter)", "cm (centemeter)", "meter (meter)"]
    weightUnits = ["lbs (pounds)", "g (grams)", "kg (kilogram)", "oz (ounce)"]
    print("FILM PACKAGE MAKER V1.0")
    print(" ")
    
    
    inputString = "Please select the units of measurement you will be inputing from the list below for weights: "
    for i in range(0,len(weightUnits)):
        inputString = inputString + "\n[" + str(i+1) + "] " + weightUnits[i]
    inputString = inputString + "\n"
    
    wOp = getOp(inputString, 1, len(weightUnits) + 1) -1
    
    print("You selected: [" + str(wOp + 1) + "] " + weightUnits[wOp])

    
    weightUnit = weightUnits[wOp].split("(")[0][:-1]
    weightInput = getFloat("Enter the weight of your object in " + weightUnit + ": ")
    print("Weight of object is: " + str(weightInput) + weightUnit)
    print("------------------------------------------------------")
    
    
    #######################################################################
    #######################################################################
    #######################################################################
    
    inputString = "Please select the units of measurement you will be inputing from the list below for lengths: "
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
    print("Please enter the dimensions of your object in "  + inputUnit +  " (L x W x H): ")
    for i in range(0, len(dimStrings)):
        inputValue = getFloat("Enter " + dimStrings[i] + ": ")
        xyz.append(inputValue * ureg.parse_expression(inputUnit) )
    xyz = sorted(xyz)
    
    extraRoom = getFloat("Please enter the amount of space on each side of the object in " + inputUnit + ": ")
    extraRoom = extraRoom * ureg.parse_expression(inputUnit)
    
    
    pWidth, pLength = optimalPackage(xyz,extraRoom)
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


runTest3()
