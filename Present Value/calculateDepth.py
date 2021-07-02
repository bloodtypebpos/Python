import math
def TrapezoidalQ(n,b,y,z,s):
    # n is Manning's n - table at 
    # https://www.engineeringtoolbox.com/mannings-roughness-d_799.html
    # b = Bottom width of channel (ft)
    # y = Depth of channel (ft)
    # z = Side slope of channel (horizontal)
    # s = Directional slope of channel - direction of flow
    A = b*y + z*y*y
    W = b + 2*y*math.sqrt(1 + z*z)
    R = A/W
    Q = 1.49/n * A * math.pow(R, 2.0/3.0) * math.sqrt(s)
    return Q
Q = 50
n = 0.022
b = 3
z = 2
s = 0.01
#(hint: A depth of 1 foot will give you Q =  25.1 cfs)
def CalculateDepth(Q, n, b, z, s):
    error = 1
    accuracy = 0.01
    increment = 0.1
    y = 1
    oldYval = 1
    while(error > accuracy):
        oldYval = y
        dQ = TrapezoidalQ(n, b, y, z, s)
        error = Q-dQ
        if error > 0:
            y = y + increment
        else:
            y = y - increment
            increment = increment/2
            error = -error
    return oldYval
y = CalculateDepth(Q, n, b, z, s)
print("y = " + str(y))
Q = TrapezoidalQ(n, b, y, z, s)
print("Q = " + str(Q))
