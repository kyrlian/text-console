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

    def resize(self, pctorabs=None):  # change split pct, or just recalc sizes (if Pct==None)
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
                self.childs[0].x = self.x
                self.childs[0].y = self.y
                self.childs[0].w = self.w
                self.childs[0].h = int(self.h * pct)
                self.childs[1].x = self.x
                self.childs[1].y = int(self.y + self.h * pct)
                self.childs[1].w = self.w
                self.childs[1].h = int(self.h * (1-pct))
            else:
                self.childs[0].x = self.x
                self.childs[0].y = self.y
                self.childs[0].w = int(self.w * pct)
                self.childs[0].h = self.h
                self.childs[1].x = int(self.x + self.w * pct)
                self.childs[1].y = self.y
                self.childs[1].w = int(self.w * (1-pct))
                self.childs[1].h = self.h
            self.childs[0].resize()
            self.childs[1].resize()

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
                for i in range(len(sibling.childs)):
                    self.parent.attachzone(sibling.childs[i])
                # resize parent subzones
                self.parent.resize(self.parent.splitpct)
            self.parent = None  # remove my parent from me to free the object

    def handlezoneclick(self, context, button, charx, chary):
        if button == 1:  # left
            if self.panel != None:
                if self.panel.isclicked(charx, chary):
                    context.focusedpanel = self.panel
                    self.panel.handlepanelclick(charx, chary)
                    return True
            for i in range(len(self.childs)):
                done = self.childs[i].handlezoneclick(
                    context, button, charx, chary)
                if done:
                    return True

    def handlezonekeydown(self, context, key):
        if (key == pygame.K_m):
            context.focusedpanel.toggleminimised()

    def update(self):
        for i in range(len(self.childs)):
            self.childs[i].update()
        if self.panel != None:
            self.panel.update()

    def draw(self, context, scr, font):
        lineheigth = font.get_linesize()
        for i in range(len(self.childs)):
            self.childs[i].draw(context, scr, font)
        if self.panel != None:
            panelcolor = self.panel.getcolor(context)
            panellines = self.panel.draw()
            for i in range(len(panellines)):
                scr.blit(font.render(
                    panellines[i], True, panelcolor), (0, i*lineheigth))
