import os
import glob
from panel import Panel
from pygame import mixer
import pygame


class PanelMp3Player(Panel):

    def initcontent(self, content):  # use content as source directory
        self.playcontrols = "▣ > || << >>"
        self.content = self.playcontrols
        self.contentheigth = 1
        self.paused = True
        self.currentsongnumber = None
        self.loaddirectory(content)
        self.listoffset = 0
        self.playingtitle = ""
        mixer.init()

    def preferedsizes(self):
        self.sizes = [3, 10, self.contentheigth+2]

    def loaddirectorycontent(self, dir):
        self.musicdir = dir
        self.songlist = [".."]
        for f in os.listdir(dir):
            if os.path.isdir(os.path.join(dir, f)) or (os.path.isfile(os.path.join(dir, f)) and f.endswith(".mp3")):
                self.songlist.append(f)
        if len(self.songlist) > 0:
            self.currentsongnumber = 0

    def loaddirectory(self, dir):
        if os.path.isdir(dir):
            self.loaddirectorycontent(dir)
        elif os.path.isdir("."):
            self.loaddirectorycontent(".")
        elif os.path.isdir("C:/"):
            self.loaddirectorycontent("C:/")
        else:
            print("No mp3 directory found")

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
        self.content = [self.playcontrols, self.playingtitle]+self.listfilenames()

    def stop(self):
        mixer.music.stop()

    def play(self):
        if self.currentsongnumber != None:
            musicfile = self.songlist[self.currentsongnumber]
            musicfilepath = os.path.join(self.musicdir, musicfile)
            if os.path.isfile(musicfilepath):
                mixer.music.load( musicfilepath )
                mixer.music.play()
                self.playingtitle = musicfile.replace(".mp3","")

    def pause(self):
        if self.paused:
            mixer.music.unpause()
        if not self.paused:
            mixer.music.pause()
        self.paused = not self.paused

    def backward(self):
        if self.currentsongnumber != None:
            self.currentsongnumber = max(self.currentsongnumber-1 , 0)
            limit =  len(self.songlist)
            while not self.songlist[self.currentsongnumber].endswith(".mp3") and limit > 0:#music file
                self.currentsongnumber = max(self.currentsongnumber-1 , 0)
                limit-=1

    def forward(self):
        if self.currentsongnumber != None:
            self.currentsongnumber == ( self.currentsongnumber +1 ) %  len(self.songlist) #loop
            limit =  len(self.songlist)
            while not self.songlist[self.currentsongnumber].endswith(".mp3") and limit > 0:#music file
                self.currentsongnumber == ( self.currentsongnumber +1 ) %  len(self.songlist) 
                limit-=1

    def handleplayerclick(self, event,charx, chary):
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

    def handlesongclick(self,event, charx, chary):
        linecliked = chary - self.zone.y - 3 + self.listoffset  # skip controls and title, manage list offset
        if linecliked >= 0 and linecliked < len(self.songlist):
            if self.songlist[linecliked].endswith(".mp3"):#music file
                self.currentsongnumber = linecliked
                self.play()
            else:#directory
                newdir =  os.path.join(self.musicdir, self.songlist[linecliked])
                self.loaddirectory(newdir)

    def handlepanelclick(self, event, charx, chary):
        self.handleplayerclick(event,charx, chary)
        self.handlesongclick(event,charx, chary)
        self.handlecontrolclick(event, charx, chary)

    def handlepanelkeydown(self, event, keymods):
        if event.key == pygame.K_UP:
            self.listoffset = max(0, self.listoffset-1)
        elif event.key == pygame.K_DOWN:
            self.listoffset = min(len(self.songlist), self.listoffset+1)
        elif event.key == pygame.K_SPACE:
            self.pause()
        elif event.key == pygame.K_RIGHT:
            self.forward()
        elif event.key == pygame.K_LEFT:
            self.backward()