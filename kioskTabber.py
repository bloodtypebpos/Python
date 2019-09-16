import pyautogui, time, threading

theTab = 0
nSeconds = 0.2
sleeperTime = 5
timeCounter = 100
timeReCount = 1200
waitBool = True
screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()
lastMouseX, lastMouseY = (0,0)
numTabs = 4

def timerCheck():
    global timeCounter
    global theTab
    global waitBool
    global numTabs
    threading.Timer(nSeconds,timerCheck).start()
    if waitBool:
        helloWorld()
    timeCounter = timeCounter - 1
    if theTab == 2:
        pyautogui.scroll(-5)
    if timeCounter < 0:
        pyautogui.hotkey('ctrl','tab')
        theTab = (theTab + 1)%numTabs
        if theTab == 2:
            pyautogui.press('home')
            timeCounter = 1800
        else:
            timeCounter = timeReCount
    
def helloWorld():
    global lastMouseX
    global lastMouseY
    global theTab
    global timeCounter
    currentMouseX, currentMouseY = pyautogui.position()
    if lastMouseX == currentMouseX:
        if lastMouseY == currentMouseY:
            #pyautogui.hotkey('ctrl','tab')
            #theTab = (theTab + 1)%3
            pass
        else:
            timeCounter = timeReCount
            lastMouseX, lastMouseY = pyautogui.position()
            tabQuit()
    else:
        timeCounter = timeReCount
        lastMouseX, lastMouseY = pyautogui.position()
        tabQuit()
    
def tabQuit():
    global theTab
    global waitBool
    global numTabs
    waitBool = False
    while theTab != 0:
        if theTab != 1:
            pyautogui.press('home')
        pyautogui.hotkey('ctrl','tab')
        theTab = (theTab + 1)%numTabs
    waitBool = True
    
time.sleep(5)    
timerCheck()
