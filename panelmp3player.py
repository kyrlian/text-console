import os
import glob
from panel import Panel
from pygame import mixer


class Panelmp3player(Panel):

    def initcontent(self, content):#use content as source directory
        self.playcontrols = "▣ > || << >>"
        self.content = self.playcontrols
        self.contentheigth = 1
        self.paused = True
        self.currentsongnumber = None
        self.musicdir = content
        self.listfiles(self.musicdir)

    def preferedsizes(self):
        self.sizes = [3, 10, self.contentheigth+2]

    def listfiles(self, dir):
        self.songlist = glob.glob( dir+"/*.mp3")
        if len(self.songlist)>0:
            self.currentsongnumber = 0

    def listfilenames(self):
        l = []
        for i in range(len(self.songlist)):
            n = os.path.basename(self.songlist[i])
            if i == self.currentsongnumber:
                n = "> "+n
            l.append(n)
        return l

    def updatecontent(self):
        playing = ""
        if self.currentsongnumber != None:
            os.path.basename(self.songlist[self.currentsongnumber])
        self.content = [self.playcontrols, playing]+self.listfilenames()

    def handlesongclick(self, charx, chary):
        linecliked = chary - self.zone.y - 2 # skip controls and title
        if linecliked>=0 and linecliked < len(self.songlist):
            self.currentsongnumber = linecliked
            self.play()

    def stop(self):
        mixer.music.stop()

    def play(self):
        mixer.init()
        mixer.music.load(self.songlist[self.currentsongnumber])
        mixer.music.play()
        pass

    def pause(self):
        if self.paused:
            mixer.music.unpause()
        if not self.paused:
            mixer.music.pause()
        self.paused = not self.paused

    def backward(self):
        self.currentsongnumber -= 1
        if self.currentsongnumber < 0:
            self.currentsongnumber = 0

    def forward(self):
        self.currentsongnumber += 1
        if self.currentsongnumber >= len(self.songlist):
            self.currentsongnumber = len(self.songlist)-1

    def handleplayerclick(self, charx, chary):
        controlsstop = [1]  # "▣ > || << >>"
        controlssplay = [3]
        controlsspause = [5, 6]
        controlscbwd = [8, 9]
        controlscfwd = [11, 12]
        if chary == self.zone.y+1:
            if charx - self.zone.x in controlsstop:
                print("clicked stop")
                self.stop()
            elif charx - self.zone.x in controlssplay:
                print("clicked play")
                self.play()
            elif charx - self.zone.x in controlsspause:
                print("clicked pause")
                self.pause()
            elif charx - self.zone.x in controlscbwd:
                print("clicked bwd")
                self.backward()
            elif charx - self.zone.x in controlscfwd:
                print("clicked fwd")
                self.forward()

    def handlepanelclick(self, charx, chary):
        self.handleplayerclick(charx, chary)
        self.handlesongclick(charx, chary)
        self.handlecontrolclick(charx, chary)
