import os  # to access local files
import tkinter as tk  # gui
import functools  # to pass a function with parameters into tkinter button
import time  # code runs faster than vlc can load.  Adds 0.01s delay
import ast  # to turn string into code that can be evaluated for saved files
import vlc  # audio
import LightHandler  # Other program written to handle lights - Classes only


# color control

# top master bar
topCol = "slate gray"
topTCol = "yellow"
# audio presets bar
row1BarCol = "gray"

# lights bar
row2BarCol = "slate gray"

# audio light text
soundTCol = "aquamarine"
lightTCol = "yellow"

# events bar
evntBarCol = "gray"
evntTBarCol = "aquamarine"

# panel selection bar
pnlBarCol = "cyan"

# panels
pnlCol = "LightSteelBlue4"
pnlTCol = "LightBlue2"

# control box stopped
ctrlStopCol = "dark slate blue"
ctrlTStopCol = "LightBlue1"

# control box playing
ctrlPlayCol = "sea green"
ctrlTPlayCol = "LightBlue1"

# control box selected
ctrlSelCol = "SteelBlue1"
ctrlTSelCol = "LightBlue1"

# control box selected and playing
ctrlSelPlayCol = "seagreen1"
ctrlTSelPlayCol = "steel blue"


mode = str()


def modeF():
    global mode
    while not mode:
        print("\"edit\" or \"game\" mode?")
        modeEntry = input()
        if modeEntry == "edit":
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


modeF()
lightF()


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
        items.sort()

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
                items.sort()

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

    def pause(self):
        for i in range(0, len(self.active)):
            if self.active[i]["vlcObj"].get_state() == vlc.State.Playing:
                self.active[i]["vlcObj"].pause()
            else:
                self.active[i]["vlcObj"].play()

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

                if data not in audioRdWrt.audSel:
                    audioRdWrt.audSel.append(data)

    def removeTrack(self, track):
        for i in range(0, len(audioRdWrt.audSel)):
            if audioRdWrt.audSel[i]["track"] == track:
                audioRdWrt.audSel.pop(i)
                break


audio = Audio()
audio.audioLoader(media.music, audio.music)
audio.audioLoader(media.sounds, audio.sounds)
audio.audioLoader(media.effects, audio.effects)


lights = LightHandler.Lights(lightCount)


def findLights():
    lights.discover()
    lights.assign()


findLights()


class AudioReadWrite():

    def __init__(self):
        self.audSel = list()

    def playAudSel(self):
        audio.stopAll()
        for i in range(0, len(self.audSel)):
            audioList = self.audSel[i]["audioList"]
            track = self.audSel[i]["track"]
            volume = self.audSel[i]["volume"]

            for j in range(0, len(audioList)):
                if audioList[j]["track"] == track:
                    audioList[j].update({"volume": volume})
                    audio.play(audioList, track)
                    break

    def clearAudSel(self):
        self.audSel = list()

    def saveAudSel(self, saveFile):
        dataLoad = dict()
        cDataNoObject = list()
        for i in range(0, len(self.audSel)):
            trackData = dict()
            for k, v in self.audSel[i].items():
                if k != "audioList":
                    trackData.update({k: v})
            cDataNoObject.append(trackData)
        print("Enter preset name:")
        presetName = input()
        presetSaveOK = False

        while presetSaveOK is False:
            print(str(presetName) + " is ok?  Confirm:  y / n")
            sceneEntry = input()
            if sceneEntry == "y":
                presetSaveOK = True
            elif sceneEntry == "n":
                break

        if presetSaveOK is True:
            dataLoad.update({"Preset Name": presetName, "Data": cDataNoObject})
            filePath = os.path.join("CoreSaved", saveFile)

            with open(filePath, "w") as f:
                f.write(str(dataLoad))

            print("Saved!")

    def loadAudSel(self, audioInst, saveFile):
        filePath = os.path.join("CoreSaved", saveFile)
        self.audSel = list()
        data = dict()

        with open(filePath, "r") as f:
            data = ast.literal_eval(f.read())

        self.audSel = data["Data"]
        aLists = [audioInst.music, audioInst.sounds, audioInst.effects]

        for i in range(0, len(self.audSel)):
            for j in range(0, len(aLists)):
                for k in range(0, len(aLists[j])):
                    if self.audSel[i]["track"] == aLists[j][k]["track"]:
                        self.audSel[i].update({"audioList": aLists[j]})
                        break

        self.playAudSel()


audioRdWrt = AudioReadWrite()
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
        self.presetB = list()  # audio environment buttons
        self.sceneB = list()  # light environment buttons

    def newFrCan(self, xPos, yPos, w, h, col, panel="No Panel"):
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

        gap = 8
        panelWidth = sW * 0.8
        boxWidth = (panelWidth - gap * 6) / 4
        panelHeight = sH - space * 6
        boxHeight = (panelHeight - gap * 9) / 6

        panelElements = dict()  # holds current button dict info

        outline = self.rect(xPos, yPos, boxWidth, boxHeight,
                            ctrlStopCol, panel)  # box outline

        trackName = self.text(xPos + boxWidth * 0.5, yPos + 20,
                              track, ctrlTStopCol, panel)  # track

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

            for j in range(0, len(audioRdWrt.audSel)):
                if audioRdWrt.audSel[j]["track"] ==\
                   self.controlBox[i]["track"]:
                    loaded = True
                    break

            if statePlaying is True and loaded is True:
                object(panel, i, ctrlSelPlayCol, ctrlTSelPlayCol)
            elif statePlaying is True:
                object(panel, i, ctrlPlayCol, ctrlTPlayCol)
            elif loaded is True:
                object(panel, i, ctrlSelCol, ctrlTSelCol)
            else:
                object(panel, i, ctrlStopCol, ctrlTStopCol)

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
        output.panelButton(8 + 90 * i, space * 5 + 15,
                           frameKey, hlbg,
                           functools.partial(source.raiseFrame,
                                             source.f, frameKey))


def multiPresetButtons(output, xPos, yPos):
    startX = xPos
    spacing = (sW - startX) / 12
    rowGap = 100
    colNumber = 0
    rowNumber = 0
    bCount = 0
    buttonCol = row1BarCol
    coreSavedFilesRaw = os.listdir("CoreSaved")
    coreSavedFiles = list()

    for i in coreSavedFilesRaw:
        if i.endswith(".txt"):
            coreSavedFiles.append(i)

    coreSavedFiles.sort()

    for i in range(0, len(coreSavedFiles)):
        fileName = str(coreSavedFiles[i])
        filePath = os.path.join("CoreSaved", fileName)
        presetName = str()
        data = dict()
        with open(filePath, "r") as f:
            data = ast.literal_eval(f.read())
        presetName = data["Preset Name"]

        if colNumber >= 12:
            rowNumber += 1
            colNumber = 0

        if bCount >= 12:
            buttonCol = row2BarCol

        xPosition = startX + colNumber * spacing
        yPosition = yPos + rowNumber * rowGap

        if mode == "edit":
            saveB = top.btn("No Panel", "Save", buttonCol,
                            functools.partial(audioRdWrt.saveAudSel, fileName))
            loadB = top.btn("No Panel", presetName, buttonCol,
                            functools.partial(audioRdWrt.loadAudSel,
                                              audio, fileName))

            output.presetB.append({"SaveB": saveB, "LoadB": loadB})
            output.presetB[bCount]["SaveB"].place(x=xPosition,
                                                  y=yPosition - 12)
            output.presetB[bCount]["SaveB"].config(width=10)
            output.presetB[bCount]["LoadB"].place(x=xPosition,
                                                  y=yPosition + 11)
            output.presetB[bCount]["LoadB"].config(width=10)

            colNumber += 1
            bCount += 1

        elif mode == "game":
            if len(data["Data"]) > 0:
                loadB = top.btn("No Panel", presetName, buttonCol,
                                functools.partial(audioRdWrt.loadAudSel,
                                                  audio, fileName))

                output.presetB.append({"LoadB": loadB})
                output.presetB[bCount]["LoadB"].place(x=xPosition, y=yPosition)
                output.presetB[bCount]["LoadB"].config(width=10)

                colNumber += 1
                bCount += 1

    output.text(xPos - 50, yPos + 11, "Sound", soundTCol)
    if bCount > 12:
        output.text(xPos - 50, yPos + rowGap + 11, "Sound", soundTCol)


def multiControlBoxes(output, audInst, audioList):
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

        panelWidth = sW * 0.6
        boxWidth = (panelWidth - gap * 6) / 3

        xPosition = gap + columnNumber * (boxWidth + gap)
        yPosition = 10 + gap * 2 + rowNumber * (boxHeight + gap)
        track = audioList[i]["track"]
        vlcObj = audioList[i]["vlcObj"]

        output.trackCtrlBox(xPosition, yPosition, ctrlStopCol,
                            track, vlcObj, audInst, audioList, currentPanel)

        rowNumber += 1


def multiSceneButtons(output, xPos, yPos):
    coreLightFilesRaw = list()
    coreLightFiles = list()
    startX = xPos
    spacing = (sW - startX) / 12
    rowGap = 100
    colNumber = 0
    rowNumber = 0
    bCount = 0
    buttonCol = row1BarCol

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

        if bCount >= 12:
            buttonCol = row2BarCol

        xPosition = startX + colNumber * spacing
        yPosition = yPos + rowNumber * rowGap

        lightsUsed = 0
        for j in range(0, len(data["Data"])):
            if data["Data"][j]["state"] == "on":
                lightsUsed += 1

        if lightsUsed > 0:
            loadB = top.btn("No Panel", sceneName, buttonCol,
                            functools.partial(lightRdWrt.loadScene, fileName))

            output.sceneB.append({"LoadB": loadB})
            output.sceneB[bCount]["LoadB"].place(x=xPosition, y=yPosition)
            output.sceneB[bCount]["LoadB"].config(width=10)

            colNumber += 1
            bCount += 1

    output.text(xPos - 50, yPos + 11, "Lights", lightTCol)
    if bCount > 12:
        output.text(xPos - 50, yPos + rowGap + 11, "Lights", lightTCol)


# Top canvas
top = Display()
top.newFrCan(0, 0, sW, space * 6, topCol)

# Top master bar
top.rect(0, 0, sW, space, topCol)
top.text(50, 25, "Master", topTCol)
playPreset = top.btn("No Panel", "Play", topCol, audioRdWrt.playAudSel)
playPreset.place(x=100, y=15)
playPreset.config(width=8)
pauseAll = top.btn("No Panel", "Un|Pause", topCol, audio.pause)
pauseAll.place(x=200, y=15)
pauseAll.config(width=8)
clearPreset = top.btn("No Panel", "Clear", topCol, audioRdWrt.clearAudSel)
clearPreset.place(x=300, y=15)
clearPreset.config(width=8)
stopAll = top.btn("No Panel", "Silence!", topCol, audio.stopAll)
stopAll.place(x=400, y=15)
stopAll.config(width=8)
fixLights = top.btn("No Panel", "Fix Lights", topCol, findLights)
fixLights.place(x=sW - 150, y=15)
fixLights.config(width=10)


top.rect(0, space, sW, space * 2, row1BarCol)
top.rect(0, space * 3, sW, space * 2, row2BarCol)

# Top sound bar
multiPresetButtons(top, 100, 75)

# Top light bar
lightBarYPos = 105
if mode == "edit":
    lightBarYPos += 4

multiSceneButtons(top, 100, lightBarYPos)

# Panel menu rectangle
top.rect(0, space * 5, sW, space, pnlBarCol)

# Sound panels
soundPanel = Display()

multiPanel(media.music, soundPanel,
           0, space * 6,
           sW, sH - space * 6,
           pnlCol)

multiPanel(media.sounds, soundPanel,
           0, space * 6,
           sW, sH - space * 6,
           pnlCol)

multiPanel(media.effects, soundPanel,
           0, space * 6,
           sW, sH - space * 6,
           pnlCol)

multiMenuButtons(soundPanel, top, pnlBarCol)
multiTextLabels(media.music, soundPanel, 50, 14, pnlTCol)
multiControlBoxes(soundPanel, audio, audio.music)

multiMenuButtons(soundPanel, top, pnlBarCol)
multiTextLabels(media.sounds, soundPanel, 50, 14, pnlTCol)
multiControlBoxes(soundPanel, audio, audio.sounds)

multiMenuButtons(soundPanel, top, pnlBarCol)
multiTextLabels(media.effects, soundPanel, 50, 14, pnlTCol)
multiControlBoxes(soundPanel, audio, audio.effects)


def checkStatus():
    audio.statusCheck()
    soundPanel.isPlaying()
    root.after(200, checkStatus)


root.after(200, checkStatus)
root.protocol("WM_DELETE_WINDOW", Display.windowClosed)
root.mainloop()
