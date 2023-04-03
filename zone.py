""" zone class """
#kyrlian, 2023

import sys
from functools import reduce
from operator import iconcat
import pygame
from panelmenu import PanelMenu
import eventconverter

class Zone:
    """ zone class """
    def __init__(self, x=0, y=0, w=0, h=0, parent=None, panel=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.parent = parent
        self.panel = panel
        self.childs = []
        self.splitdir = None
        self.splitpct = .5
        self.attachpanel(panel)
        self.panelist = []

    def attachpanel(self, panel):
        """ attach panel to zone """
        if panel is not None:
            self.panel = panel
            self.childs = []
            panel.attachtozone(self)
            return True
        return False

    def attachzone(self, zone):
        """  attach child zone """
        self.childs.append(zone)
        zone.parent = self
        self.panel = None

    def split(self, direction, pct, newpanel=None):
        """  split zone in two subzone, can set a panel for second zone """
        self.splitdir = direction
        self.splitpct = pct
        if  newpanel is None:
            newpanel = PanelMenu("Menu")
        if direction == "h":  # horizontal split
            self.attachzone(Zone(self.x, self.y, self.w,
                            int(self.h * pct), self, self.panel))
            self.attachzone(Zone(self.x, int(self.y + self.h * pct),
                            self.w, int(self.h * (1-pct)), self,newpanel))
        else:  # vertical split
            self.attachzone(Zone(self.x, self.y, int(
                self.w * pct), self.h, self, self.panel))
            self.attachzone(Zone(int(self.x + self.w * pct), self.y,
                            int(self.w * (1-pct)), self.h, self,newpanel))
        return self.childs[0], self.childs[1]

    def resizeme(self, pctorabs=None): # change the split of my parent
        """  resize this zone """
        if self.parent is not None:
            if self.parent.childs[0] == self or pctorabs is None: #I am first sub zone
                zone0size = pctorabs
            else: #resize info is for first sub zone, but I'm second, convert
                if pctorabs < 1:#pct
                    zone0size = 1 - pctorabs
                else: #abs
                    if self.parent.splitdir == "h":
                        zone0size = self.parent.h - pctorabs 
                    else:
                        zone0size =  self.parent.w - pctorabs
            self.parent.resizesplit(zone0size)
        else:#rootzone - should never apply
            print("I am root")

    #TODO handle zone resize with mouse drag

    def resizesplit(self, pctorabs=None):  # change split pct, or just recalc sizes (if Pct==None)
        """  resize the splits of this zone """
        if len(self.childs) > 0:#resize splits
            pct = self.splitpct
            if pctorabs is not None:
                if pctorabs < 1:
                    pct = pctorabs
                else: #abs
                    if self.splitdir == "h":
                        pct = pctorabs / self.h
                    else:
                        pct = pctorabs / self.w
                self.splitpct = pct
            if self.splitdir == "h":
                newsplith = int(self.h * pct)
                if newsplith < 1:# ensure we have at least h=1 for both zones to keep titlebar
                    newsplith = 1 #keep title bar of 1st zone
                elif self.h - newsplith < 1:
                    newsplith = self.h - 1#keep title bar of 2nd zone
                self.childs[0].x = self.x
                self.childs[0].y = self.y
                self.childs[0].w = self.w
                self.childs[0].h = newsplith
                self.childs[1].x = self.x
                self.childs[1].y = self.y + newsplith
                self.childs[1].w = self.w
                self.childs[1].h = self.h - newsplith
            else:
                newsplitw = int(self.w * pct)
                self.childs[0].x = self.x
                self.childs[0].y = self.y
                self.childs[0].w = newsplitw
                self.childs[0].h = self.h
                self.childs[1].x = self.x + newsplitw
                self.childs[1].y = self.y
                self.childs[1].w = self.w - newsplitw
                self.childs[1].h = self.h
            self.childs[0].resizesplit()
            self.childs[1].resizesplit()

    def switch(self):#switch me with my sibling zone
        """  switch the subzones """
        if self.parent is not None:
            tmp = self.parent.childs[0]
            self.parent.childs[0] = self.parent.childs[1]
            self.parent.childs[1] = tmp
            self.parent.resizesplit()

    def remove(self):
        """  remove me from my parent """
        if self.parent is None:  # if I am root, quit
            print("I am root")
            pygame.quit()
            sys.exit()
        else:
            self.parent.childs.remove(self)  # remove me from my parent
            # copy sibling content to parent
            sibling = self.parent.childs[0]
            if not self.parent.attachpanel(sibling.panel):
                self.parent.childs = []
                for nephew in sibling.childs:
                    self.parent.attachzone(nephew)
                # resize parent subzones
                self.parent.resizesplit(self.parent.splitpct)
            self.parent = None  # remove my parent from me to free the object


    def handlezoneclick(self, context, event, charx, chary):
        """ detect panel clicked, and manage click """
        if self.panel is not None and self.panel.isclicked(charx, chary):
            if context.focusedpanel is self.panel:
                #send click only if already has focus
                self.panel.handlepanelclick(event, charx, chary)
            else:
                context.focusedpanel = self.panel
        else:
            for child in self.childs:
                child.handlezoneclick(context, event, charx, chary)

    def listpanels(self):
        """  list sub panels """
        if self.panel is not None:
            return [self.panel]
        return list(reduce(iconcat,map(lambda c: c.listpanels(),self.childs)))
        
    def getnextpanel(self,panel=None):
        """ get next panel  """
        self.panelist=self.listpanels()
        if panel is not None:
            idx = self.panelist.index(panel)
            if idx is not None:
                return self.panelist [(idx+1)%len(self.panelist)]
        return self.panelist[0]
        
    def handlezonekeydown(self, context, event):
        """  handle key down in zone, and pass to focused panel """
        if event.key == eventconverter.KEY_TAB and event.keymods == eventconverter.KMOD_CTRL:#Pass focus to next panel in zone
            nextpanel = self.getnextpanel(context.focusedpanel)
            if nextpanel is not None:
                context.focusedpanel = nextpanel
        else:
            context.focusedpanel.handlepanelkeydown(event)

    def update(self):
        """  update panel or child zones """
        for child in self.childs:
            child.update()
        if self.panel is not None:
            self.panel.update()

    # TODO migrate to python curses ? https://docs.python.org/3/howto/curses.html

    def draw(self, context, renderer):
        """  draw zone """
        for child in self.childs:
            child.draw(context, renderer)
        if self.panel is not None:
            panellines = self.panel.draw()
            for idx, line in enumerate(panellines):
                linecolor = self.panel.getcolor(context,idx)
                renderer.renderline(line,linecolor,0,idx)
