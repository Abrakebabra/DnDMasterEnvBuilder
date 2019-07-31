import os
import tkinter as tk
import functools
import vlc
import time  # code runs faster than vlc
# import yeelight


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
    # later:  Convert tracks to trackID so same names across panels can be used

    def __init__(self):
        self.active = list()  # Holds list of active tracks

        self.music = list()  # Holds "path": vlc.MediaPlayer(path)
        self.sounds = list()  # Holds "path": vlc.MediaPlayer(path)
        self.effects = list()  # Holds "path": vlc.MediaPlayer(path)

    def audioLoader(self, MediaAudio, varList):
        for i in range(0, len(MediaAudio)):
            for j in range(0, len(MediaAudio[i])):
                ma = MediaAudio[i][j]
                track = dict()

                track.update({"panel": ma["panel"],
                              "track": ma["track"],
                              "trackID": ma["trackID"],
                              ma["track"]: vlc.MediaPlayer(ma["path"])})

                varList.append(track)

    def play(self, audioList, track, vol=100):

        def handleTrack():
            for i in range(0, len(audioList)):
                if audioList[i]["track"] == track:
                    self.active.append({"panel": audioList[i]["panel"],
                                        "audioList": str(audioList),
                                        "track": audioList[i]["track"],
                                        "trackID": audioList[i]["trackID"]})

                    audioList[i][track].play()
                    time.sleep(0.01)  # code runs faster than vlc
                    audioList[i][track].audio_set_volume(vol)

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

    def stop(self, audioList, track, panel=None):
        for i in range(0, len(audioList)):
            if audioList[i]["track"] == track:
                audioList[i][track].stop()

            for i in range(0, len(self.active)):
                if self.active[i]["track"] == track:
                    self.active.pop(i)
                    break

    def volume(self, audioList, track, volUpDown):

        def volUp(trackObj):
            currentVol = trackObj.audio_get_volume()
            newVol = currentVol + 10
            if newVol <= 100:
                trackObj.audio_set_volume(newVol)
            else:
                trackObj.audio_set_volume(100)

        def volDown(trackObj):
            currentVol = trackObj.audio_get_volume()
            newVol = currentVol - 10
            if newVol >= 0:
                trackObj.audio_set_volume(newVol)
            else:
                trackObj.audio_set_volume(0)

        for i in range(0, len(audioList)):
            if audioList[i]["track"] == track:
                if volUpDown == "up":
                    volUp(audioList[i][track])
                elif volUpDown == "down":
                    volDown(audioList[i][track])

    def stopAll(self):
        
        stopList = list()
        
        for i in range(0, len(self.active)):
            stopList.append(self.active[i])
            
        for i in range(0, len(stopList)):
            track = stopList[i]["track"]
            audioList = stopList[i]["audioList"]

            if str(self.music) == audioList:
                self.stop(self.music, track)
            elif str(self.sounds) == audioList:
                self.stop(self.sounds, track)
            elif str(self.effects) == audioList:
                self.stop(self.effects, track)


audio = Audio()
audio.audioLoader(media.music, audio.music)
audio.audioLoader(media.sounds, audio.sounds)
audio.audioLoader(media.effects, audio.effects)


class TestAudio():

    def __init__(self, track="Build 1"):
        self.track = track

    def play(self):
        audio.play(audio.music, self.track)

    def stop(self):
        audio.stop(audio.music, self.track)

    def volup(self):
        audio.volume(audio.music, self.track, "up")

    def voldown(self):
        audio.volume(audio.music, self.track, "down")

    def getvol(self):
        for i in range(0, len(audio.music)):
            if audio.music[i]["track"] == self.track:
                print(str(audio.music[i][self.track].audio_get_volume()))

    def multistart(self):
        audio.play(audio.music, "02 Jojo")
        audio.play(audio.music, "Build 1")
        audio.play(audio.sounds, "Latin 2")

    def stopall(self):
        audio.stopAll()


class Lights():

    def __init__(self):
        pass


class Presets():
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
        self.f = dict()
        self.c = dict()
        self.b = dict()

    def newFrCan(self, xPos, yPos, w, h, col, pane="default"):
        global root

        self.f.update({pane: tk.Frame(root, width=w, height=h, bg=col)})
        self.f[pane].place(x=xPos, y=yPos)

        self.c.update({pane: tk.Canvas(self.f[pane], width=w, height=h,
                      bg=col, highlightthickness=0)})
        self.c[pane].place(x=0, y=0)

    def raiseFrame(self, frame, pane="default"):
        frame[pane].tkraise()

    def rect(self, x, y, w, h, col, pane="default"):
        self.c[pane].create_rectangle(x, y, x + w, y + h, fill=col, width=0)

    def text(self, x, y, words, col, pane="default"):
        self.c[pane].create_text(x, y, text=words, fill=col)

    def panelButton(self, xPos, yPos, words, hlbg, action, pane="default"):
        self.b.update({words: tk.Button(self.c[pane], text=words,
                       highlightbackground=hlbg, command=action)})
        self.b[words].place(x=xPos, y=yPos)
        self.b[words].config(width=8)

    #def trackCtrl(self, xPos, yPos, track, audioObj,)

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
multiTextLabels(media.music, musicPanel, 50, 50, "black")


soundBar = Display()
soundBar.newFrCan(sW * 0.2, space * 5, sW * 0.6, space, "orange")

soundPanel = Display()
multiPanel(media.sounds, soundPanel,
                 sW * 0.2, space * 6,
                 sW * 0.6, sH - space * 6,
                 "pink")

multiMenuButtons(soundPanel, soundBar)
multiTextLabels(media.sounds, soundPanel, 50, 50, "black")


effectsBar = Display()
effectsBar.newFrCan(sW * 0.8, space * 5, sW * 0.2, space, "light coral")

effects = Display()
effects.newFrCan(sW * 0.8, space * 6,
                 sW * 0.2, sH - space * 6, "orange")

effects.text(50, 50, "Effects", "black")












root.protocol("WM_DELETE_WINDOW", Display.windowClosed)
root.mainloop()
