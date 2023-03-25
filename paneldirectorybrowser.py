""" MP3 panel """
# kyrlian, 2023

import os
from panel import Panel
from pygame import mixer
import pygame


class PanelDirectoryBrowser(Panel):
    """ Directory Browser panel """

    def __init__(self, title="Directory Browser", initargs=["", ".mp3"], status="normal"):
        Panel.__init__(self, title, initargs, status)
        self.panelcontrols = self.initpanelcontrols()
        self.content = ""
        self.currentfilenumber = None
        self.currentdir = ""
        self.filelist = []
        self.extensionfilter = None
        if initargs is not None:
            if initargs[0] is not None:
                self.currentdir = initargs[0]
            if initargs[1] is not None:
                self.extensionfilter = initargs[1]
        self.loaddirectory(self.currentdir)
        self.listoffset = 0
        mixer.init()

    def registerfileclickaction(self, action):
        self.actiononclick = action

    def handlefileclick(self):
        self.actiononclick()

    def preferedsizes(self):
        self.sizes = [3, 10, len(self.content)+2]

    def loaddirectorycontent(self, directory):
        """ load directory content """
        self.currentdir = directory
        self.filelist = [".."]
        self.listoffset = 0
        for filename in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, filename)) or \
            (os.path.isfile(os.path.join(directory, filename)) and (self.extensionfilter is None or filename.endswith(self.extensionfilter))):
                self.filelist.append(filename)
        if len(self.filelist) > 0:
            self.currentfilenumber = 0

    def loaddirectory(self, directory):
        """ load directory """
        if directory is not None and isinstance(directory, str) and os.path.isdir(directory):
            self.loaddirectorycontent(directory)
        elif os.path.isdir("."):
            self.loaddirectorycontent(".")
        elif os.path.isdir("C:/"):
            self.loaddirectorycontent("C:/")
        else:
            print("No valid directory found")

    def listfilenames(self):
        """ list file names from filelist """
        displaylist = []
        for i in range(self.listoffset, len(self.filelist)):
            filename = self.filelist[i]
            if i == self.currentfilenumber:
                filename = "> "+filename
            displaylist.append(filename)
        return displaylist

    def updatecontent(self):
        """ update panel content """
        self.content = self.listfilenames()

    def scrollup(self):
        self.listoffset = max(0, self.listoffset-1)

    def scrolldown(self):
        self.listoffset = min(len(self.filelist), self.listoffset+1)

    def initpanelcontrols(self):
        browsercontrols = []  # name,key,symbol,pos,command
        browsercontrols.append(("Up", pygame.K_UP, "^", [14], self.scrollup))
        browsercontrols.append(("Down", pygame.K_DOWN, "v", [16], self.scrolldown))
        return browsercontrols

    def handlebrowserclick(self, event, charx, chary):
        """ handle click on song list """
        linecliked = chary - self.zone.y - 1 + self.listoffset  # manage list offset
        if linecliked >= 0 and linecliked < len(self.filelist):
            if self.filelist[linecliked].endswith(self.extensionfilter):  # eligible file
                self.currentfilenumber = linecliked
                self.handlefileclick()
            else:  # directory
                newdir = os.path.join(self.currentdir, self.filelist[linecliked])
                self.loaddirectory(newdir)

    def handlepanelclick(self, event, charx, chary):
        """ handle click on panel """
        self.handlebrowserclick(event, charx, chary)
        self.handlecontrolclick(event, charx, chary)

    def handlebrowserkeydown(self, event, keymods):
        """ handle player keys """
        for name, key, symbol, pos, command in self.panelcontrols:
            if event.key == key:
                print(f"Pressed {name}")
                command()
                return

    def handlepanelkeydown(self, event, keymods):
        self.handlebrowserkeydown(event, keymods)
        self.handlecontrolkeydown(event, keymods)
