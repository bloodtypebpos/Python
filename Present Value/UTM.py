import math

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

LocD = ["17R", "0490457E", "3232763N"]  # Loc A's Easting and Loc B's Northing
LocE = ["17R", "0490967E", "3233696N"]  # Loc B's Easting and Loc B's Northing 


def dist2(L1,L2):
    if L1 == L2:
        print("These two coordinates are the same!")
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
        if dy == 0:
            pass
        elif dy < 0:
            direction = direction + "North "
        else:
            direction = direction + "South "
            northBool = False
        if dx == 0:
            pass
        elif dx < 0:
            direction = direction + "East"
        else:
            direction = direction + "West"
            eastBool = False
        print(direction)
        
        # If dy = 0, then atan(dx/dy) gives error
        # However, we know if dy = 0 then we're just moving EAST or WEST
        # So we just set the direction to 90* or 270* if dy = 0
        if dy == 0:
            if dx < 0:
                b = round(math.degrees(math.pi/2),1)
            else:
                b = round(math.degrees((3*math.pi)/2),1)
        else:
            b = round(math.degrees(math.atan(dx/dy)),1)
        
        
        bearings = "Bearings: "
        if eastBool == True:
            if northBool == True:
                #North-East
                b = b
                #bearings = bearings + str(b)
            else:
                #South-East
                b = b + 180
                #bearings = bearings + str(b+180)
        else:
            if northBool == True:
                #North-West
                b = b + 360
                #bearings = bearings + str(b+360)
            else:
                #South-West
                b = b + 180
                #bearings = bearings + str(b+180)
        if b > 360:
            b = b-360
        bearings = bearings + str(b)
        print(bearings)

print("-----------------------------------------------------------")
# North-West
dist2(LocB,LocA)
print("-----------------------------------------------------------")
# North-East
dist2(LocC,LocA)
print("-----------------------------------------------------------")
# South-West
dist2(LocA,LocC)
print("-----------------------------------------------------------")
# South-East
dist2(LocA,LocB)
print("-----------------------------------------------------------")
# South
dist2(LocA,LocD)
print("-----------------------------------------------------------")
# North
dist2(LocD,LocA)
print("-----------------------------------------------------------")
# East
dist2(LocA,LocE)
print("-----------------------------------------------------------")
# West
dist2(LocE,LocA)
print("-----------------------------------------------------------")
# Same Location
dist2(LocA,LocA)
print("-----------------------------------------------------------")




