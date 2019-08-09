import tkinter as tk  # gui
import functools  # to pass a function with parameters into tkinter button
import math  # convert color temp to rgb
import os  # to access drive files
import ast  # to read save files
import LightHandler

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


modeF()
lightF()


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


lights = LightHandler.Lights(lightCount)
lights.discover()
lights.assign()


lightRdWrt = LightHandler.LightReadWrite(lights)


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
        self.sceneB = list()

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

    def controlPanel(self, xPos, yPos, lightClsObj, lightName, panel):
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

        def update():
            for i in range(0, len(lightClsObj.lt)):
                lt = lightClsObj.lt[i]
                if lt["Light Name"] == lightName:
                    if lt["state"] == "off":
                        entryH.delete(0, 100)
                        entryS.delete(0, 100)
                        entryBr.delete(0, 100)
                        entryTemp.delete(0, 100)
                    elif lt["state"] == "on":
                        if lt["mode"] == "hsv":
                            entryH.delete(0, 100)
                            entryH.insert(0, lt["h"])
                            entryS.delete(0, 100)
                            entryS.insert(0, lt["s"])
                            entryBr.delete(0, 100)
                            entryBr.insert(0, lt["brightness"])
                            entryTemp.delete(0, 100)
                        elif lt["mode"] == "temp":
                            entryH.delete(0, 100)
                            entryS.delete(0, 100)
                            entryBr.delete(0, 100)
                            entryBr.insert(0, lt["brightness"])
                            entryTemp.delete(0, 100)
                            entryTemp.insert(0, lt["temp"])

        def onUpdate():
            lights.on(lightName)
            update()

        def offUpdate():
            lights.off(lightName)
            update()

        on = self.btn(panel, "On", "slate gray", onUpdate)
        on.place(x=xPos + colL,
                 y=yPos + row3)
        on.config(width=5)

        off = self.btn(panel, "Off", "slate gray", offUpdate)
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
            update()

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
            update()

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
                    col1Brt = 75 + light["brightness"] / 4
                    col1Sat = 25 + light["s"] * 0.75
                    col1 = colConv.hsvRGB(light["h"], col1Sat, col1Brt)
                    colComp = 359 - abs(light["h"] - 180)
                    col2 = colConv.hsvRGB(colComp, 100, 100)
                    col1Hex = colConv.rgbHex(col1[0], col1[1], col1[2])
                    col2Hex = colConv.rgbHex(col2[0], col2[1], col2[2])
                    for j in range(0, len(self.controlBox)):
                        ctrlBox = self.controlBox[j]
                        if light["Light Name"] == ctrlBox["Light Name"]:
                            colChange(ctrlBox, j, col1Hex, col2Hex)

    def loadRWVal(self, lightClsObj, ctrlCanvas, fileName):
        lightRdWrt.loadScene(fileName)

        for i in range(0, len(lightClsObj.lt)):
            lt = lightClsObj.lt[i]

            for j in range(0, len(ctrlCanvas.controlBox)):
                ctrlB = ctrlCanvas.controlBox[j]
                if lt["Light Name"] == ctrlB["Light Name"]:
                    if lt["state"] == "off":
                        ctrlB["entryH"].delete(0, 100)
                        ctrlB["entryS"].delete(0, 100)
                        ctrlB["entryBr"].delete(0, 100)
                        ctrlB["entryTemp"].delete(0, 100)
                    elif lt["state"] == "on":
                        if lt["mode"] == "hsv":
                            ctrlB["entryH"].delete(0, 100)
                            ctrlB["entryH"].insert(0, lt["h"])
                            ctrlB["entryS"].delete(0, 100)
                            ctrlB["entryS"].insert(0, lt["s"])
                            ctrlB["entryBr"].delete(0, 100)
                            ctrlB["entryBr"].insert(0, lt["brightness"])
                            ctrlB["entryTemp"].delete(0, 100)
                        elif lt["mode"] == "temp":
                            ctrlB["entryH"].delete(0, 100)
                            ctrlB["entryS"].delete(0, 100)
                            ctrlB["entryBr"].delete(0, 100)
                            ctrlB["entryBr"].insert(0, lt["brightness"])
                            ctrlB["entryTemp"].delete(0, 100)
                            ctrlB["entryTemp"].insert(0, lt["temp"])


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


def multiSceneButtons(output, xPos, yPos):
    coreLightFilesRaw = list()
    coreLightFiles = list()
    startX = xPos
    spacing = (sW - startX) / 12
    rowGap = 100
    colNumber = 0
    rowNumber = 0

    if lights.lightSetup == "Home":
        subDir = os.path.join("CoreLights", "All")
        coreLightFilesRaw = os.listdir(subDir)
    elif lights.lightSetup == "Out":
        subDir = os.path.join("CoreLights", "Portable")
        coreLightFilesRaw = os.listdir(subDir)

    for i in coreLightFilesRaw:
        if i.endswith(".txt"):
            coreLightFiles.append(i)

        coreLightFiles.sort()

    for i in range(0, len(coreLightFiles)):
        fileName = str(coreLightFiles[i])
        filePath = str()
        if lights.lightSetup == "Home":
            filePath = os.path.join("CoreLights/All", fileName)
        elif lights.lightSetup == "Out":
            filePath = os.path.join("CoreLights/Portable", fileName)

        sceneName = str()
        data = dict()
        with open(filePath, "r") as f:
            data = ast.literal_eval(f.read())
        sceneName = data["Scene Name"]

        if colNumber >= 12:
            rowNumber += 1
            colNumber = 0

        xPosition = startX + colNumber * spacing
        yPosition = yPos + rowNumber * rowGap

        if mode == "edit":
            saveB = top.btn("No Panel", "Save", "gray",
                            functools.partial(lightRdWrt.saveScene, fileName))
            loadB = top.btn("No Panel", sceneName, "gray",
                            functools.partial(top.loadRWVal, lights,
                                              lightControl, fileName))

            output.sceneB.append({"SaveB": saveB, "LoadB": loadB})
            output.sceneB[i]["SaveB"].place(x=xPosition,
                                            y=yPosition - 15)
            output.sceneB[i]["SaveB"].config(width=10)
            output.sceneB[i]["LoadB"].place(x=xPosition,
                                            y=yPosition + 15)
            output.sceneB[i]["LoadB"].config(width=10)

            colNumber += 1

        elif mode == "safe":
            lightsUsed = 0
            for j in range(0, len(data["Data"])):
                if data["Data"][j]["state"] == "on":
                    lightsUsed += 1

            if lightsUsed > 0:
                loadB = top.btn("No Panel", sceneName, "gray",
                                functools.partial(top.loadRWVal, lights,
                                                  lightControl, fileName))

                output.sceneB.append({"LoadB": loadB})
                output.sceneB[i]["LoadB"].place(x=xPosition, y=yPosition)
                output.sceneB[i]["LoadB"].config(width=10)

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
                                        Sat 1-100\
                                        Brightness 1-100\
                                        Temp 1700-6500",
                "aquamarine", "No Panel")


lightControl = Display()
multiPanel(lightControl)

lightControl.controlPanel(0, 0, lights, "clip1", "0")
lightControl.controlPanel(0, 0, lights, "clip2", "1")
lightControl.controlPanel(0, 0, lights, "clip3", "2")
lightControl.controlPanel(0, 0, lights, "standHigh", "3")
lightControl.controlPanel(0, 0, lights, "standMid", "4")
lightControl.controlPanel(0, 0, lights, "standLow", "5")

multiSceneButtons(top, sW * 0.02, sH * 0.7)


def checkStatus():
    lightControl.rectangleColors()
    root.after(200, checkStatus)


root.after(200, checkStatus)
root.protocol("WM_DELETE_WINDOW", Display.windowClosed)
root.mainloop()
