#kyrlian, 2023

from panel import Panel
from panelmp3player import PanelMp3Player
from panelclock import PanelClock
from paneltextinput import PanelTextInput

class PanelMenu(Panel):

    choices=[]
    choices.append(("Clock",PanelClock,""))
    choices.append(("MP3 Player",PanelMp3Player,r"D:\music\#Divers"))
    choices.append(("Text Editor",PanelTextInput,["Lorem","ipsum"]))
    
    def initcontent(self, initargs=None):
        self.content = []
        for txt,panelclass,initargs in PanelMenu.choices:
            self.content.append(txt)

    def replaceme(self,panelclass,title,arg):
        self.zone.attachpanel(panelclass(title,arg))
        self.zone = None

    def handlechoiceclick(self, event,charx, chary):
        for i in range(len(PanelMenu.choices)):
            title,panelclass,arg = PanelMenu.choices[i]
            if chary == self.zone.y + 1+ i:
                print(f"clicked {title}")
                self.replaceme(panelclass,title,arg)
                return

    def handlepanelclick(self, event, charx, chary):
        self.handlechoiceclick(event,charx, chary)
        self.handlecontrolclick(event, charx, chary)