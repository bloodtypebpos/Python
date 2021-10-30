
from machine import Pin,SPI,PWM
import framebuf
import time
import random

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9



class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 135
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0 # 0 ok     (actually green)
        self.green =   0x001f # 1 ok     (actually blue)
        self.blue  =   0xf800 # 2 ok     (actually red)
        self.white =   0xffff # ok
        self.black =   0x0000 # 3 ok
        self.orange=   0x07f6 # 5 ok
        self.ergoblue =0x06DF #
        self.yellow=   0x9fe0 # 6 ok    0x07ff
        self.pink =    0xF81D # 
        self.purple=   0xffe0 # 4 ok
        self.brown=    0x23cb # 7 ok
        
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)


if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535
    
    
    #------joystck pin declaration-----
    # NOTE: 0 = pressed, 1 = not pressed
    Akey = Pin(15,Pin.IN,Pin.PULL_UP)
    Bkey = Pin(17,Pin.IN,Pin.PULL_UP)
    
    joyUp = Pin(2 ,Pin.IN,Pin.PULL_UP)
    joySelect = Pin(3 ,Pin.IN,Pin.PULL_UP)
    joyLeft = Pin(16 ,Pin.IN,Pin.PULL_UP)
    joyDown = Pin(18 ,Pin.IN,Pin.PULL_UP)
    joyRight = Pin(20 ,Pin.IN,Pin.PULL_UP)
    
    joy = [joyUp,joyRight,joyDown,joyLeft,joySelect,Akey,Bkey]

    LCD = LCD_1inch14()
    #color BRG
    lcdColors = [LCD.red,LCD.green,LCD.blue,LCD.black,LCD.purple,LCD.orange,LCD.yellow,LCD.brown,LCD.ergoblue,LCD.pink]

    joyVal = 0    
    val = 1
    buttonVal = 0
    menuVal = 20
    selectVal = 0
    selectBool = True
    blinkBool = True
    selectVals = [0,1,2,3,4]
    runVals = [90,130,20,5,3,20,100]
    runStatus = ["Moving Up","Resting Up","Moving Down","Resting Down","Short Rest","Long Rest"]
    
        
    def menuHeader(mText):
        LCD.fill(LCD.white)
        LCD.text("MAIN MENU" + mText, 10, 10, LCD.black)
        LCD.text("Select Option:", 20, 20, LCD.black)
        LCD.text("UP/DOWN to select option", 10, 100, LCD.black)
        LCD.text("A-Key to enter selection", 10, 110, LCD.black)
        LCD.text("B-Key to  Main Menu", 10, 120, LCD.black)

    def menuSelector(selectBool,selectVal,selectVals,blinkBool):
        while(selectBool):
            LCD.fill_rect(215,113,20,20,LCD.black)        # use to see selection bottom right corner
            LCD.text(str(selectVal),220,120,LCD.white)    # use to see selection bottom right corner
            if Akey.value() == 0:
                selectVal = selectVals[selectVal]
                selectBool == False
                break
            else:
                if joyUp.value() == 0:
                    selectVal = selectVal - 1
                elif joyDown.value() == 0:
                    selectVal = selectVal + 1
                if selectVal < 0:
                    selectVal = 0
                elif selectVal >= len(selectVals):
                    selectVal = len(selectVals)-1
                if(blinkBool):
                    LCD.fill_rect(20,selectVal*10 + 30, 10, 8, LCD.red)
                else:
                    LCD.fill_rect(20, 30, 10, 65, LCD.white)
                blinkBool = not blinkBool
                time.sleep(0.1)
            LCD.show()
        return selectVal

    def mainMenu():
        selectVal = 0
        selectVals = [10,20,30,40,0]
        selectBool = True
        blinkBool = True
        menuHeader("")
        LCD.text("[1] Run Cycle Test", 30, 30, LCD.black)
        LCD.text("[2] Edit Cycle Test", 30, 40, LCD.black)
        LCD.text("[3] View Cycle Stats", 30, 50, LCD.black)
        LCD.text("[4] Save Report", 30, 60, LCD.black)
        LCD.text("[5] Return", 30, 70, LCD.black)
        selectVal = menuSelector(selectBool,selectVal,selectVals,blinkBool)
        return selectVal

        

    def editCycleTest():
        selectVal = 0
        selectBool = True
        blinkBool = True

        while(selectBool):
            menuHeader(" > EDIT CYCLE TEST")
            LCD.text("UP       | " + str(runVals[0]), 30, 30, LCD.black)
            LCD.text("UP REST  | " + str(runVals[1]), 30, 40, LCD.black)
            LCD.text("DOWN     | " + str(runVals[2]), 30, 50, LCD.black)
            LCD.text("DOWN REST| " + str(runVals[3]), 30, 60, LCD.black)
            LCD.text("CYCLES   | " + str(runVals[4]), 30, 70, LCD.black)
            LCD.text("LONG REST| " + str(runVals[5]), 30, 80, LCD.black)
            LCD.text("SAVE SETTINGS AND RETURN", 30, 90, LCD.black)
            LCD.fill_rect(215,113,20,20,LCD.black)        # use to see selection bottom right corner
            LCD.text(str(selectVal),220,120,LCD.white)    # use to see selection bottom right corner
            if Akey.value() == 0:
                selectBool == False
                return selectVal
            else:
                if joyLeft.value() == 0:
                    runVals[selectVal] = runVals[selectVal] - 1
                elif joyRight.value() == 0:
                    runVals[selectVal] = runVals[selectVal] + 1
                elif joyUp.value() == 0:
                    selectVal = selectVal - 1
                elif joyDown.value() == 0:
                    selectVal = selectVal + 1
                if selectVal < 0:
                    selectVal = 0
                elif selectVal > 6:
                    selectVal = 6
                if(blinkBool):
                    LCD.fill_rect(20,selectVal*10 + 30, 10, 8, LCD.red)
                else:
                    LCD.fill_rect(20, 30, 10, 70, LCD.white)
                blinkBool = not blinkBool
                time.sleep(0.1)
            LCD.show()        
        
    
    
    while(1):
        time.sleep(0.25)
        if menuVal == 0:
            menuVal = mainMenu()
        elif menuVal == 20:
            menuVal = editCycleTest()
        else:
            menuVal = mainMenu()
            
    
    
    
    
r"""    
    LCD.hline(10,10,220,LCD.blue)
    LCD.hline(10,125,220,LCD.blue)
    LCD.vline(10,10,115,LCD.blue)
    LCD.vline(230,10,115,LCD.blue)
    
    
    LCD.rect(12,12,20,20,LCD.red)
    LCD.rect(12,103,20,20,LCD.red)
    LCD.rect(208,12,20,20,LCD.red)
    LCD.rect(208,103,20,20,LCD.red)
    
    LCD.show()
    key0 = Pin(15,Pin.IN)
    key1 = Pin(17,Pin.IN)
    key2 = Pin(2 ,Pin.IN)
    key3 = Pin(3 ,Pin.IN)
    while(1):
        if(key0.value() == 0):
            LCD.fill_rect(12,12,20,20,LCD.red)
        else :
            LCD.fill_rect(12,12,20,20,LCD.white)
            LCD.rect(12,12,20,20,LCD.red)
            
        if(key1.value() == 0):
            LCD.fill_rect(12,103,20,20,LCD.red)
        else :
            LCD.fill_rect(12,103,20,20,LCD.white)
            LCD.rect(12,103,20,20,LCD.red)
            
        if(key2.value() == 0):
            LCD.fill_rect(208,12,20,20,LCD.red)
        else :
            LCD.fill_rect(208,12,20,20,LCD.white)
            LCD.rect(208,12,20,20,LCD.red)
            
        if(key3.value() == 0):
            LCD.fill_rect(208,103,20,20,LCD.red)
        else :
            LCD.fill_rect(208,103,20,20,LCD.white)
            LCD.rect(208,103,20,20,LCD.red)
            
            
        LCD.show()
    time.sleep(1)
    LCD.fill(0xFFFF)

"""
