#kyrlian, 2023

import sys
import pygame

from panel import Panel

class Zone:
    def __init__(self, x=0, y=0, w=0, h=0, parent=None, panel=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.parent = parent
        self.panel = panel
        self.childs = []
        self.attachpanel(panel)
        self.panelist = []

    def attachpanel(self, panel):
        if panel != None:
            self.panel = panel
            self.childs = []
            panel.attachtozone(self)
            return True
        return False

    def removepanel(self):
        self.panel = None

    def attachzone(self, zone):
        self.childs.append(zone)
        zone.parent = self
        self.removepanel()

    def split(self, dir, pct, newpanel=None):
        self.splitdir = dir
        self.splitpct = pct
        if  newpanel == None:
            newpanel = Panel("temp")
        if dir == "h":  # horizontal split
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
        if self.parent != None:
            if self.parent.childs[0] == self or pctorabs == None: #I am first sub zone
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
            if pctorabs < 1:#pct
                self.w = int(self.w * pctorabs)
                self.h = int(self.h * pctorabs)
            else: #abs, not really adapted - because usually resize is on 1 axis (the split), for rootzone it doenst apply
                self.w = int(pctorabs)
                self.h = int(pctorabs)


    def resizesplit(self, pctorabs=None):  # change split pct, or just recalc sizes (if Pct==None)
        if len(self.childs) > 0:#resize splits
            if pctorabs != None:
                if pctorabs < 1:
                    pct = pctorabs
                else: #abs
                    if self.splitdir == "h":
                        pct = pctorabs / self.h
                    else:
                        pct = pctorabs / self.w
                self.splitpct = pct
            else:
                pct = self.splitpct
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

    def remove(self):
        if self.parent == None:  # if I am root, quit
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
        if self.panel != None and self.panel.isclicked(charx, chary):
            context.focusedpanel = self.panel
            self.panel.handlepanelclick(event, charx, chary)#TODO send even if didnt already have focus ?
        else:
            for child in self.childs:
                child.handlezoneclick(context, event, charx, chary)

    def listpanels(self):
        from functools import reduce
        from operator import iconcat
        if self.panel != None:
            return [self.panel]
        else:
            return list(reduce(iconcat,map(lambda c: c.listpanels(),self.childs)))
        
    def getnextpanel(self,panel=None):
        self.panelist=self.listpanels()
        if panel != None:
            i = self.panelist.index(panel)
            if i != None:
                return self.panelist [(i+1)%len(self.panelist)]
        else:
            return self.panelist[0]
        
    def handlezonekeydown(self, context, event, keymods):
        if event.key == pygame.K_m and keymods & pygame.KMOD_CTRL:#Minimize zone
            context.focusedpanel.toggleminimised()
        elif event.key == pygame.K_TAB and keymods & pygame.KMOD_CTRL:#Pass focus to next panel in zone
            nextpanel = self.getnextpanel(context.focusedpanel)
            if nextpanel != None:
                context.focusedpanel = nextpanel
        else:
            context.focusedpanel.handlepanelkeydown(event, keymods)

    def update(self):
        for child in self.childs:
            child.update()
        if self.panel != None:
            self.panel.update()

    def draw(self, context, scr, font):
        lineheigth = font.get_linesize()
        for child in self.childs:
            child.draw(context, scr, font)
        if self.panel != None:
            panelcolor = self.panel.getcolor(context)
            panellines = self.panel.draw()
            #TODO secondary array for optional linecolor
            # panellinecolors
            for i in range(len(panellines)):
                scr.blit(font.render(
                    panellines[i], True, panelcolor), (0, i*lineheigth))
