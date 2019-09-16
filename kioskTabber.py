import pyautogui, time, threading

theTab = 0
nSeconds = 0.1
sleeperTime = 5
timeCounter = 50
timeReCount = 50
waitBool = True
screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()
lastMouseX, lastMouseY = (0,0)

def timerCheck():
    global timeCounter
    global theTab
    global waitBool
    threading.Timer(nSeconds,timerCheck).start()
    if waitBool:
        helloWorld()
    timeCounter = timeCounter - 1
    if timeCounter < 0:
        pyautogui.hotkey('ctrl','tab')
        theTab = (theTab + 1)%3
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
    waitBool = False
    while theTab != 0:
        pyautogui.press('home')
        pyautogui.hotkey('ctrl','tab')
        theTab = (theTab + 1)%3
    waitBool = True
    
time.sleep(5)    
timerCheck()
