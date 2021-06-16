import math

def CalculateDistance(n1, e1, n2, e2):
    return math.sqrt((n1-n2)**2 + (e1-e2)**2)

def CalculateBearing(n1, e1, n2, e2):
    b = 0
    if (n2 > n1):
        if (e2 > e1):
            b = 57.2958* math.atan((n2-n1)/(e2-e1))
        elif (e1 > e2):
            b = 57.2958* math.atan((n2-n1)/(e2-e1))+180
    elif (n1 > n2):
        if (e2 > e1):
            b = 57.2958* math.atan((n2-n1)/(e2-e1))+360
        elif (e1 > e2):
            b = 57.2958* math.atan((n2-n1)/(e2-e1))
    return b




#Location A - Front of the ATC
#29.2320, -81.0982
#17R 0490457E 3233696N

#Location B - Racetrac on LPGA Blvd
#9.2236, -81.0929
#17R 0490967E 3232763N

#Location C - Buc-ees
#29.2239, -81.1004
#17R 0490240E 3232801N

LocA = ["17R", "0490457E", "3233696N"]
LocB = ["17R", "0490967E", "3232763N"]
LocC = ["17R", "0490240E", "3232801N"]





def dist2(L1,L2):
    if L1[0] != L2[0]:
        print("These coordinates are not in the same UTM Zone")
    else:
        x1 = int(L1[1][:-1])
        y1 = int(L1[2][:-1])
        x2 = int(L2[1][:-1])
        y2 = int(L2[2][:-1])
        dx = x1-x2
        dy = y1-y2
        d = math.sqrt(dx**2 + dy**2)
        print("Locations:")
        print(L1)
        print(L2)
        print("Distance: " + str(round(d,2)) + " m")
        eastBool = True
        northBool = True
        direction = "Direction: "
        if dy < 0:
            direction = direction + "North-"
        else:
            direction = direction + "South-"
            northBool = False
        if dx < 0:
            direction = direction + "East"
        else:
            direction = direction + "West"
            eastBool = False
        print(direction)
        b = round(math.degrees(math.atan(dx/dy)),1)
        bearings = "Bearings: "
        if eastBool == True:
            if northBool == True:
                bearings = bearings + str(b+180)
            else:
                bearings = bearings + str(b-180)
        else:
            if northBool == True:
                bearings = bearings + str(b-180)
            else:
                bearings = bearings + str(b+360)
        print(bearings)
