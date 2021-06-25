import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm

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
n = 0.02270732  #This is the value I've found that gives a Q very close to 25.1 cfs... i found it ironically using iterative techniques
b = 3
z = 2
s = 0.01
#(hint: A depth of 1 foot will give you Q =  25.1 cfs)





def CalculateDepth(Q, n, b, z, s):
    print("Here goes....")
    error = 1
    accuracy = 0.01
    increment = 0.1
    y = 1
    oldYval = 1
    val = 1
    while(error > accuracy):
        if val < 100:
            oldYval = y
            print("-------------------------------------------------------------")
            print("val: " + str(val))
            print("y: " + str(y))
            print("error: " + str(error))
            print("accuracy: " + str(accuracy))
            print("increment: " + str(increment))
            dQ = TrapezoidalQ(n, b, y, z, s)
            print("dQ: " + str(dQ))
            error = Q-dQ
            print("new error: " + str(error))
            if error > 0:
                y = y + increment
            else:
                y = y - increment
                increment = increment/2
                error = -error
            val = val + 1
        else:
            stopit = input("Wanna stop this mess? type 'Yes' to exit. Anything else will loop further...")
            if stopit == "Yes":
                error = 1
                accuracy = 2
            else:
                val = 1
    return oldYval




def finish():
    Q = 50
    n = 0.02270732  #This is the value I've found that gives a Q very close to 25.1 cfs... i found it ironically using iterative techniques
    b = 3
    z = 2
    s = 0.01
    #(hint: A depth of 1 foot will give you Q =  25.1 cfs)
    y = CalculateDepth(Q, n, b, z, s)
    print("===========================================================================")
    print("y = " + str(y))    
    Q = TrapezoidalQ(n, b, y, z, s)
    print("Q = " + str(Q))    





#######################################################################
#        This is just for visualization purposes only                 #
#######################################################################

def gainingIntuition():
    n = 0.02270732  #This is the value I've found that gives a Q very close to 25.1 cfs... i found it ironically using iterative techniques
    b = 3
    z = 2
    s = 0.01
    
    X = []
    Y = []
    x = 1
    y = 1
    for i in range(0,100):
        X.append(x)
        Y.append(TrapezoidalQ(n, b, y, z, s))
        x = x + 0.01
        y = y + 0.01
    
    plt.plot(X,Y)
    plt.scatter(X,Y,color="BLUE")
    plt.plot([1,2],[50,50], color = "GREEN")
    plt.plot([1,2],[52,52], color = "RED")
    plt.plot([1,2],[48,48], color = "RED")
    plt.show()
    
    
    
#gainingIntuition() 
#finish()

def CalculateDepth2(Q, n, b, z, s):
    X = []
    Y = []
    Z = []
    print("Here goes....")
    error = 1
    accuracy = 0.01
    increment = 0.1
    y = 1
    oldYval = 1
    val = 1
    while(error > accuracy):
        if val < 100:
            oldYval = y
            print("-------------------------------------------------------------")
            print("iteration: " + str(val))
            print("y: " + str(y))
            print("error: " + str(error))
            print("accuracy: " + str(accuracy))
            print("increment: " + str(increment))
            dQ = TrapezoidalQ(n, b, y, z, s)
            X.append(y)
            Y.append(dQ)
            Z.append(val)
            print("dQ: " + str(dQ))
            error = Q-dQ
            print("new error: " + str(error))
            if error > 0:
                y = y + increment
            else:
                y = y - increment
                increment = increment/2
                error = -error
            val = val + 1
        else:
            stopit = input("Wanna stop this mess? type 'Yes' to exit. Anything else will loop further...")
            if stopit == "Yes":
                error = 1
                accuracy = 2
            else:
                val = 1
    plt.plot([min(X),max(X)],[Q,Q], color = "GREEN")
    plt.plot([min(X),max(X)],[Q+accuracy,Q+accuracy], color = "RED")
    plt.plot([min(X),max(X)],[Q-accuracy,Q-accuracy], color = "RED")
    X.append(oldYval)
    Y.append(TrapezoidalQ(n, b, oldYval, z, s))
    Z.append(val + 1)
    plt.scatter(X,Y,color="Black",s=55)
    plt.scatter(X,Y,c=Z,cmap="hot",s=25)
    #ugh = TrapezoidalQ(n, b, oldYval, z, s)
    #plt.scatter([oldYval],[ugh],c=[30])
    cbar = plt.colorbar()
    plt.show()
    return oldYval




def finish2():
    Q = 50
    n = 0.02270732  #This is the value I've found that gives a Q very close to 25.1 cfs... i found it ironically using iterative techniques
    b = 3
    z = 2
    s = 0.01
    #(hint: A depth of 1 foot will give you Q =  25.1 cfs)
    y = CalculateDepth2(Q, n, b, z, s)
    print("===========================================================================")
    print("y = " + str(y))    
    Q = TrapezoidalQ(n, b, y, z, s)
    print("Q = " + str(Q))    

finish2()


