import os
import tkinter as tk
import functools
# import vlc
# import yeelight


class Media():
    music = list()
    sounds = list()
    effects = list()

    @classmethod
    def getMedia(cls, inputDir, varList):
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

    @classmethod
    def printList(cls, var):
        for i in range(0, len(var)):
            print("\n" + str(var[i][0]["panel"]) + ":")
            for j in range(0, len(var[i])):
                for k, v in var[i][j].items():
                    print(str(k) + ": " + str(v))
                print("\n")


media = Media()
media.getMedia("CoreMusic", Media.music)
media.getMedia("CoreSounds", Media.sounds)
media.getMedia("CoreEffects", Media.effects)


class Audio():
    pass


class Lights():
    pass


class Presets():
    pass


class ActiveData():
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
multiPanel(Media.music, musicPanel,
                 0, space * 6,
                 sW * 0.2, sH - space * 6,
                 "orange")

multiMenuButtons(musicPanel, musicBar)
multiTextLabels(Media.music, musicPanel, 50, 50, "black")


soundBar = Display()
soundBar.newFrCan(sW * 0.2, space * 5, sW * 0.6, space, "orange")

soundPanel = Display()
multiPanel(Media.sounds, soundPanel,
                 sW * 0.2, space * 6,
                 sW * 0.6, sH - space * 6,
                 "pink")

multiMenuButtons(soundPanel, soundBar)
multiTextLabels(Media.sounds, soundPanel, 50, 50, "black")


effectsBar = Display()
effectsBar.newFrCan(sW * 0.8, space * 5, sW * 0.2, space, "light coral")

effects = Display()
effects.newFrCan(sW * 0.8, space * 6,
                 sW * 0.2, sH - space * 6, "orange")

effects.text(50, 50, "Effects", "black")












root.protocol("WM_DELETE_WINDOW", Display.windowClosed)
root.mainloop()
