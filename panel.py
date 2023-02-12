""" base panel class"""
#kyrlian, 2023

import pygame

class Panel:
    """ base panel class"""

    def __init__(self, title="", initargs=None, status="normal"):
        self.controls = "□_|⇅x"
        self.title = title
        self.status = status
        self.zone = None
        self.sizes = [.1, .5, .9]
        self.content = []

    def attachtozone(self, zone):
        """ Attach panel to parent zone """
        self.zone = zone

    def preferedsizes(self):
        """ compute prefered sizes """
        # stub, to be customized for each panel type

    def updatecontent(self):
        """ update panel content """
        # stub, to be customized for each panel type

    def update(self):
        """ update panel """
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
    
    def handlecontrolclick(self, event, charx, chary):
        """ handle click of control panel """
        if self.zone is not None and chary == self.zone.y:
            controlsminimize = -6  # "□_|⇅x"
            controlssplith = -5
            controlssplitv = -4
            controlsswitch = -3
            controlsclose = -2
            if charx == self.zone.x + self.zone.w + controlsminimize:
                print("clicked minimize")
                self.toggleminimised()
            elif charx == self.zone.x + self.zone.w + controlssplith:
                print("clicked split h")
                self.zone.split("h", .5)
            elif charx == self.zone.x + self.zone.w + controlssplitv:
                print("clicked split v")
                self.zone.split("v", .5)
            elif charx == self.zone.x + self.zone.w + controlsswitch:
                print("clicked switch")
                self.zone.switch()
            elif charx == self.zone.x + self.zone.w + controlsclose:
                print("clicked close")
                self.zone.remove()

    def handlepanelclick(self, event, charx, chary):
        """ handle click of panel """
        self.handlecontrolclick(event, charx, chary)

    def handlecontrolkeydown(self, event, keymods):
        """  handle control keys """
        if keymods & pygame.KMOD_CTRL:#CTRL keys
            #TODO merge control click/key config (see map in PanelMenu)
            #and handle M(inimize), H(hsplit),V(vsplit),W(switch)X(close)
            if event.key == pygame.K_m:#Minimize zone
                self.toggleminimised()

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
                            len(self.controls))+self.controls+"╗")  # top border
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