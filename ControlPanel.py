import os  # to access local files
import tkinter as tk  # gui
import functools  # to pass a function with parameters into tkinter button
import vlc  # audio
import time  # code runs faster than vlc can load.  Adds 0.01s delay
# import PIL  # for pictures
# import yeelight  # lights


class Media():

    def __init__(self):
        # mimics the structure of directories and files to create the
        # panels and buttons.
        self.music = list()
        self.sounds = list()
        self.effects = list()
        self.genID = 0

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
                                       "path": str(fullPath),
                                       "trackID": str(self.genID)})
                self.genID += 1

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
                                 "trackID": ma["trackID"],
                                 "volume": 100,
                                 "vlcObj": vlc.MediaPlayer(ma["path"])})

                varList.append(trackObj)

    def play(self, audioList, trackID):

        def handleTrack():
            for i in range(0, len(audioList)):
                if audioList[i]["trackID"] == trackID:
                    trackObj = audioList[i]
                    self.active.append({"panel": trackObj["panel"],
                                        "audioList": audioList,
                                        "track": trackObj["track"],
                                        "trackID": trackObj["trackID"],
                                        "vlcObj": trackObj["vlcObj"]})

                    trackObj["vlcObj"].stop()
                    time.sleep(0.01)  # code runs faster than vlc can load
                    trackObj["vlcObj"].play()
                    time.sleep(0.01)  # code runs faster than vlc can load
                    trackObj["vlcObj"].audio_set_volume(trackObj["volume"])

        if len(self.active) > 0:
            found = False
            for i in range(0, len(self.active)):
                if self.active[i]["trackID"] == trackID:
                    found = True

            if found is True:
                return
            else:
                handleTrack()
        else:
            handleTrack()

    def stop(self, audioList, trackID):
        for i in range(0, len(self.active)):
            if self.active[i]["trackID"] == trackID:
                self.active[i]["vlcObj"].stop()
                self.active.pop(i)
                break

    def volume(self, audioList, trackID, volUpDown):

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
            if audioList[i]["trackID"] == trackID:
                if volUpDown == "up":
                    volUp(audioList[i])
                elif volUpDown == "down":
                    volDown(audioList[i])

    def stopAll(self):

        stopList = list()

        for i in range(0, len(self.active)):
            stopList.append(self.active[i])

        for i in range(0, len(stopList)):
            trackID = stopList[i]["trackID"]
            audioList = stopList[i]["audioList"]

            if self.music == audioList:
                self.stop(self.music, trackID)
            elif self.sounds == audioList:
                self.stop(self.sounds, trackID)
            elif self.effects == audioList:
                self.stop(self.effects, trackID)

    def statusCheck(self):
        checkList = list()

        for i in range(0, len(self.active)):
            checkList.append(self.active[i])

        for i in range(0, len(checkList)):
            trackObj = checkList[i]
            state = trackObj["vlcObj"].get_state()

            if state == vlc.State.Ended:
                if trackObj["panel"] == "No Panel":
                    self.stop(trackObj["audioList"], trackObj["trackID"])
                else:
                    trackObj["vlcObj"].stop()
                    time.sleep(0.01)
                    trackObj["vlcObj"].play()


audio = Audio()
audio.audioLoader(media.music, audio.music)
audio.audioLoader(media.sounds, audio.sounds)
audio.audioLoader(media.effects, audio.effects)


class TestAudio():

    def __init__(self, trackID="0"):
        self.trackID = trackID

    def play(self):
        audio.play(audio.music, self.trackID)

    def stop(self):
        audio.stop(audio.music, self.trackID)

    def getvol(self):
        for i in range(0, len(audio.music)):
            if audio.music[i]["trackID"] == self.trackID:
                print(str(audio.music[i]["volume"]))

    def volup(self):
        audio.volume(audio.music, self.trackID, "up")
        self.getvol()

    def voldown(self):
        audio.volume(audio.music, self.trackID, "down")
        self.getvol()

    def startmulti(self):
        audio.play(audio.music, "0")
        audio.play(audio.music, "1")
        audio.play(audio.sounds, "14")

    def stopall(self):
        audio.stopAll()


test = TestAudio()


class Lights():

    def __init__(self):
        pass


class Presets():

    def __init__(self):
        self.currentData = list()

    def playCurrent(self):
        pass

    def clearCurrent(self):
        pass

    def savePreset(self):
        # save, then re-scan file and re-fresh?
        pass

    def loadPreset(self):
        pass


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
        return self.c[panel].create_rectangle(x, y, x + w, y + h, fill=col, width=0)

    def text(self, x, y, words, col, panel="No Panel"):
        self.c[panel].create_text(x, y, text=words, fill=col)

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
                     track, trackID, vlcObj,
                     audInst, audioList, panel="No Panel"):

        global sW
        global sH
        global space

        gap = 8
        if panel == "No Panel":
            panelWidth = sW * 0.2
            boxWidth = panelWidth - gap * 2
        else:
            panelWidth = sW * 0.6
            boxWidth = (panelWidth - gap * 6) / 3

        panelHeight = sH - space * 6
        boxHeight = (panelHeight - gap * 9) / 6

        panelElements = dict()  # holds current button dict info

        outline = self.rect(xPos, yPos, boxWidth, boxHeight,
                            "red", panel)  # box outline
        trackName = self.text(xPos + boxWidth * 0.5, yPos + 20,
                              track, "black", panel)  # track

        def testFunc():
            print("yes")

        selectTrack = self.btn(panel, "Select", hlbg,
                               testFunc)
        selectTrack.place(x=xPos + boxWidth * 0.02, y=yPos + boxHeight * 0.7,
                          anchor="sw")
        selectTrack.config(width=8)

        removeTrack = self.btn(panel, "Remove", hlbg,
                               testFunc)
        removeTrack.place(x=xPos + boxWidth * 0.02, y=yPos + boxHeight * 0.98,
                          anchor="sw")
        removeTrack.config(width=8)

        volUp = self.btn(panel, "Vol Up", hlbg,
                         functools.partial(audInst.volume,
                                           audioList, trackID, "up"))
        volUp.place(x=xPos + boxWidth * 0.3, y=yPos + boxHeight * 0.7,
                    anchor="sw")
        volUp.config(width=8)

        volDown = self.btn(panel, "Vol Down", hlbg,
                           functools.partial(audInst.volume,
                                             audioList, trackID, "down"))
        volDown.place(x=xPos + boxWidth * 0.3, y=yPos + boxHeight * 0.98,
                      anchor="sw")
        volDown.config(width=8)

        playTrack = self.btn(panel, "Play", hlbg,
                             functools.partial(audInst.play,
                                               audioList, trackID))
        playTrack.place(x=xPos + boxWidth * 0.98, y=yPos + boxHeight * 0.7,
                        anchor="se")
        playTrack.config(width=8)

        stopTrack = self.btn(panel, "Stop", hlbg,
                             functools.partial(audInst.stop,
                                               audioList, trackID))
        stopTrack.place(x=xPos + boxWidth * 0.98, y=yPos + boxHeight * 0.98,
                        anchor="se")
        stopTrack.config(width=8)

        panelElements.update({"Outline": outline, "Track Name": trackName,
                              "Select": selectTrack, "Remove": removeTrack,
                              "Vol Up": volUp, "Vol Down": volDown,
                              "Play": playTrack, "Stop": stopTrack,
                              "vlcObj": vlcObj, "panel": panel})

        self.controlBox.append(panelElements)

    def isPlaying(self):
        def object(panel, i, col):
            self.c[panel].itemconfig(self.controlBox[i]["Outline"], fill=col)
            self.controlBox[i]["Select"].config(highlightbackground=col)
            self.controlBox[i]["Remove"].config(highlightbackground=col)
            self.controlBox[i]["Vol Up"].config(highlightbackground=col)
            self.controlBox[i]["Vol Down"].config(highlightbackground=col)
            self.controlBox[i]["Play"].config(highlightbackground=col)
            self.controlBox[i]["Stop"].config(highlightbackground=col)

        for i in range(0, len(self.controlBox)):
            panel = self.controlBox[i]["panel"]
            if self.controlBox[i]["vlcObj"].get_state() == vlc.State.Playing:
                object(panel, i, "green")
            else:
                object(panel, i, "red")

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


def multiMenuButtons(source, output):
    for i in range(0, len(source.f.keys())):
        frameKey = [key for key in source.f.keys()][i]
        output.panelButton(8 + 90 * i, 24,
                           frameKey, "red",
                           functools.partial(source.raiseFrame,
                                             source.f, frameKey))

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
        trackID = audioList[i]["trackID"]
        vlcObj = audioList[i]["vlcObj"]

        output.trackCtrlBox(xPosition, yPosition, "red",
                            track, trackID, vlcObj,
                            audInst, audioList, currentPanel)

        rowNumber += 1



top = Display()
top.newFrCan(0, 0, sW, space * 5, "grey")

top.text(50, 25, "Title?", "yellow")

top.rect(0, space, sW, space * 2, "pink")
top.text(50, 75, "Presets", "yellow")

top.rect(0, space * 2, sW, space * 2, "orange")
top.text(50, 150, "Lights", "blue")

top.rect(0, space * 4, sW, space, "pink")
top.text(50, space * 4 + space / 2, "Events", "blue")


musicBar = Display()
musicBar.newFrCan(0, space * 5, sW * 0.2, space, "coral")

musicPanel = Display()
multiPanel(media.music, musicPanel,
           0, space * 6,
           sW * 0.2, sH - space * 6,
           "orange")

multiMenuButtons(musicPanel, musicBar)
multiTextLabels(media.music, musicPanel, 50, 8, "black")
multiControlBoxes(musicPanel, audio, audio.music)

soundBar = Display()
soundBar.newFrCan(sW * 0.2, space * 5, sW * 0.6, space, "orange")

soundPanel = Display()
multiPanel(media.sounds, soundPanel,
           sW * 0.2, space * 6,
           sW * 0.6, sH - space * 6,
           "pink")

multiMenuButtons(soundPanel, soundBar)
multiTextLabels(media.sounds, soundPanel, 50, 8, "black")
multiControlBoxes(soundPanel, audio, audio.sounds)

effectsBar = Display()
effectsBar.newFrCan(sW * 0.8, space * 5, sW * 0.2, space, "light coral")

effects = Display()
effects.newFrCan(sW * 0.8, space * 6,
                 sW * 0.2, sH - space * 6, "orange")

effects.text(50, 8, "Effects", "black")
multiControlBoxes(effects, audio, audio.effects)




def checkStatus():
    audio.statusCheck()
    musicPanel.isPlaying()
    soundPanel.isPlaying()
    effects.isPlaying()
    root.after(200, checkStatus)


root.after(200, checkStatus)
root.protocol("WM_DELETE_WINDOW", Display.windowClosed)
root.mainloop()
