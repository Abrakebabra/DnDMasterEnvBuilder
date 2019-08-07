import tkinter as tk  # gui
import functools  # to pass a function with parameters into tkinter button
import yeelight  # lights
import math  # convert color temp to rgb
import os  # to access drive files
import ast  # to read save files

# .get_model_specs() - Find out specs or to wake it up
# .get_properties() - perhaps can use this to wake it up
# .set_brightness()  1-100
# .set_color_temp()  1700-6500
# .set_hsv()  hue 0-359, sat 0-100, v 0-100 (brightness?  Omitted, brightness
# will remain the same)


mode = str()


def modeF():
    global mode
    while not mode:
        print("\"edit\", \"safe\", or \"none\" mode?")
        modeEntry = input()
        if modeEntry == "edit":
            mode = modeEntry
        elif modeEntry == "safe":
            mode = modeEntry
        elif modeEntry == "none":
            mode = modeEntry


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

# modeF()
# lightF()

mode = "edit"
lightCount = 3


class ColorConverter():
    def __init__(self):
        pass

    def rgbHex(self, r, g, b):
        # https://stackoverflow.com/questions/3380726/converting-a-rgb-color-
        # tuple-to-a-six-digit-code-in-python
        return "#%02x%02x%02x" % (int(r), int(g), int(b))

    def complimentary(self, r, g, b):
        red = 255 - int(r)
        green = 255 - int(g)
        blue = 255 - int(b)

        return red, green, blue

    def tempRGB(self, colour_temperature):
        # https://gist.github.com/petrklus/b1f427accdf7438606a6

        # Converts from K to RGB, algorithm courtesy of
        # http://www.tannerhelland.com/4435/
        # convert-temperature-rgb-algorithm-code/

        # range check
        if colour_temperature < 1000:
            colour_temperature = 1000
        elif colour_temperature > 40000:
            colour_temperature = 40000

        tmp_internal = colour_temperature / 100.0

        # red
        if tmp_internal <= 66:
            red = 255
        else:
            tmp_red = 329.698727446 * math.pow(
                tmp_internal - 60, - 0.1332047592)
            if tmp_red < 0:
                red = 0
            elif tmp_red > 255:
                red = 255
            else:
                red = tmp_red

        # green
        if tmp_internal <= 66:
            tmp_green = 99.4708025861 * math.log(
                tmp_internal) - 161.1195681661
            if tmp_green < 0:
                green = 0
            elif tmp_green > 255:
                green = 255
            else:
                green = tmp_green
        else:
            tmp_green = 288.1221695283 * math.pow(
                tmp_internal - 60, -0.0755148492)
            if tmp_green < 0:
                green = 0
            elif tmp_green > 255:
                green = 255
            else:
                green = tmp_green

        # blue
        if tmp_internal >= 66:
            blue = 255
        elif tmp_internal <= 19:
            blue = 0
        else:
            tmp_blue = 138.5177312231 * math.log(
                tmp_internal - 10) - 305.0447927307

            if tmp_blue < 0:
                blue = 0
            elif tmp_blue > 255:
                blue = 255
            else:
                blue = tmp_blue

        return red, green, blue

    def hsvRGB(self, hue, sat, val):
        # https://gist.github.com/mathebox/e0805f72e7db3269ec22
        h = hue / 360
        s = sat / 100
        v = val / 100

        i = math.floor(h * 6)
        f = h * 6 - i
        p = v * (1-s)
        q = v * (1-f * s)
        t = v * (1-(1-f) * s)

        r, g, b = [
            (v, t, p),
            (q, v, p),
            (p, v, t),
            (p, q, v),
            (t, p, v),
            (v, p, q),
        ][int(i % 6)]

        red = int(r * 255)
        green = int(g * 255)
        blue = int(b * 255)

        return red, green, blue


colConv = ColorConverter()


class Lights():

    # Light physical IDs

    # standHigh = "0x0000000007e71dfa"
    # standMid = "0x0000000007e74620"
    # standLow = "0x0000000007e71ffd"
    # clip1 = ""
    # clip2 = ""
    # clip3 = ""

    clip1 = "0x0000000007e71dfa"  # standHigh
    clip2 = "0x0000000007e74620"  # standMid
    clip3 = "0x0000000007e71ffd"  # standLow

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

            if self.lightSetup == "Out" or self.lightSetup == "Home":
                if bulbID == Lights.clip1:
                    self.lt.append({"Light Name": "clip1",
                                    "LightObj": yeelight.Bulb(
                                     self.bulbList[i]["ip"],
                                     effect=transition),
                                    "state": "off", "mode": "temp",
                                    "temp": 5000, "brightness": 100,
                                    "h": 30, "s": 100})
                elif bulbID == Lights.clip2:
                    self.lt.append({"Light Name": "clip2",
                                    "LightObj": yeelight.Bulb(
                                     self.bulbList[i]["ip"],
                                     effect=transition),
                                    "state": "off", "mode": "temp",
                                    "temp": 5000, "brightness": 100,
                                    "h": 30, "s": 100})
                elif bulbID == Lights.clip3:
                    self.lt.append({"Light Name": "clip3",
                                    "LightObj": yeelight.Bulb(
                                     self.bulbList[i]["ip"],
                                     effect=transition),
                                    "state": "off", "mode": "temp",
                                    "temp": 5000, "brightness": 100,
                                    "h": 30, "s": 100})

            if self.lightSetup == "Home":
                if bulbID == Lights.standHigh:
                    self.lt.append({"Light Name": "standHigh",
                                    "LightObj": yeelight.Bulb(
                                     self.bulbList[i]["ip"],
                                     effect=transition),
                                    "state": "off", "mode": "temp",
                                    "temp": 5000, "brightness": 100,
                                    "h": 30, "s": 100})
                elif bulbID == Lights.standMid:
                    self.lt.append({"Light Name": "standMid",
                                    "LightObj": yeelight.Bulb(
                                     self.bulbList[i]["ip"],
                                     effect=transition),
                                    "state": "off", "mode": "temp",
                                    "temp": 5000, "brightness": 100,
                                    "h": 30, "s": 100})
                elif bulbID == Lights.standLow:
                    self.lt.append({"Light Name": "standLow",
                                    "LightObj": yeelight.Bulb(
                                     self.bulbList[i]["ip"],
                                     effect=transition),
                                    "state": "off", "mode": "temp",
                                    "temp": 5000, "brightness": 100,
                                    "h": 30, "s": 100})

    def allOn(self):
        for i in range(0, len(self.lt)):
            light = self.lt[i]
            self.lt[i].update({"state": "on"})
            self.lt[i]["LightObj"].turn_on()

            if light["mode"] == "hsv":
                light["LightObj"].set_hsv(int(light["h"]), int(light["s"]),
                                          int(light["brightness"]))

            elif light["mode"] == "temp":
                light["LightObj"].set_color_temp(int(light["temp"]))
                light["LightObj"].set_brightness(int(light["brightness"]))

    def allOff(self):
        for i in range(0, len(self.lt)):
            self.lt[i].update({"state": "off"})
            self.lt[i]["LightObj"].turn_off()

    def on(self, lightName):
        for i in range(0, len(self.lt)):
            if self.lt[i]["Light Name"] == lightName:
                light = self.lt[i]
                light.update({"state": "on"})
                self.lt[i]["LightObj"].turn_on()
                if light["mode"] == "hsv":
                    light["LightObj"].set_hsv(int(light["h"]), int(light["s"]),
                                              int(light["brightness"]))

                elif light["mode"] == "temp":
                    light["LightObj"].set_color_temp(int(light["temp"]))
                    light["LightObj"].set_brightness(int(light["brightness"]))

    def off(self, lightName):
        for i in range(0, len(self.lt)):
            if self.lt[i]["Light Name"] == lightName:
                self.lt[i].update({"state": "off"})
                self.lt[i]["LightObj"].turn_off()

    def change(self, lightName, r, g, b, brightness):
        for i in range(0, len(self.lt)):
            if self.lt[i]["Light Name"] == lightName:
                self.lt[i]["LightObj"].set_rgb(r, g, b)
                self.lt[i]["LightObj"].set_brightness(brightness)

    def updateHSV(self, lightName, h, s, v):
        for i in range(0, len(self.lt)):
            if self.lt[i]["Light Name"] == lightName:
                self.lt[i].update({"state": "on", "mode": "hsv",
                                   "h": h, "s": s, "brightness": v})

    def updateTemp(self, lightName, temp, br):
        for i in range(0, len(self.lt)):
            if self.lt[i]["Light Name"] == lightName:
                self.lt[i].update({"state": "on", "mode": "temp",
                                   "temp": temp, "brightness": br})

    def sendSettings(self):
        for i in range(0, len(self.lt)):
            light = self.lt[i]

            if self.lt[i]["state"] == "on":
                light["LightObj"].turn_on()

                if light["mode"] == "hsv":
                    light["LightObj"].set_hsv(int(light["h"]), int(light["s"]),
                                              int(light["brightness"]))

                elif light["mode"] == "temp":
                    light["LightObj"].set_color_temp(int(light["temp"]))
                    light["LightObj"].set_brightness(int(light["brightness"]))

            elif self.lt[i]["state"] == "off":
                light["LightObj"].turn_off()


lights = Lights(lightCount)
lights.discover()
lights.assign()
# lights.allOn()


class Presets():

    def __init__(self):
        self.lightSettings = list()

    def savePreset(self, saveFile):
        self.lightSettings = list()  # clears data
        subDirs = os.listdir("CoreLights")

        if lights.lightSetup == "Home":
            for i in subDirs:
                if i == "All":
                    subDir = os.path.join("CoreLights", i)
        elif lights.lightSetup == "Out":
            for i in subDirs:
                if i == "Portable":
                    subDir = os.path.join("CoreLights", i)

        for i in range(0, len(lights.lt)):
            settings = dict()
            lt = lights.lt[i]
            if lt["state"] == "off":
                settings.update({"Light Name": lt["Light Name"],
                                 "state": lt["state"]})
            elif lt["state"] == "on":
                if lt["mode"] == "hsv":
                    settings.update({"Light Name": lt["Light Name"],
                                     "state": lt["state"],
                                     "h": lt["h"], "s": lt["s"],
                                     "brightness": lt["brightness"]})
                elif lt["mode"] == "temp":
                    settings.update({"Light Name": lt["Light Name"],
                                     "state": lt["state"],
                                     "temp": lt["temp"],
                                     "brightness": lt["brightness"]})

            self.lightSettings.append(settings)

        dataLoad = dict()
        onlyData = list()
        for i in range(0, len(self.lightSettings)):
            lightData = dict()
            for k, v in self.lightSettings[i].items():
                lightData.update({k: v})
            onlyData.append(lightData)
        print("Enter preset name:")
        presetName = input()
        presetSaveOK = False

        while presetSaveOK is False:
            print(str(presetName) + " is ok?  Confirm:  y / n")
            presetEntry = input()
            if presetEntry == "y":
                presetSaveOK = True
            elif presetEntry == "n":
                break

        if presetSaveOK is True:
            dataLoad.update({"Preset Name": input(),
                             "Data": onlyData})
            # Wait.... needs to split off 3 or 6 lights...
            filePath = os.path.join(subDir, saveFile)

            with open(filePath, "w") as f:
                f.write(str(dataLoad))

            print("Saved!")

    def loadPreset(self, audioInst, saveFile):
        filePath = os.path.join("CoreSaved", saveFile)
        self.cData = list()
        data = dict()

        with open(filePath, "r") as f:
            data = ast.literal_eval(f.read())

        self.cData = data["Data"]
        aLists = [audioInst.music, audioInst.sounds, audioInst.effects]

        for i in range(0, len(self.cData)):
            for j in range(0, len(aLists)):
                for k in range(0, len(aLists[j])):
                    if self.cData[i]["track"] == aLists[j][k]["track"]:
                        self.cData[i].update({"audioList": aLists[j]})
                        break

        self.playCurrent()


presets = Presets()


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
        return self.c[panel].create_text(x, y, text=words, fill=col)

    def btn(self, panel, words, hlbg, action):
        # Wrapper to shorten button create method
        return tk.Button(self.c[panel], text=words,
                         highlightbackground=hlbg, command=action)

    def controlPanel(self, xPos, yPos, lightName, panel):
        global sW
        global sH

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
                            "slate gray", panel)  # box outline

        lightN = self.text(xPos + row1, yPos + 20,
                           lightName, "light steel blue", panel)

        hText = self.text(xPos + col1 + 25,
                          yPos + row1 - 10,
                          "Hue", "light steel blue", panel)

        entryH = tk.Entry(self.c[panel], width=5)
        entryH.place(x=xPos + col1, y=yPos + row1)

        sText = self.text(xPos + col2 + 25,
                          yPos + row1 - 10,
                          "Sat", "light steel blue", panel)

        entryS = tk.Entry(self.c[panel], width=5)
        entryS.place(x=xPos + col2, y=yPos + row1)

        brightText = self.text(xPos + col3 + 25,
                               yPos + row1 - 10,
                               "Bright", "light steel blue", panel)

        entryBr = tk.Entry(self.c[panel], width=5)
        entryBr.place(x=xPos + col3,
                      y=yPos + row1)

        tempText = self.text(xPos + col2 + 30,
                             yPos + row2 - 10,
                             "Temp", "light steel blue", panel)

        entryTemp = tk.Entry(self.c[panel], width=5)
        entryTemp.place(x=xPos + col2, y=yPos + row2)

        on = self.btn(panel, "On", "slate gray",
                      functools.partial(lights.on, lightName))
        on.place(x=xPos + colL,
                 y=yPos + row3)
        on.config(width=5)

        off = self.btn(panel, "Off", "slate gray",
                       functools.partial(lights.off, lightName))
        off.place(x=xPos + colR,
                  y=yPos + row3)
        off.config(width=5)

        def sendHSV(lightName):
            for i in range(0, len(self.controlBox)):
                if self.controlBox[i]["Light Name"] == lightName:
                    try:
                        h = int(self.controlBox[i]["entryH"].get())
                        s = int(self.controlBox[i]["entryS"].get())
                        v = int(self.controlBox[i]["entryBr"].get())
                        if v == 0:
                            return
                    except ValueError:
                        return
            lights.updateHSV(lightName, h, s, v)
            lights.sendSettings()

        def sendTemp(lightName):
            for i in range(0, len(self.controlBox)):
                if self.controlBox[i]["Light Name"] == lightName:
                    try:
                        temp = int(self.controlBox[i]["entryTemp"].get())
                        bright = int(self.controlBox[i]["entryBr"].get())
                        if bright == 0:
                            return
                    except ValueError:
                        return
            lights.updateTemp(lightName, temp, bright)
            lights.sendSettings()

        setHSV = self.btn(panel, "Set HSV", "slate gray",
                          functools.partial(sendHSV, lightName))
        setHSV.place(x=xPos + col2 - 20,
                     y=yPos + row4)
        setHSV.config(width=10)

        setTempBr = self.btn(panel, "Set Temp + Bright", "slate gray",
                             functools.partial(sendTemp, lightName))
        setTempBr.place(x=xPos + col2 - 40,
                        y=yPos + row5)
        setTempBr.config(width=15)

        panelElements.update({"Outline": outline, "Light Text": lightN,
                              "Light Name": lightName, "panel": panel,
                              "hText": hText, "entryH": entryH,
                              "sText": sText, "entryS": entryS,
                              "brightText": brightText, "entryBr": entryBr,
                              "tempText": tempText, "entryTemp": entryTemp,
                              "on": on, "off": off,
                              "setHSV": setHSV, "setTempBr": setTempBr})

        self.controlBox.append(panelElements)

    def rectangleColors(self):

        def colChange(ctrlBox, j, colOutline, colText):
            self.c[ctrlBox["panel"]].itemconfig(
                ctrlBox["Outline"], fill=colOutline)
            self.controlBox[j]["on"].config(highlightbackground=colOutline)
            self.controlBox[j]["off"].config(highlightbackground=colOutline)
            self.controlBox[j]["setHSV"].config(highlightbackground=colOutline)
            self.controlBox[j]["setTempBr"].config(
                highlightbackground=colOutline)
            self.c[ctrlBox["panel"]].itemconfig(
                ctrlBox["Light Text"], fill=colText)
            self.c[ctrlBox["panel"]].itemconfig(
                ctrlBox["hText"], fill=colText)
            self.c[ctrlBox["panel"]].itemconfig(
                ctrlBox["sText"], fill=colText)
            self.c[ctrlBox["panel"]].itemconfig(
                ctrlBox["brightText"], fill=colText)
            self.c[ctrlBox["panel"]].itemconfig(
                ctrlBox["tempText"], fill=colText)

        for i in range(0, len(lights.lt)):
            light = lights.lt[i]
            if light["state"] == "off":
                for j in range(0, len(self.controlBox)):
                    ctrlBox = self.controlBox[j]
                    if light["Light Name"] == ctrlBox["Light Name"]:
                        colChange(ctrlBox, j, "gray25", "gold2")

            elif light["state"] == "on":
                if light["mode"] == "temp":
                    col1 = colConv.tempRGB(light["temp"])
                    col2 = colConv.complimentary(col1[0], col1[1], col1[2])
                    col1Hex = colConv.rgbHex(col1[0], col1[1], col1[2])
                    col2Hex = colConv.rgbHex(col2[0], col2[1], col2[2])
                    for j in range(0, len(self.controlBox)):
                        ctrlBox = self.controlBox[j]
                        if light["Light Name"] == ctrlBox["Light Name"]:
                            colChange(ctrlBox, j, col1Hex, col2Hex)

                elif light["mode"] == "hsv":
                    col1 = colConv.hsvRGB(light["h"], light["s"],
                                          light["brightness"])
                    col2 = colConv.complimentary(col1[0], col1[1], col1[2])
                    col1Hex = colConv.rgbHex(col1[0], col1[1], col1[2])
                    col2Hex = colConv.rgbHex(col2[0], col2[1], col2[2])
                    for j in range(0, len(self.controlBox)):
                        ctrlBox = self.controlBox[j]
                        if light["Light Name"] == ctrlBox["Light Name"]:
                            colChange(ctrlBox, j, col1Hex, col2Hex)


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
                        sH / 4, boxWidth, boxHeight, "Steelblue2", str(i))


def multiPresetButtons(output, xPos, yPos):
    startX = xPos
    spacing = (sW - startX) / 12
    rowGap = 100
    colNumber = 0
    rowNumber = 0
    coreLightFilesRaw = list()
    coreLightFiles = list()
    subDirs = os.listdir("CoreLights")

    if lights.lightSetup == "Home":
        for i in subDirs:
            if i == "All":
                subDir = os.path.join("CoreLights", i)
                coreLightFilesRaw = os.listdir(subDir)
                break
    elif lights.lightSetup == "Out":
        for i in subDirs:
            if i == "Portable":
                subDir = os.path.join("CoreLights", i)
                coreLightFilesRaw = os.listdir(subDir)
                break

    for i in coreLightFilesRaw:
        if i.endswith(".txt"):
            coreLightFiles.append(i)

    coreLightFiles.reverse()

    for i in range(0, len(coreLightFiles)):
        fileName = str(coreLightFiles[i])
        filePath = str()
        if lights.lightSetup == "Home":
            filePath = os.path.join("CoreLights/All", fileName)
        elif lights.lightSetup == "Out":
            filePath = os.path.join("CoreLights/Portable", fileName)

        presetName = str()
        data = dict()
        with open(filePath, "r") as f:
            data = ast.literal_eval(f.read())
        presetName = data["Preset Name"]

        if colNumber >= 12:
            rowNumber += 1
            colNumber = 0

        xPosition = startX + colNumber * spacing
        yPosition = yPos + rowNumber * rowGap

        def testFunc():
            print("Hola!")

        if mode == "edit":
            saveB = top.btn("No Panel", "Save", "gray",
                            functools.partial(presets.savePreset, str(i + 1)))
            loadB = top.btn("No Panel", presetName, "gray", testFunc)

            output.presetB.append({"SaveB": saveB, "LoadB": loadB})
            output.presetB[i]["SaveB"].place(x=xPosition,
                                             y=yPosition - 15)
            output.presetB[i]["SaveB"].config(width=10)
            output.presetB[i]["LoadB"].place(x=xPosition,
                                             y=yPosition + 15)
            output.presetB[i]["LoadB"].config(width=10)

        elif mode == "safe":
            loadB = top.btn("No Panel", presetName, "gray", testFunc)

            output.presetB.append({"LoadB": loadB})
            output.presetB[i]["LoadB"].place(x=xPosition, y=yPosition)
            output.presetB[i]["LoadB"].config(width=10)

        colNumber += 1


top = Display()
top.newFrCan(0, 0, sW, sH, "grey", "No Panel")


colBarX = sW * 0.2
colBarWidth = sW * 0.6
colBandW = colBarWidth / 72
colBarY = sH * 0.02
hBarCol = 0


for i in range(0, 72):

    hslCol = colConv.hsvRGB(hBarCol, 80, 100)
    hexCol = colConv.rgbHex(hslCol[0], hslCol[1], hslCol[2])
    top.rect(colBarX + i * colBandW, colBarY, colBandW, 15, hexCol, "No Panel")
    hBarCol += 5


colTextSpacing = colBarWidth / 12

hTextCol = 0
for i in range(0, 12):
    hslCol2 = colConv.hsvRGB(hTextCol, 80, 100)
    hexCol2 = colConv.rgbHex(hslCol2[0], hslCol2[1], hslCol2[2])
    top.text(colBarX + i * colTextSpacing, colBarY + 30,
             str(i * 30), hexCol2, "No Panel")
    hTextCol += 30

tempBandW = colBarWidth / 48
tempBarY = sH * 0.08
tempBarCol = 1700

for i in range(0, 48):
    tempCol = colConv.tempRGB(tempBarCol)
    hexCol3 = colConv.rgbHex(tempCol[0], tempCol[1], tempCol[2])
    top.rect(colBarX + i * tempBandW, tempBarY,
             tempBandW, 15, hexCol3, "No Panel")

    tempBarCol += 100

tempTextSpacing = colBarWidth / 6
tempTextCol = 1700
for i in range(0, 6):
    tempCol2 = colConv.tempRGB(tempTextCol)
    hexCol4 = colConv.rgbHex(tempCol2[0], tempCol2[1], tempCol2[2])
    top.text(colBarX + i * tempTextSpacing, tempBarY + 30,
             str(tempTextCol), hexCol4, "No Panel")
    tempTextCol += 800


expl = top.text((sW / 2),
                sH * 0.2,
                "Hue 0-359\
                                        Sat 0-100\
                                        Brightness 0-100\
                                        Temp 1700-6500",
                "aquamarine", "No Panel")


multiPresetButtons(top, 100, sH * 0.7)


lightControl = Display()
multiPanel(lightControl)

lightControl.controlPanel(0, 0, "clip1", "0")
lightControl.controlPanel(0, 0, "clip2", "1")
lightControl.controlPanel(0, 0, "clip3", "2")
lightControl.controlPanel(0, 0, "standHigh", "3")
lightControl.controlPanel(0, 0, "standMid", "4")
lightControl.controlPanel(0, 0, "standLow", "5")


def checkStatus():
    lightControl.rectangleColors()
    root.after(200, checkStatus)


root.after(200, checkStatus)
root.protocol("WM_DELETE_WINDOW", Display.windowClosed)
root.mainloop()
