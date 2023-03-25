""" base panel class"""
#kyrlian, 2023

import pygame

class Panel:
    """ base panel class"""

    def __init__(self, title="", initargs=None, status="normal"):
        self.windowcontrols=self.initwindowcontrols()
        self.windowcontrolstring = self.drawcontrols(self.windowcontrols,"")
        self.title = title
        self.status = status
        self.zone = None
        self.sizes = [.1, .5, .9]
        self.content = []
        self.linkedpanel = None
        self.isfirstupdate = True
    
    def linkpanel(self,panel):
        """ link two panels (ex player and browser)"""
        self.linkedpanel = panel
        panel.linkedpanel = self

    def unlinkpanel(self):
        """ unlink two panels (ex player and browser)"""
        if self.linkedpanel is not None:
            self.linkedpanel.linkedpanel = None
        self.linkedpanel = None
        
    def attachtozone(self, zone):
        """ Attach panel to parent zone """
        self.zone = zone

    def preferedsizes(self):
        """ compute prefered sizes """
        # stub, to be customized for each panel type

    def updatecontent(self):
        """ update panel content """
        # stub, to be customized for each panel type

    def firstupdate(self):
        """  panel first update """
        # stub, to be customized for each panel type

    def update(self):
        """ update panel """
        if self.isfirstupdate is True:
            self.firstupdate()
            self.isfirstupdate = False
        self.updatecontent()
        self.preferedsizes()  # is after init content, so it can use len(self.content)

    def toggleminimised(self):
        """ toggle minimized status """
        if self.zone is not None:
            if self.status == "minimized":
                self.status = "normal"
                self.zone.resizeme(self.sizes[1])
            elif self.status == "normal":
                self.status = "maximized"
                self.zone.resizeme(self.sizes[2])
            else:
                self.status = "minimized"
                self.zone.resizeme(self.sizes[0])

    def getcolor(self, context, iline):
        """ get color for line """
        if context.focusedpanel == self:
            return (200, 200, 200)
        return (100, 100, 100)

    def isclicked(self, charx, chary):
        """ return true if panel is clicked """
        if self.zone is not None:
            return charx >= self.zone.x and charx < self.zone.x + self.zone.w and chary >= self.zone.y and chary < self.zone.y + self.zone.h
        return False
    
    def splith(self):
        if self.zone is not None:
            self.zone.split("h", .5)

    def splitv(self):
        if self.zone is not None:
            self.zone.split("v", .5)

    def remove(self):
        self.unlinkpanel()
        if self.zone is not None:
            self.zone.remove()

    def switch(self):
        if self.zone is not None:
            self.zone.switch()
        
    def initwindowcontrols(self):
        # "□_|⇅x"
        controls=[]#name,key,symbol,pos,command
        controls.append(("MaxMin",pygame.K_m,"M",[1],self.toggleminimised))
        controls.append(("SplitH",pygame.K_h,"H",[2],self.splith))
        controls.append(("SplitV",pygame.K_v,"V",[3],self.splitv))
        controls.append(("Switch",pygame.K_s,"S",[4],self.switch))
        controls.append(("Close",pygame.K_x,"X",[5],self.remove))
        return controls

    def drawcontrols(self, controls, spacing):
        return spacing.join(list(map(lambda tuple: tuple[2],controls)))
    
    def handlecontrolclick(self, event, charx, chary):
        """ handle click of control panel """
        if self.zone is not None and chary == self.zone.y:
            controlswidth = len(self.windowcontrolstring )
            for name,key,symbol,pos,command in self.windowcontrols:
                if charx - (self.zone.x + self.zone.w - controlswidth - 2) in pos:
                    print(f"clicked {name}")
                    command()
                    return

    def handlepanelclick(self, event, charx, chary):
        """ handle click of panel """
        self.handlecontrolclick(event, charx, chary)
        #to be customized for each panel type

    def handlecontrolkeydown(self, event, keymods):
        """  handle control keys """
        if keymods & pygame.KMOD_CTRL:#CTRL keys
            for name,key,symbol,pos,command in self.windowcontrols:
                if event.key == key:
                    print(f"Pressed {name}")
                    command()
                    return
        
    def handlepanelkeydown(self, event, keymods):#triggered only on focused panel
        """  handle panel keydown """
        self.handlecontrolkeydown(event, keymods)
        #to be customized for each panel type

    def draw(self):
        """  draw panel content to text array """
        if self.zone is not None:
            txtarray = []
            # top border with windows controls
            for i in range(self.zone.y):
                txtarray.append("")
            txtarray.append(" "*self.zone.x+"╔"+self.title+"═"*(self.zone.w-2-len(self.title) -
                            len(self.windowcontrolstring))+self.windowcontrolstring+"╗")  # top border
            # side borders plus content
            for txtline in self.content:
                txtarray.append(" "*self.zone.x+"║"+txtline +
                                " "*(self.zone.w-2-len(txtline))+"║")
            # side borders after content
            for i in range(self.zone.h-2-len(self.content)):
                txtarray.append(" "*self.zone.x+"║"+" "*(self.zone.w-2)+"║")
            # bottom border
            txtarray.append(" "*self.zone.x+"╚"+"═" *
                            (self.zone.w-2)+"╝")  # bottom border
            cutarray = []  # generate copy array staying in the zone
            for y in range(self.zone.y + self.zone.h):
                cutarray.append(txtarray[y][0:self.zone.x+self.zone.w])
            return cutarray
        return []