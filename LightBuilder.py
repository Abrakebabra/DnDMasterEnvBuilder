import os  # to access local files
import tkinter as tk  # gui
import functools  # to pass a function with parameters into tkinter button
import yeelight  # lights

# .get_model_specs() - Find out specs or to wake it up
# .get_properties() - perhaps can use this to wake it up
# .set_brightness()  1-100
# .set_color_temp()  1700-6500
# .set_hsv()  hue 0-359, sat 0-100, v 0-100 (brightness?  Omitted, brightness
        # will remain the same)
# .RGBTransition(red,green,blue,duration=ms (min 50), brightness=100)


inputLoop = True
lightCount = int()


def lightF():
    global inputLoop
    global lightCount

    while inputLoop is True:
        print("0, 3 or 6 lights?")
        lightCountEntry = input()
        if lightCountEntry == "0":
            lightCount = int(lightCountEntry)
            inputLoop = False
        elif lightCountEntry == "3":
            lightCount = int(lightCountEntry)
            inputLoop = False
        elif lightCountEntry == "6":
            lightCount = int(lightCountEntry)
            inputLoop = False


# lightF()

lightCount = 3


class Lights():

    # Light physical IDs
    standHigh = "0x0000000007e71dfa"
    standMid = "0x0000000007e74620"
    standLow = "0x0000000007e71ffd"
    clip1 = ""
    clip2 = ""
    clip3 = ""

    def __init__(self, lightCount):
        self.bulbList = list()
        self.lt = list()
        self.lightSetup = str()

        if lightCount == 0:
            self.lightSetup = "None"
        elif lightCount == 3:
            self.lightSetup = "Out"
        elif lightCount == 6:
            self.lightSetup = "Home"

    def discover(self):
        global lightCount

        while len(self.bulbList) < lightCount:
            self.bulbList = yeelight.discover_bulbs(timeout=1)
        print(str(len(self.bulbList)) + " bulbs found")

    def assign(self, transition="smooth"):
        # transition can be "smooth" at 300ms or "sudden"
        Lights.lt = list()  # clear assignment

        # assigns bulbs independent of IP address
        for i in range(0, len(self.bulbList)):
            bulbID = self.bulbList[i]["capabilities"]["id"]

            if bulbID == Lights.clip1:
                self.lt.append({"Light Name": "clip1",
                                "LightObj": yeelight.Bulb(
                                 self.bulbList[i]["ip"], effect=transition),
                                "state": "on", "mode": "temp",
                                "temp": 4000, "brightness": 100,
                                "h": 30, "s": 100})
            elif bulbID == Lights.clip2:
                self.lt.append({"Light Name": "clip2",
                                "LightObj": yeelight.Bulb(
                                 self.bulbList[i]["ip"], effect=transition),
                                "state": "on", "mode": "temp",
                                "temp": 4000, "brightness": 100,
                                "h": 30, "s": 100})
            elif bulbID == Lights.clip3:
                self.lt.append({"Light Name": "clip3",
                                "LightObj": yeelight.Bulb(
                                 self.bulbList[i]["ip"], effect=transition),
                                "state": "on", "mode": "temp",
                                "temp": 4000, "brightness": 100,
                                "h": 30, "s": 100})
            elif bulbID == Lights.standHigh:
                self.lt.append({"Light Name": "standHigh",
                                "LightObj": yeelight.Bulb(
                                 self.bulbList[i]["ip"], effect=transition),
                                "state": "on", "mode": "temp",
                                "temp": 4000, "brightness": 100,
                                "h": 30, "s": 100})
            elif bulbID == Lights.standMid:
                self.lt.append({"Light Name": "standMid",
                                "LightObj": yeelight.Bulb(
                                 self.bulbList[i]["ip"], effect=transition),
                                "state": "on", "mode": "temp",
                                "temp": 4000, "brightness": 100,
                                "h": 30, "s": 100})
            elif bulbID == Lights.standLow:
                self.lt.append({"Light Name": "standLow",
                                "LightObj": yeelight.Bulb(
                                 self.bulbList[i]["ip"], effect=transition),
                                "state": "on", "mode": "temp",
                                "temp": 4000, "brightness": 100,
                                "h": 30, "s": 100})

    def allOn(self):
        for i in range(0, len(self.lt)):
            self.lt[i].update({"status": "on"})
            self.lt[i]["LightObj"].turn_on()
            self.lt[i]

    def allOff(self):
        for i in range(0, len(self.lt)):
            self.lt[i].update({"status": "off"})
            self.lt[i]["LightObj"].turn_off()

    def on(self, lightName):
        for i in range(0, len(self.lt)):
            if self.lt[i]["Light Name"] == lightName:
                self.lt[i].update({"status": "on"})
                self.lt[i]["LightObj"].turn_on()

    def off(self, lightName):
        for i in range(0, len(self.lt)):
            if self.lt[i]["Light Name"] == lightName:
                self.lt[i].update({"status": "off"})
                self.lt[i]["LightObj"].turn_off()

    def change(self, lightName, r, g, b, brightness):
        for i in range(0, len(self.lt)):
            if self.lt[i]["Light Name"] == lightName:
                self.lt[i]["LightObj"].set_rgb(r, g, b)
                self.lt[i]["LightObj"].set_brightness(brightness)

    def updateH(self, lightName, h, s, v):
        for i in range(0, len(self.lt)):
            if self.lt[i]["Light Name"] == lightName:
                self.lt[i].update({"status": "on", "mode": "hsv",
                                   "h": h, "s": s, "brightness": v})

    def updateTemp(self, lightName, temp, br):
        for i in range(0, len(self.lt)):
            if self.lt[i]["Light Name"] == lightName:
                self.lt[i].update({"status": "on", "mode": "temp",
                                   "temp": temp, "brightness": br})

    def sendSettings(self):
        pass


lights = Lights(lightCount)
lights.discover()
lights.assign()


def testLight():
    lights.on("standHigh")
    lights.on("standMid")
    lights.on("standLow")
    lights.change("standHigh", 255, 0, 0, 100)
    lights.change("standMid", 255, 0, 0, 100)
    lights.change("standLow", 255, 0, 0, 100)


root = tk.Tk()
getScreenWidth = root.winfo_screenwidth()
getScreenHeight = root.winfo_screenheight()
wRatio = 1
hRatio = 0.97
sW = 1 * getScreenWidth
sH = 0.97 * getScreenHeight
sX = (getScreenWidth / 2) - (sW / 2)  # place Dsp in screen center
sY = 0  # place Dsp at top
root.title("DnD Light Builder")
root.geometry("%dx%d+%d+%d" % (sW, sH, sX, sY))


class Display():

    @classmethod
    def windowClosed(cls):
        global root
        root.destroy()

    def __init__(self):
        self.f = dict()  # frames are all unique so no need for list
        self.c = dict()  # canvases are all unique so no need for list
        self.pb = dict()  # buttons are all unique so no need for list
        self.ab = list()  # may have identical names so list required
        self.controlBox = list()  # holds each track control box
        self.presetB = list()

    def newFrCan(self, xPos, yPos, w, h, col, panel):
        global root

        self.f.update({panel: tk.Frame(root, width=w, height=h, bg=col)})
        self.f[panel].place(x=xPos, y=yPos)

        self.c.update({panel: tk.Canvas(self.f[panel], width=w, height=h,
                      bg=col, highlightthickness=0)})
        self.c[panel].place(x=0, y=0)

    def raiseFrame(self, frame, panel):
        frame[panel].tkraise()

    def rect(self, x, y, w, h, col, panel):
        return self.c[panel].create_rectangle(x, y, x + w, y + h,
                                              fill=col, width=0)

    def text(self, x, y, words, col, panel):
        self.c[panel].create_text(x, y, text=words, fill=col)

    def btn(self, panel, words, hlbg, action):
        # Wrapper to shorten button create method
        return tk.Button(self.c[panel], text=words,
                         highlightbackground=hlbg, command=action)

    def controlPanel(self, xPos, yPos, lightName, panel):
        global sW
        global sH

        def testFunc():
            print("Test")

        gap = 10
        panelWidth = sW
        boxWidth = (panelWidth - gap * 7) / 6
        panelHeight = sH
        boxHeight = panelHeight / 3
        row1 = boxHeight * 0.2
        row2 = boxHeight * 0.4
        row3 = boxHeight * 0.6
        row4 = boxHeight * 0.7
        row5 = boxHeight * 0.8
        col1 = boxWidth * 0.1
        col2 = boxWidth * 0.4
        col3 = boxWidth * 0.7
        colL = boxWidth * 0.2
        colR = boxWidth * 0.6
        panelElements = dict()  # holds current button dict info

        outline = self.rect(xPos, yPos, boxWidth, boxHeight,
                            "SteelBlue1", panel)  # box outline

        lightN = self.text(xPos + row1, yPos + 20,
                           lightName, "steel blue", panel)

        hText = self.text(xPos + col1 + 25,
                          yPos + row1 - 10,
                          "Hue", "steel blue", panel)

        entryH = tk.Entry(self.c[panel], width=5)
        entryH.place(x=xPos + col1, y=yPos + row1)

        sText = self.text(xPos + col2 + 25,
                          yPos + row1 - 10,
                          "Sat", "steel blue", panel)

        entryS = tk.Entry(self.c[panel], width=5)
        entryS.place(x=xPos + col2, y=yPos + row1)

        brightText = self.text(xPos + col3 + 25,
                               yPos + row1 - 10,
                               "Bright", "steel blue", panel)

        entryBr = tk.Entry(self.c[panel], width=5)
        entryBr.place(x=xPos + col3,
                      y=yPos + row1)

        tempText = self.text(xPos + col2 + 30,
                             yPos + row2 - 10,
                             "Temp", "steel blue", panel)

        entryTemp = tk.Entry(self.c[panel], width=5)
        entryTemp.place(x=xPos + col2, y=yPos + row2)

        on = self.btn(panel, "On", "SteelBlue1",
                      functools.partial(lights.on, lightName))
        on.place(x=xPos + colL,
                 y=yPos + row3)
        on.config(width=5)

        off = self.btn(panel, "Off", "SteelBlue1",
                       functools.partial(lights.off, lightName))
        off.place(x=xPos + colR,
                  y=yPos + row3)
        off.config(width=5)

        setHSV = self.btn(panel, "Set HSV", "SteelBlue1",
                          testFunc)
        setHSV.place(x=xPos + col2 - 20,
                     y=yPos + row4)
        setHSV.config(width=10)

        setTempBr = self.btn(panel, "Set Temp + Bright", "SteelBlue1",
                             testFunc)
        setTempBr.place(x=xPos + col2 - 40,
                        y=yPos + row5)
        setTempBr.config(width=15)

        panelElements.update({"Outline": outline, "Light Text": lightN,
                              "Light Name": lightName,
                              "hText": hText, "entryH": entryH,
                              "sText": sText, "entryS": entryS,
                              "brightText": brightText, "entryBr": entryBr,
                              "tempText": tempText, "entryTemp": entryTemp,
                              "on": on, "off": off,
                              "setHSV": setHSV, "setTempBr": setTempBr})

        self.controlBox.append(panelElements)


def multiPanel(output):
    global sW
    global sH
    gap = 10
    panelWidth = sW
    boxWidth = (panelWidth - gap * 7) / 6
    panelHeight = sH
    boxHeight = panelHeight / 3

    for i in range(0, 6):
        output.newFrCan(gap / 2 + (gap * i) + i * ((sW / 6) - gap),
                        sH / 4, boxWidth, boxHeight, "SteelBlue2", str(i))


top = Display()
top.newFrCan(0, 0, sW, sH, "grey", "No Panel")

expl = top.text((sW / 2) - 50,
                sH * 0.2,
                "Hue 0-359\
                            Sat 0-100\
                            Brightness 0-100\
                            Temp 1700-6500",
                "SteelBlue1", "No Panel")

lightControl = Display()
multiPanel(lightControl)

lightControl.controlPanel(0, 0, "clip1", "0")
lightControl.controlPanel(0, 0, "clip2", "1")
lightControl.controlPanel(0, 0, "clip3", "2")
lightControl.controlPanel(0, 0, "standHigh", "3")
lightControl.controlPanel(0, 0, "standMid", "4")
lightControl.controlPanel(0, 0, "standLow", "5")


# def checkStatus():
#     root.after(200, checkStatus)


# root.after(200, checkStatus)
root.protocol("WM_DELETE_WINDOW", Display.windowClosed)
root.mainloop()
