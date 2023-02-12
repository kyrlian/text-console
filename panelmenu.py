""" menu panel """
#kyrlian, 2023

import pygame
from panel import Panel
from panelmp3player import PanelMp3Player
from panelclock import PanelClock
from paneltextinput import PanelTextInput

class PanelMenu(Panel):
    """ menu panel """
    choices=[]#key,title,class,args
    choices.append((pygame.K_c,"Clock",PanelClock,""))
    choices.append((pygame.K_m,"MP3 Player",PanelMp3Player,r"D:\music\#Divers"))
    choices.append((pygame.K_t,"Text Editor",PanelTextInput,["Lorem","ipsum"]))

    def __init__(self, title="Menu", initargs=None, status="normal"):
        Panel.__init__(self, title, initargs, status)
        for key,txt,panelclass,initargs in PanelMenu.choices:
            self.content.append(txt)

    def replaceme(self,panelclass,title,arg):
        """ replace this panel with chosen one """
        if self.zone is not None:
            self.zone.attachpanel(panelclass(title,arg))
            self.zone = None

    def handlechoiceclick(self, event,charx, chary):
        """ handle click on choice """
        if self.zone is not None:
            for idx, (key,title,panelclass,arg) in enumerate(PanelMenu.choices):
                if chary == self.zone.y + 1 + idx:
                    print(f"clicked {title}")
                    self.replaceme(panelclass,title,arg)
                    return

    def handlepanelclick(self, event, charx, chary):
        self.handlechoiceclick(event,charx, chary)
        self.handlecontrolclick(event, charx, chary)

    def handlemenukeydown(self, event, keymods):
        """ handle menu shortcuts """
        if self.zone is not None:
            for key,title,panelclass,arg in PanelMenu.choices:
                if event.key == key:
                    print(f"keyed {title}")
                    self.replaceme(panelclass,title,arg)
                    return

    def handlepanelkeydown(self, event, keymods):
        self.handlecontrolkeydown(event, keymods)
        self.handlemenukeydown(event, keymods)