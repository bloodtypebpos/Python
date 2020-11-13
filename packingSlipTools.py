import openpyxl
import os
import datetime
import time

dbdir = r'S:\PACKING-SLIP'


def c2dtime(inputTime):
    return datetime.datetime.fromtimestamp(inputTime)#.strftime('%Y-%m-%d %H:%M:%S')

def num2num(OldValue,OldMin,OldMax,NewMin,NewMax):
    return (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

def dateRanger():
    mValMin = 0
    mValMax = 3
    mainMenuStatus = 1
    endDate = datetime.date(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day)
    startDate = datetime.date(2010,1,1)
    print("Please select from the following:")
    print("   [0] Return to the Main Menu?")
    print("   [1] Search Packing Slips from dates after the beginning of this year?")
    print("   [2] Search Packing Slips from dates after an input date?")
    print("   [3] Search Packing Slips between two input dates?")
    print("   [4] Search every single Packing Slip.... Not Recommended")
    mVal = mValCheck(mValMin,mValMax)
    if mVal == 0:
        mainMenuStatus = 0
    elif mVal == 1:
        startDate = datetime.date(datetime.date.today().year,1,1)
    elif mVal == 2:
        print("Please enter the date you want to search from in the format: YYYY,MM,DD")
        dateInput = input("   examples:    2011,12,25         2017,5,15       2020,2,7")
        try:
            dateYear = int(dateInput.split(",")[0])
            dateMonth = int(dateInput.split(",")[1])
            dateDay = int(dateInput.split(",")[2])
            startDate = datetime.date(dateYear,dateMonth,dateDay)
        except:
            print("Your entry was invalid, and a start date of the beginning of this year will be used instead")
    elif mVal == 3:
        print("Please enter the date you want to search from in the format: YYYY,MM,DD")
        dateInput = input("   examples:    2011,12,25         2017,5,15       2020,2,7")
        try:
            dateYear = int(dateInput.split(",")[0])
            dateMonth = int(dateInput.split(",")[1])
            dateDay = int(dateInput.split(",")[2])
            startDate = datetime.date(dateYear,dateMonth,dateDay)
        except:
            print("Your entry was invalid, and a start date of the beginning of this year will be used instead")        
        print("Please enter the date you want to search after in the format: YYYY,MM,DD")
        dateInput = input("   examples:    2011,12,25         2017,5,15       2020,2,7        : ")
        try:
            dateYear = int(dateInput.split(",")[0])
            dateMonth = int(dateInput.split(",")[1])
            dateDay = int(dateInput.split(",")[2])
            endDate = datetime.date(dateYear,dateMonth,dateDay)
        except:
            print("Your entry was invalid, and a start date of the beginning of this year will be used instead")
    return [mainMenuStatus,startDate,endDate]





    

def findByCity():
    print("[1] Find Packing Slips by City")
    print("- - - - - - - - - - - - - - - ")
    dateRange = dateRanger()
    if dateRange[0] == 0:
        print("Sorry... we'll fix this in the future....")
    city = input("Please enter the name of the City you are looking for: ")
    result = []
    fnames = os.listdir(dbdir)
    fromDate = dateRange[1]
    toDate = dateRange[2]
    val = 0
    num = 1
    dnum = 0
    dfnames = []
    for f in fnames:
        fname = os.path.join(dbdir,f)
        theDate = c2dtime(os.path.getctime(fname))
        newDate = datetime.date(theDate.year,theDate.month,theDate.day)
        if newDate >= fromDate:
            if newDate <= toDate:
                num = num + 1
                dfnames.append(fname)
    for f in dfnames:
        if val < 10:
            #print(dnum)
            dnum = dnum + 1
            newdnum = num2num(dnum,0,num,0,50)
            newdnum = int(newdnum)
            #print(dnum)
            loadStr = ""
            for i in range(0,newdnum):
                loadStr = loadStr + "#"
            for i in range(newdnum,50):
                loadStr = loadStr + "-"
            os.system('CLS')
            print(loadStr + "| " + str(dnum) + " / " + str(num))
            fname = os.path.join(dbdir,f)
            theDate = c2dtime(os.path.getctime(fname))
            newDate = datetime.date(theDate.year,theDate.month,theDate.day)
            if newDate > fromDate:
                #val = val + 1
                if ".xlsx" in fname:
                    #print(fname)
                    #print(newDate)
                    wb = openpyxl.load_workbook(fname)
                    sht = wb[wb.sheetnames[0]]
                    addr = sht["D9"].value
                    wb.close()
                    try:
                        if city.lower() in addr.lower():
                            result.append([fname,newDate])
                    except:
                        pass
        else:
            break
    if len(result) > 0:
        for res in result:
            for r in res:
                print(r)
            print("---------------------------------")
    else:
        print("There were no matches")
    input("The search is complete! Hit the Enter Key to return to the Main Menu")
    return 0


def mValCheck(mValMin,mValMax):
    mValBool = True
    while mValBool:
        mVal = input("Please make your selection and hit Enter: ")
        try:
            dmValBool = True
            mVal = int(mVal)
            if mVal < mValMin:
                dmValBool = False
            elif mVal > mValMax:
                dmValBool = False
            if dmValBool:
                mValBool = False
            else:
                print("That was an invalid selection. Please try again")
        except:
            print("That was an invalid selection. Please try again")
    return mVal


def mainMenu():
    mValMin = 0
    mValMax = 6
    print("MAIN MENU")
    print("- - - - -")
    print("Please select from the following options:")
    print("   [0] Main Menu ... which is this menu...")
    print("   [1] Find Packing Slips by City?")
    print("   [2] Find Packing Slips by Customer To?")
    print("   [3] Find Packing Slips by Ship To?")
    print("   [4] Find Packing Slips by Sales Order Number?")
    print("   [5] Find Packing Slips by Purchase Order Number?")
    print("   [6] Find Packing Slips by Product?")
    mVal = mValCheck(mValMin,mValMax)
    return mVal
    
        


################################################################################################################################################################
print("Packing Slips Folder Tools v1.0")
menuBool = True
menuVal = 0
while menuBool:
    if menuVal == 0:
        menuVal = mainMenu()
    elif menuVal == 1:
        findByCity()
    else:
        menuVal = 0

    os.system('CLS')

    



#findByCity(2020,1,1,"middletown")

















