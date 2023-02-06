import os
import glob
from panel import Panel
from pygame import mixer
import pygame


class Panelmp3player(Panel):

    def initcontent(self, content):  # use content as source directory
        self.playcontrols = "▣ > || << >>"
        self.content = self.playcontrols
        self.contentheigth = 1
        self.paused = True
        self.currentsongnumber = None
        self.musicdir = content
        self.listfiles(self.musicdir)
        self.listoffset = 0
        mixer.init()

    def preferedsizes(self):
        self.sizes = [3, 10, self.contentheigth+2]

    def listfiles(self, dir):
        self.songlist = [".."]
        for f in os.listdir(dir):
            if os.path.isdir(os.path.join(dir, f)) or (os.path.isfile(os.path.join(dir, f)) and f.endswith(".mp3")):
                self.songlist.append(f)
        if len(self.songlist) > 0:
            self.currentsongnumber = 0

    def listfilenames(self):
        displaylist = []
        for i in range(self.listoffset,len(self.songlist)):
            f = self.songlist[i]
            if i == self.currentsongnumber:
                f = "> "+f
            displaylist.append(f)
        return displaylist

    def updatecontent(self):
        # If not paused and song is finished, go to next
        if not self.paused and not mixer.music.get_busy():
            self.forward()
            self.play()
        playing = ""
        if self.currentsongnumber != None:
            playing = self.songlist[self.currentsongnumber]
        self.content = [self.playcontrols, playing]+self.listfilenames()

    def stop(self):
        mixer.music.stop()

    def play(self):
        if self.currentsongnumber != None:
            mixer.music.load( os.path.join(self.musicdir, self.songlist[self.currentsongnumber]))
            mixer.music.play()

    def pause(self):
        if self.paused:
            mixer.music.unpause()
        if not self.paused:
            mixer.music.pause()
        self.paused = not self.paused

    def backward(self):
        if self.currentsongnumber != None:
            self.currentsongnumber = max(self.currentsongnumber-1 , 0)

    def forward(self):
        if self.currentsongnumber != None:
            self.currentsongnumber += 1
            if self.currentsongnumber >= len(self.songlist):
                self.currentsongnumber = 0  # Loop

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

    def handlesongclick(self, charx, chary):
        linecliked = chary - self.zone.y - 2 - self.listoffset  # skip controls and title, manage list offset
        if linecliked >= 0 and linecliked < len(self.songlist):
            if self.songlist[linecliked].endswith(".mp3"):
                self.currentsongnumber = linecliked
                self.play()
            else:
                self.musicdir = os.path.join(self.musicdir, self.songlist[self.linecliked])
                self.listfiles(self.musicdir)

    def handlepanelclick(self, charx, chary):
        self.handleplayerclick(charx, chary)
        self.handlesongclick(charx, chary)
        self.handlecontrolclick(charx, chary)

    def handlepanelkeydown(self, key):
        if key == pygame.K_UP:
            self.listoffset = max(0, self.listoffset-1)
        elif key == pygame.K_DOWN:
            self.listoffset = min(len(self.songlist), self.listoffset+1)
        elif key == pygame.K_SPACE:
            self.pause()
        elif key == pygame.K_RIGHT:
            self.forward()
        elif key == pygame.K_LEFT:
            self.backward()