""" MP3 panel """
#kyrlian, 2023

import os
from panel import Panel
from pygame import mixer
import pygame


class PanelMp3Player(Panel):
    """ MP3 panel """

    def __init__(self, title="MP3 Player", initargs=None, status="normal"):
        Panel.__init__(self, title, initargs, status)
        self.panelcontrols=self.initpanelcontrols()
        self.panelcontrolstring = self.drawpanelcontrols()# "▣ > || << >>"
        self.content = self.panelcontrolstring
        self.paused = True
        self.musicdir = ""
        self.listoffset = 0
        self.playingtitle = ""
        mixer.init()

    def attachfilebrowser(self,directorybrowserpanelinstance):
        self.browser = directorybrowserpanelinstance

    def preferedsizes(self):
        self.sizes = [3, 10, len(self.content)+2]

    def updatecontent(self):
        """ update panel content """
        # If not paused and song is finished, go to next
        if not self.paused and not mixer.music.get_busy():
            self.forward()
            self.play()
        #TODO move file list to secondary panel
        self.content = [self.panelcontrolstring, self.playingtitle]

    def stop(self):
        """ stop player """
        mixer.music.stop()

    def play(self):
        """ play song """
        if self.browser.currentfilenumber is not None:
            musicfile = self.browser.filelist[self.browser.currentfilenumber]
            musicfilepath = os.path.join(self.musicdir, musicfile)
            if os.path.isfile(musicfilepath):
                mixer.music.load( musicfilepath )
                mixer.music.play()
                self.playingtitle = musicfile.replace(".mp3","")

    def pause(self):
        """ pause song """
        if self.paused:
            mixer.music.unpause()
        if not self.paused:
            mixer.music.pause()
        self.paused = not self.paused

    def backward(self):
        """ go to previous song """
        if self.browser.currentfilenumber is not None:
            self.browser.currentfilenumber = max(self.browser.currentfilenumber-1 , 0)
            limit =  len(self.browser.filelist)
            while not self.browser.filelist[self.browser.currentfilenumber].endswith(".mp3") and limit > 0:#music file
                self.browser.currentfilenumber = max(self.browser.currentfilenumber-1 , 0)
                limit-=1

    def forward(self):
        """ go to next song """
        if self.browser.currentfilenumber is not None:
            self.browser.currentfilenumber = ( self.browser.currentfilenumber +1 ) %  len(self.browser.filelist) #loop
            limit = len(self.browser.filelist)
            while not self.browser.filelist[self.browser.currentfilenumber].endswith(".mp3") and limit > 0:#music file
                self.browser.currentfilenumber = ( self.browser.currentfilenumber +1 ) %  len(self.browser.filelist)
                limit-=1

    def initpanelcontrols(self):
        # "▣ > || << >>"
        playercontrols=[]#name,key,symbol,pos,command
        playercontrols.append(("Stop",None,"▣",[1],self.stop))
        playercontrols.append(("Play",None,">",[3],self.play))
        playercontrols.append(("Pause",pygame.K_SPACE,"||",[5,6],self.pause))
        playercontrols.append(("Bwd",pygame.K_RIGHT,"<<",[8,9],self.backward))
        playercontrols.append(("Fwd",pygame.K_LEFT,">>",[11,12],self.forward))
        return playercontrols
    
    def drawpanelcontrols(self):
        # concat control symbols
        return " ".join(list(map(lambda tuple: tuple[2],self.panelcontrols)))

    def handleplayerclick(self, event,charx, chary):
        """ handle click on player controls """
        if self.zone is not None and chary == self.zone.y+1:
            for name,key,symbol,pos,command in self.panelcontrols:
                if charx - self.zone.x in pos:
                    print(f"clicked {name}")
                    command()
                    return

    def handlepanelclick(self, event, charx, chary):
        """ handle click on panel """
        self.handleplayerclick(event,charx, chary)
        self.handlecontrolclick(event, charx, chary)

    def handleplayerkeydown(self, event, keymods):
        """ handle player keys """
        for name,key,symbol,pos,command in self.panelcontrols:
            if event.key == key:
                print(f"Pressed {name}")
                command()
                return

    def handlepanelkeydown(self, event, keymods):
        self.handleplayerkeydown(event, keymods)
        self.handlecontrolkeydown(event, keymods)
