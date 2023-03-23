""" menu panel """
#kyrlian, 2023

import pygame
from panel import Panel
from panelmp3player import PanelMp3Player
from panelclock import PanelClock
from paneltextinput import PanelTextInput

class PanelMenu(Panel):
    """ menu panel """

    def __init__(self, title="Menu", initargs=None, status="normal"):
        Panel.__init__(self, title, initargs, status)
        self.menucontrols = self.initmenucontrols()
        for name,key,symbol,pos,command in self.menucontrols:
            self.content.append(name)

    def replacewith(self,newpanel):
        if self.zone is not None:
            self.zone.attachpanel(newpanel)
            self.zone = None

    def replacewithClock(self):
        self.replacewith(PanelClock("Clock"))

    def replacewithMP3Player(self):
        self.replacewith(PanelMp3Player("MP3 Player",r"D:\music"))
    
    def replacewithTextEditor(self):
        self.replacewith(PanelTextInput("Text editor",["Lorem","ipsum"]))

    def initmenucontrols(self):
        controls=[]#name,key,symbol,pos,command
        controls.append(("[C]lock",pygame.K_c,"C",[1],self.replacewithClock))
        controls.append(("[M]P3 Player",pygame.K_m,"M",[2],self.replacewithMP3Player))
        controls.append(("[T]ext Editor",pygame.K_t,"T",[3],self.replacewithTextEditor))
        return controls
    
    def handlechoiceclick(self, event,charx, chary):
        """ handle click on choice """
        if self.zone is not None:
            for name,key,symbol,pos,command in self.menucontrols:
                if chary - self.zone.y in pos:
                    print(f"clicked {name}")
                    command()
                    return

    def handlepanelclick(self, event, charx, chary):
        self.handlechoiceclick(event,charx, chary)
        self.handlecontrolclick(event, charx, chary)

    def handlemenukeydown(self, event, keymods):
        """ handle menu shortcuts """
        if self.zone is not None:
            for name,key,symbol,pos,command in self.menucontrols:
                if event.key == key:
                    print(f"keyed {name}")
                    command()
                    return

    def handlepanelkeydown(self, event, keymods):
        self.handlecontrolkeydown(event, keymods)
        self.handlemenukeydown(event, keymods)