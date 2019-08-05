import os  # to access local files
import tkinter as tk  # gui
import functools  # to pass a function with parameters into tkinter button
import time  # code runs faster than vlc can load.  Adds 0.01s delay
import ast  # to turn string into code that can be evaluated for saved files
import vlc  # audio
import yeelight  # lights


mode = str()


def modeF():
    global mode
    while not mode:
        print("\"create\" or \"game\" mode?")
        modeEntry = input()
        if modeEntry == "create":
            mode = modeEntry
        elif modeEntry == "game":
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

mode = "game"
lightCount = 0


class Media():

    def __init__(self):
        # mimics the structure of directories and files to create the
        # panels and buttons.
        self.music = list()
        self.sounds = list()
        self.effects = list()

    def getMedia(self, inputDir, varList):
        items = os.listdir(inputDir)
        subDirs = list()

        for i in items:
            if os.path.isdir(os.path.join(inputDir, i)):
                subDirs.append(i)

        def storeInfo(path, data, subDir):
            panelGroup = list()

            for j in data:
                fullPath = os.path.join(path, j)
                if j.endswith(".mp3") or\
                   j.endswith(".m4a") or\
                   j.endswith(".wav"):
                    trackName = j[:-4]
                    panelGroup.append({"panel": str(subDir),
                                       "track": str(trackName),
                                       "path": str(fullPath)})

            varList.append(panelGroup)

        if len(subDirs) > 0:
            for i in subDirs:
                subDirPath = os.path.join(inputDir, i)
                items = os.listdir(subDirPath)

                storeInfo(subDirPath, items, i)
        else:
            storeInfo(inputDir, items, "No Panel")

    def printList(self, var):
        for i in range(0, len(var)):
            print("\n" + str(var[i][0]["panel"]) + ":")
            for j in range(0, len(var[i])):
                for k, v in var[i][j].items():
                    print(str(k) + ": " + str(v))
                print("\n")


media = Media()
media.getMedia("CoreMusic", media.music)
media.getMedia("CoreSounds", media.sounds)
media.getMedia("CoreEffects", media.effects)


class Audio():

    def __init__(self):
        self.active = list()  # Holds list of active tracks

        self.music = list()  # Holds "path": vlc.MediaPlayer(path)
        self.sounds = list()  # Holds "path": vlc.MediaPlayer(path)
        self.effects = list()  # Holds "path": vlc.MediaPlayer(path)

    def audioLoader(self, MediaAudio, varList):
        for i in range(0, len(MediaAudio)):
            for j in range(0, len(MediaAudio[i])):
                ma = MediaAudio[i][j]
                trackObj = dict()

                trackObj.update({"panel": ma["panel"],
                                 "track": ma["track"],
                                 "volume": 100,
                                 "vlcObj": vlc.MediaPlayer(ma["path"])})

                varList.append(trackObj)

    def play(self, audioList, track):

        def handleTrack():
            for i in range(0, len(audioList)):
                if audioList[i]["track"] == track:
                    trackObj = audioList[i]
                    self.active.append({"panel": trackObj["panel"],
                                        "audioList": audioList,
                                        "track": trackObj["track"],
                                        "vlcObj": trackObj["vlcObj"]})

                    trackObj["vlcObj"].stop()
                    time.sleep(0.02)  # code runs faster than vlc can load
                    trackObj["vlcObj"].play()
                    time.sleep(0.02)  # code runs faster than vlc can load
                    trackObj["vlcObj"].audio_set_volume(trackObj["volume"])

        if len(self.active) > 0:
            found = False
            for i in range(0, len(self.active)):
                if self.active[i]["track"] == track:
                    found = True

            if found is True:
                return
            else:
                handleTrack()
        else:
            handleTrack()

    def stop(self, audioList, track):
        for i in range(0, len(self.active)):
            if self.active[i]["track"] == track:
                self.active[i]["vlcObj"].stop()
                self.active.pop(i)
                break

    def volume(self, audioList, track, volUpDown):

        def volUp(trackObj):
            currentVol = trackObj["volume"]
            newVol = currentVol + 10
            trackPlaying = trackObj["vlcObj"].get_state() == vlc.State.Playing

            if newVol <= 100:
                trackObj.update({"volume": newVol})
                if trackPlaying:
                    trackObj["vlcObj"].audio_set_volume(trackObj["volume"])
            else:
                if trackPlaying:
                    trackObj["vlcObj"].audio_set_volume(100)

        def volDown(trackObj):
            currentVol = trackObj["volume"]
            newVol = currentVol - 10
            trackPlaying = trackObj["vlcObj"].get_state() == vlc.State.Playing

            if newVol >= 0:
                trackObj.update({"volume": newVol})
                if trackPlaying:
                    trackObj["vlcObj"].audio_set_volume(newVol)
            else:
                if trackPlaying:
                    trackObj["vlcObj"].audio_set_volume(0)

        for i in range(0, len(audioList)):
            if audioList[i]["track"] == track:
                if volUpDown == "up":
                    volUp(audioList[i])
                elif volUpDown == "down":
                    volDown(audioList[i])

    def stopAll(self):

        stopList = list()

        for i in range(0, len(self.active)):
            stopList.append(self.active[i])

        for i in range(0, len(stopList)):
            track = stopList[i]["track"]
            audioList = stopList[i]["audioList"]

            if self.music == audioList:
                self.stop(self.music, track)
            elif self.sounds == audioList:
                self.stop(self.sounds, track)
            elif self.effects == audioList:
                self.stop(self.effects, track)

    def statusCheck(self):
        checkList = list()

        for i in range(0, len(self.active)):
            checkList.append(self.active[i])

        for i in range(0, len(checkList)):
            trackObj = checkList[i]
            state = trackObj["vlcObj"].get_state()

            if state == vlc.State.Ended:
                if trackObj["audioList"] == self.effects:
                    self.stop(trackObj["audioList"], trackObj["track"])
                else:
                    trackObj["vlcObj"].stop()
                    time.sleep(0.02)
                    trackObj["vlcObj"].play()

    def selectTrack(self, audioList, track):
        for i in range(0, len(audioList)):
            if audioList[i]["track"] == track:
                trackObj = audioList[i]
                data = {"panel": trackObj["panel"],
                        "audioList": audioList,
                        "track": trackObj["track"],
                        "volume": trackObj["volume"]}

                if data not in presets.cData:
                    presets.cData.append(data)

    def removeTrack(self, track):
        for i in range(0, len(presets.cData)):
            if presets.cData[i]["track"] == track:
                presets.cData.pop(i)
                break


audio = Audio()
audio.audioLoader(media.music, audio.music)
audio.audioLoader(media.sounds, audio.sounds)
audio.audioLoader(media.effects, audio.effects)


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
                                "r": "?", "g": "?", "b": "?",
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


class Presets():

    def __init__(self):
        self.cData = list()
        self.presets = list()

    def playCurrent(self):
        audio.stopAll()
        for i in range(0, len(self.cData)):
            audioList = self.cData[i]["audioList"]
            track = self.cData[i]["track"]
            volume = self.cData[i]["volume"]

            for j in range(0, len(audioList)):
                if audioList[j]["track"] == track:
                    audioList[j].update({"volume": volume})
                    audio.play(audioList, track)
                    break

    def clearCurrent(self):
        self.cData = list()

    def savePreset(self, saveFile):
        dataLoad = dict()
        cDataNoObject = list()
        for i in range(0, len(self.cData)):
            trackData = dict()
            for k, v in self.cData[i].items():
                if k != "audioList":
                    trackData.update({k: v})
            cDataNoObject.append(trackData)
        print("Enter preset name:")
        dataLoad.update({"Preset Name": input(), "Data": cDataNoObject})
        filePath = os.path.join("CoreSaved", saveFile)

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
space = 50
root.title("DnD Control Board")
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
        return self.c[panel].create_text(x, y, text=words, fill=col)

    def btn(self, panel, words, hlbg, action):
        # Wrapper to shorten button create method
        return tk.Button(self.c[panel], text=words,
                         highlightbackground=hlbg, command=action)

    def panelButton(self, xPos, yPos, words, hlbg, action, panel="No Panel"):
        self.pb.update({words: self.btn(panel, words, hlbg, action)})
        self.pb[words].place(x=xPos, y=yPos)
        self.pb[words].config(width=8)

    def trackCtrlBox(self,
                     xPos, yPos, hlbg,
                     track, vlcObj, audInst, audioList, panel="No Panel"):

        global sW
        global sH
        global space

        gap = 8
        panelWidth = sW * 0.8
        boxWidth = (panelWidth - gap * 6) / 4
        panelHeight = sH - space * 6
        boxHeight = (panelHeight - gap * 9) / 6

        panelElements = dict()  # holds current button dict info

        outline = self.rect(xPos, yPos, boxWidth, boxHeight,
                            "maroon", panel)  # box outline

        trackName = self.text(xPos + boxWidth * 0.5, yPos + 20,
                              track, "LightBlue1", panel)  # track

        selectTrack = self.btn(panel, "Select", hlbg,
                               functools.partial(audInst.selectTrack,
                                                 audioList, track))
        selectTrack.place(x=xPos + boxWidth * 0.02, y=yPos + boxHeight * 0.7,
                          anchor="sw")
        selectTrack.config(width=8)

        removeTrack = self.btn(panel, "Remove", hlbg,
                               functools.partial(audInst.removeTrack, track))
        removeTrack.place(x=xPos + boxWidth * 0.02, y=yPos + boxHeight * 0.98,
                          anchor="sw")
        removeTrack.config(width=8)

        volUp = self.btn(panel, "Vol Up", hlbg,
                         functools.partial(audInst.volume,
                                           audioList, track, "up"))
        volUp.place(x=xPos + boxWidth * 0.3, y=yPos + boxHeight * 0.7,
                    anchor="sw")
        volUp.config(width=8)

        volDown = self.btn(panel, "Vol Down", hlbg,
                           functools.partial(audInst.volume,
                                             audioList, track, "down"))
        volDown.place(x=xPos + boxWidth * 0.3, y=yPos + boxHeight * 0.98,
                      anchor="sw")
        volDown.config(width=8)

        playTrack = self.btn(panel, "Play", hlbg,
                             functools.partial(audInst.play,
                                               audioList, track))
        playTrack.place(x=xPos + boxWidth * 0.98, y=yPos + boxHeight * 0.7,
                        anchor="se")
        playTrack.config(width=8)

        stopTrack = self.btn(panel, "Stop", hlbg,
                             functools.partial(audInst.stop,
                                               audioList, track))
        stopTrack.place(x=xPos + boxWidth * 0.98, y=yPos + boxHeight * 0.98,
                        anchor="se")
        stopTrack.config(width=8)

        panelElements.update({"Outline": outline, "Track Name": trackName,
                              "track": track,
                              "Select": selectTrack, "Remove": removeTrack,
                              "Vol Up": volUp, "Vol Down": volDown,
                              "Play": playTrack, "Stop": stopTrack,
                              "vlcObj": vlcObj, "panel": panel})

        self.controlBox.append(panelElements)

    def isPlaying(self):
        def object(panel, i, col, textCol):
            self.c[panel].itemconfig(self.controlBox[i]["Outline"], fill=col)
            self.c[panel].itemconfig(self.controlBox[i]["Track Name"],
                                     fill=textCol)
            self.controlBox[i]["Select"].config(highlightbackground=col)
            self.controlBox[i]["Remove"].config(highlightbackground=col)
            self.controlBox[i]["Vol Up"].config(highlightbackground=col)
            self.controlBox[i]["Vol Down"].config(highlightbackground=col)
            self.controlBox[i]["Play"].config(highlightbackground=col)
            self.controlBox[i]["Stop"].config(highlightbackground=col)

        for i in range(0, len(self.controlBox)):
            panel = self.controlBox[i]["panel"]
            statePlaying = self.controlBox[i]["vlcObj"].get_state() ==\
                vlc.State.Playing

            loaded = False

            for j in range(0, len(presets.cData)):
                if presets.cData[j]["track"] == self.controlBox[i]["track"]:
                    loaded = True
                    break

            if statePlaying is True and loaded is True:
                object(panel, i, "seagreen1", "steel blue")
            elif statePlaying is True:
                object(panel, i, "sea green", "LightBlue1")
            elif loaded is True:
                object(panel, i, "SteelBlue1", "LightBlue1")
            else:
                object(panel, i, "dark slate blue", "LightBlue1")

    @classmethod
    def windowClosed(cls):
        global root
        root.destroy()


def multiPanel(source, output, x, y, w, h, col):
    for i in range(0, len(source)):
        if len(source[i]) > 0:
            output.newFrCan(x, y, w, h, col, str(source[i][0]["panel"]))


def multiTextLabels(source, output, x, y, col):
    for i in range(0, len(source)):
        if len(source[i]) > 0:
            output.text(x, y, str(source[i][0]["panel"]),
                        col, str(source[i][0]["panel"]))


def multiMenuButtons(source, output, hlbg):
    for i in range(0, len(source.f.keys())):
        frameKey = [key for key in source.f.keys()][i]
        output.panelButton(8 + 90 * i, 15,
                           frameKey, hlbg,
                           functools.partial(source.raiseFrame,
                                             source.f, frameKey))


def multiPresetButtons(output):
    global audio
    global mode

    startX = 400
    spacing = (sW - startX) / 9
    coreSavedFilesRaw = os.listdir("CoreSaved")
    coreSavedFiles = list()

    for i in coreSavedFilesRaw:
        if i.endswith(".txt"):
            coreSavedFiles.append(i)

    coreSavedFiles.reverse()

    for i in range(0, len(coreSavedFiles)):
        fileName = str(coreSavedFiles[i])
        filePath = os.path.join("CoreSaved", fileName)
        presetName = str()
        data = dict()
        with open(filePath, "r") as f:
            data = ast.literal_eval(f.read())
        presetName = data["Preset Name"]

        if mode == "create":
            saveB = top.btn("No Panel", "Save", "pink",
                            functools.partial(presets.savePreset, fileName))
            loadB = top.btn("No Panel", presetName, "pink",
                            functools.partial(presets.loadPreset,
                                              audio, fileName))

            output.presetB.append({"SaveB": saveB, "LoadB": loadB})
            output.presetB[i]["SaveB"].place(x=startX + spacing * i, y=53)
            output.presetB[i]["SaveB"].config(width=10)
            output.presetB[i]["LoadB"].place(x=startX + spacing * i, y=76)
            output.presetB[i]["LoadB"].config(width=10)

        elif mode == "game":
            loadB = top.btn("No Panel", presetName, "pink",
                            functools.partial(presets.loadPreset,
                                              audio, fileName))

            output.presetB.append({"LoadB": loadB})
            output.presetB[i]["LoadB"].place(x=startX + spacing * i, y=65)
            output.presetB[i]["LoadB"].config(width=10)


def multiControlBoxes(output, audInst, audioList):
    global sW
    global sH
    global space

    gap = 8
    columnNumber = 0
    rowNumber = 0

    prevPanel = str()
    panelHeight = sH - space * 6
    boxHeight = (panelHeight - gap * 9) / 6

    for i in range(0, len(audioList)):
        currentPanel = audioList[i]["panel"]
        if prevPanel != currentPanel:
            columnNumber = 0
            rowNumber = 0
            prevPanel = currentPanel

        if space + rowNumber * (boxHeight + space) + boxHeight > sH:
            columnNumber += 1
            rowNumber = 0

        if currentPanel == "No Panel":
            panelWidth = sW * 0.2
            boxWidth = panelWidth - gap * 2
        else:
            panelWidth = sW * 0.6
            boxWidth = (panelWidth - gap * 6) / 3

        xPosition = gap + columnNumber * (boxWidth + gap)
        yPosition = gap * 2 + rowNumber * (boxHeight + gap)
        track = audioList[i]["track"]
        vlcObj = audioList[i]["vlcObj"]

        output.trackCtrlBox(xPosition, yPosition, "red",
                            track, vlcObj, audInst, audioList, currentPanel)

        rowNumber += 1


top = Display()
top.newFrCan(0, 0, sW, space * 5, "grey")

top.text(50, 25, "Title?", "yellow")

top.rect(0, space, sW, space * 2, "pink")
top.text(50, 75, "Presets", "yellow")

playPreset = top.btn("No Panel", "Play", "pink", presets.playCurrent)
playPreset.place(x=100, y=65)
playPreset.config(width=7)
clearPreset = top.btn("No Panel", "Clear",
                      "pink", presets.clearCurrent)
clearPreset.place(x=200, y=65)
clearPreset.config(width=7)
stopAll = top.btn("No Panel", "Silence!", "pink", audio.stopAll)
stopAll.place(x=300, y=65)
stopAll.config(width=7)

megaRed = top.btn("No Panel", "RED!", "orange", testLight)
megaRed.place(x=100, y=150)
megaRed.config(width=7)

multiPresetButtons(top)

top.rect(0, space * 2, sW, space * 2, "orange")
top.text(50, 150, "Lights", "blue")

top.rect(0, space * 4, sW, space, "pink")
top.text(50, space * 4 + space / 2, "Events", "blue")


soundBar = Display()
soundBar.newFrCan(0, space * 5, sW, space, "slate gray")

soundPanel = Display()

multiPanel(media.music, soundPanel,
           0, space * 6,
           sW, sH - space * 6,
           "LightSteelBlue4")

multiPanel(media.sounds, soundPanel,
           0, space * 6,
           sW, sH - space * 6,
           "LightSteelBlue4")

multiPanel(media.effects, soundPanel,
           0, space * 6,
           sW, sH - space * 6,
           "LightSteelBlue4")

multiMenuButtons(soundPanel, soundBar, "slate gray")
multiTextLabels(media.music, soundPanel, 50, 8, "LightBlue2")
multiControlBoxes(soundPanel, audio, audio.music)

multiMenuButtons(soundPanel, soundBar, "slate gray")
multiTextLabels(media.sounds, soundPanel, 50, 8, "LightBlue2")
multiControlBoxes(soundPanel, audio, audio.sounds)

multiMenuButtons(soundPanel, soundBar, "slate gray")
multiTextLabels(media.effects, soundPanel, 50, 8, "LightBlue2")
multiControlBoxes(soundPanel, audio, audio.effects)


def checkStatus():
    audio.statusCheck()
    soundPanel.isPlaying()
    root.after(200, checkStatus)


root.after(200, checkStatus)
root.protocol("WM_DELETE_WINDOW", Display.windowClosed)
root.mainloop()
