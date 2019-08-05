import os  # to access local files
import tkinter as tk  # gui
import functools  # to pass a function with parameters into tkinter button
import yeelight  # lights

# .get_model_specs() - Find out specs or to wake it up
# .get_properties() - perhaps can use this to wake it up
# .set_brightness()  1-100
# .set_rgb()  0-255
# .set_color_temp()  1700-6500
# .set_hsv()  hue 0-359, sat 0-100, v 0-100 (brightness?  Omitted, brightness
        # will remain the same)
# .RGBTransition(red,green,blue,duration=ms (min 50), brightness=100)



lightCount = int()
while lightCount is False:
    print("0, 3 or 6 lights?")
    entry = input()
    if entry == 0:
        lightCount = entry
    elif entry == 3:
        lightCount = entry
    elif entry == 6:
        lightCount = entry


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
                                "state": "off", "brightness": 100,
                                "r": 10, "g": 9, "b": 9,
                                "h": "?", "s": "?", "v": "?"})
            elif bulbID == Lights.clip2:
                self.lt.append({"Light Name": "clip2",
                                "LightObj": yeelight.Bulb(
                                 self.bulbList[i]["ip"], effect=transition)})
            elif bulbID == Lights.clip3:
                self.lt.append({"Light Name": "clip3",
                                "LightObj": yeelight.Bulb(
                                 self.bulbList[i]["ip"], effect=transition)})
            elif bulbID == Lights.standHigh:
                self.lt.append({"Light Name": "standHigh",
                                "LightObj": yeelight.Bulb(
                                 self.bulbList[i]["ip"], effect=transition)})
            elif bulbID == Lights.standMid:
                self.lt.append({"Light Name": "standMid",
                                "LightObj": yeelight.Bulb(
                                 self.bulbList[i]["ip"], effect=transition)})
            elif bulbID == Lights.standLow:
                self.lt.append({"Light Name": "standLow",
                                "LightObj": yeelight.Bulb(
                                 self.bulbList[i]["ip"], effect=transition)})

    def allOn(self):
        for i in range(0, len(self.lt)):
            self.lt[i]["LightObj"].turn_on()
            self.lt[i]

    def allOff(self):
        for i in range(0, len(self.lt)):
            self.lt[i]["LightObj"].turn_off()

    def on(self, lightName):
        for i in range(0, len(self.lt)):
            if self.lt[i]["Light Name"] == lightName:
                self.lt[i]["LightObj"].turn_on()

    def off(self, lightName):
        for i in range(0, len(self.lt)):
            if self.lt[i]["Light Name"] == lightName:
                self.lt[i]["LightObj"].turn_off()

    def change(self, lightName, r, g, b, brightness):
        for i in range(0, len(self.lt)):
            if self.lt[i]["Light Name"] == lightName:
                self.lt[i]["LightObj"].set_rgb(r, g, b)
                self.lt[i]["LightObj"].set_brightness(brightness)


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
space = 50
root.title("DnD Light Builder")
root.geometry("%dx%d+%d+%d" % (sW, sH, sX, sY))

class Display():

    def __init__(self):
        self.f = dict()  # frames are all unique so no need for list
        self.c = dict()  # canvases are all unique so no need for list
        self.pb = dict()  # buttons are all unique so no need for list
        self.ab = list()  # may have identical names so list required
        self.controlBox = list()  # holds each track control box
        self.presetB = list()

    def newFrCan(self, xPos, yPos, w, h, col, panel="No Panel"):
        global root

        self.f.update({panel: tk.Frame(root, width=w, height=h, bg=col)})
        self.f[panel].place(x=xPos, y=yPos)

        self.c.update({panel: tk.Canvas(self.f[panel], width=w, height=h,
                      bg=col, highlightthickness=0)})
        self.c[panel].place(x=0, y=0)

    def raiseFrame(self, frame, panel="No Panel"):
        frame[panel].tkraise()

    def rect(self, x, y, w, h, col, panel="No Panel"):
        return self.c[panel].create_rectangle(x, y, x + w, y + h,
                                              fill=col, width=0)

    def text(self, x, y, words, col, panel="No Panel"):
        self.c[panel].create_text(x, y, text=words, fill=col)

    def btn(self, panel, words, hlbg, action):
        # Wrapper to shorten button create method
        return tk.Button(self.c[panel], text=words,
                         highlightbackground=hlbg, command=action)

    @classmethod
    def windowClosed(cls):
        global root
        root.destroy()



top = Display()
top.newFrCan(0, 0, sW, sH, "grey")

def checkStatus():
    audio.statusCheck()
    soundPanel.isPlaying()
    effectsPanel.isPlaying()
    root.after(200, checkStatus)


root.after(200, checkStatus)
root.protocol("WM_DELETE_WINDOW", Display.windowClosed)
root.mainloop()
