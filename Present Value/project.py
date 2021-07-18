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

def get_float_array_from_dataframe(df, col_name, dropBool):
    # First we will get the column in col_name
    col = df[col_name]
    # Next we have to strip off the first row of text
    # Not always needed. Always check. Better to have an argument to check first.
    #col = col.drop(col.index[0])
    # Like this \/
    if dropBool:
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

def optimalPackage(xyz,extraRoom):
    # This is the formula to use to check the optimal package
    # Consider any object in 3D will have a length, width height. For simplicity, we take the object and treat it as a rectangular box
    # Because of the nature of covering the object with plastic film, we can't just consider the surface area of the box.
    # Just like wrapping christmas presents, if you have a roll of paper, what area gets "wasted" with the folds?
    # We discover the perfect length and width for wrapping our box, with some extra room
    # Note: xyz array must be shortest val to largest val
    x = xyz[1]
    y = xyz[0]
    z = xyz[2]
    pWidth = x + (2*extraRoom) + y + (2*extraRoom)
    pLength = z + (2*extraRoom) + y + (2*extraRoom)
    return pWidth, pLength

# Roll Widths are the common widths the the rolls of film commonly come in, in inchest. These come from a .csv table
rollWidths = np.asarray(get_float_array_from_dataframe(df, 'roll_width_in', False))
rollWidthUnits = []

lenUnits = ["in (inches)", "mm (millimeter)", "cm (centemeter)", "meter (meter)"]
print("FILM PACKAGE MAKER V1.0 \n")

inputString = "Please select the units of measurement you will be inputing from the list below: "
for i in range(0,len(lenUnits)):
    inputString = inputString + "\n[" + str(i+1) + "] " + lenUnits[i]
inputString = inputString + "\n"

# This is the user's option for the units to use for length
uOp = getOp(inputString, 1, len(lenUnits) + 1) -1

print("You selected: [" + str(uOp + 1) + "] " + lenUnits[uOp] + "\n------------------------------------------------------")
 
inputUnit = lenUnits[uOp].split("(")[0][:-1]
ureg = UnitRegistry()

xyz = []
dimStrings = ["Length", "Width", "Height"]
print("Please enter the dimensions of your object in "  + inputUnit +  " (L x W x H): ")
# xyz is getting filled with the dimensions from the user for the object
for i in range(0, len(dimStrings)):
    inputValue = getFloat("Enter " + dimStrings[i] + ": ")
    xyz.append(inputValue * ureg.parse_expression(inputUnit) )
# Users often don't orientate the objects correctly (mixing up length x width etc). We sort the array from min to max values
xyz = sorted(xyz)
# The objects often need extra room, sometimes for seams etc. This is used to add those in
extraRoom = getFloat("Please enter the amount of space on each side of the object in " + inputUnit + ": ")* ureg.parse_expression(inputUnit)
# We get the optimal Width and Length of roll for the object
pWidth, pLength = optimalPackage(xyz,extraRoom)
# We use pint here to convert our roll width as an np.array to include the units of measurement
for i in range(0,len(rollWidths)):
    rollWidthUnits.append(rollWidths[i]*ureg.inch)
# Here we are initializing some values for checking the optimal length/width vs what's commercially available
dpW = pWidth
dpL = pLength
W = 0
L = 0
# We use this to tell us if we should reorientate the part for less waste on a commercially available roll
lwBool = False
# We go through the different sized roll widths, converting the units to match each other
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

inputString = "Please select the units of measurement you will be outputting from the list below: "
for i in range(0,len(lenUnits)):
    inputString = inputString + "\n[" + str(i+1) + "] " + lenUnits[i]
inputString = inputString + "\n"
# We need a user input for the output units of measurement
outOp = getOp(inputString, 1, len(lenUnits) + 1) -1
outputUnit = lenUnits[outOp].split("(")[0][:-1]
print("You selected: [" + str(outOp + 1) + "] " + lenUnits[outOp]+ "\n------------------------------------------------------")
# Finally, we check for best orientation to reduce amount of waste
if lwBool:
    if dpW < dpL:
        print("The rolls of film you should use for this object is   : " + str(rollWidthUnits[W].to(outputUnit)) + " (" + str(rollWidthUnits[W]) + ")")
        print("The length of film you should use to cover the object : " + str(pLength.to(outputUnit)))
    else:
        print("The rolls of film you should use for this object is   : " + str(rollWidthUnits[L].to(outputUnit)) + " (" + str(rollWidthUnits[L]) + ")")
        print("The length of film you should use to cover the object : " + str(pWidth.to(outputUnit)))
else:
    print("The object is too big for any of the rolls of film to go around...")
