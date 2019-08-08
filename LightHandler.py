import yeelight
import os
import ast


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
        self.lightCount = lightCount

        if self.lightCount == 0:
            self.lightSetup = "None"
        elif self.lightCount == 3:
            self.lightSetup = "Out"
        elif self.lightCount == 6:
            self.lightSetup = "Home"

    def discover(self):

        while len(self.bulbList) < self.lightCount:
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

    def nudge(self):
        for i in range(0, len(self.lt)):
            # wake up lights
            self.lt[i]["LightObj"].get_model_specs()

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


class LightReadWrite():

    def __init__(self, lightClassObj):
        self.lightSettings = list()
        self.lightClsObj = lightClassObj

    def saveScene(self, saveFile):
        self.lightSettings = list()  # clears data

        if self.lightClsObj.lightSetup == "Home":
            subDir = os.path.join("CoreLights", "All")
        elif self.lightClsObj.lightSetup == "Out":
            subDir = os.path.join("CoreLights", "Portable")

        for i in range(0, len(self.lightClsObj.lt)):
            settings = dict()
            lt = self.lightClsObj.lt[i]
            if lt["state"] == "off":
                settings.update({"Light Name": lt["Light Name"],
                                 "state": lt["state"]})
            elif lt["state"] == "on":
                if lt["mode"] == "hsv":
                    settings.update({"Light Name": lt["Light Name"],
                                     "state": lt["state"], "mode": lt["mode"],
                                     "h": lt["h"], "s": lt["s"],
                                     "brightness": lt["brightness"]})
                elif lt["mode"] == "temp":
                    settings.update({"Light Name": lt["Light Name"],
                                     "state": lt["state"], "mode": lt["mode"],
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
        print("Enter scene name:")
        sceneName = input()
        sceneSaveOK = False

        while sceneSaveOK is False:
            print(str(sceneName) + " is ok?  Confirm:  y / n")
            sceneEntry = input()
            if sceneEntry == "y":
                sceneSaveOK = True
            elif sceneEntry == "n":
                break

        if sceneSaveOK is True:
            dataLoad.update({"Scene Name": sceneName,
                             "Data": onlyData})
            filePath = os.path.join(subDir, saveFile)

            with open(filePath, "w") as f:
                f.write(str(dataLoad))

            print("Saved!")

    def loadScene(self, saveFile):

        if self.lightClsObj.lightSetup == "Home":
            subDir = os.path.join("CoreLights", "All")
        elif self.lightClsObj.lightSetup == "Out":
            subDir = os.path.join("CoreLights", "Portable")

        filePath = os.path.join(subDir, saveFile)
        lightData = dict()

        with open(filePath, "r") as f:
            data = ast.literal_eval(f.read())
        lightData = data["Data"]

        self.lightClsObj.nudge()

        for i in range(0, len(lightData)):
            for j in range(0, len(self.lightClsObj.lt)):
                if lightData[i]["Light Name"] ==\
                   self.lightClsObj.lt[j]["Light Name"]:
                    for k, v in lightData[i].items():
                        if k != "Light Name":
                            self.lightClsObj.lt[j].update({k: v})

        self.lightClsObj.sendSettings()
