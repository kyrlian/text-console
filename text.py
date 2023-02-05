import sys
import pygame


# single line borders - https://en.wikipedia.org/wiki/Box_Drawing
# 	        0 	1 	2 	3 	4 	5 	6 	7 	8 	9 	A 	B 	C 	D 	E 	F
# U+250x 	─ 	━ 	│ 	┃ 	┄ 	┅ 	┆ 	┇ 	┈ 	┉ 	┊ 	┋ 	┌ 	┍ 	┎ 	┏
# U+251x 	┐ 	┑ 	┒ 	┓ 	└ 	┕ 	┖ 	┗ 	┘ 	┙ 	┚ 	┛ 	├ 	┝ 	┞ 	┟
# U+252x 	┠ 	┡ 	┢ 	┣ 	┤ 	┥ 	┦ 	┧ 	┨ 	┩ 	┪ 	┫ 	┬ 	┭ 	┮ 	┯
# U+253x 	┰ 	┱ 	┲ 	┳ 	┴ 	┵ 	┶ 	┷ 	┸ 	┹ 	┺ 	┻ 	┼ 	┽ 	┾ 	┿
# U+254x 	╀ 	╁ 	╂ 	╃ 	╄ 	╅ 	╆ 	╇ 	╈ 	╉ 	╊ 	╋ 	╌ 	╍ 	╎ 	╏
# U+255x 	═ 	║ 	╒ 	╓ 	╔ 	╕ 	╖ 	╗ 	╘ 	╙ 	╚ 	╛ 	╜ 	╝ 	╞ 	╟
# U+256x 	╠ 	╡ 	╢ 	╣ 	╤ 	╥ 	╦ 	╧ 	╨ 	╩ 	╪ 	╫ 	╬ 	╭ 	╮ 	╯
# U+257x 	╰ 	╱ 	╲ 	╳ 	╴ 	╵ 	╶ 	╷ 	╸ 	╹ 	╺ 	╻ 	╼ 	╽ 	╾ 	╿
# blocks - https://en.wikipedia.org/wiki/Block_Elements
# 	█ 	Full block
# 	░ 	Light shade
# 	▒ 	Medium shade
# 	▓ 	Dark shade
# 	▙ 	Quadrant upper left and lower left and lower right
# 	▛ 	Quadrant upper left and upper right and lower left
# 	▜ 	Quadrant upper left and upper right and lower right
# 	▟ 	Quadrant upper right and lower left and lower right
# 	▀ 	Upper half block
# 	▄ 	Lower half block
# 	▌ 	Left half block
# 	▐ 	Right half block

class Context:
    def __init__(self):
        self.focusedpanel = None


class Zone:
    def __init__(self, x=0, y=0, w=0, h=0, parent=None, panel=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.parent = parent
        self.panel = panel
        self.childs = []
        self.addpanel(panel)

    def addpanel(self, panel):
        if panel != None:
            self.panel = panel
            self.childs = []
            panel.attachtozone(self)

    def removepanel(self):
        self.panel = None

    def split(self, dir, pct):
        self.splitdir = dir
        self.splitpct = pct
        if dir == "h":  # horizontal split
            subz1 = Zone(self.x, self.y, self.w, int(self.h * pct), self, self.panel)
            subz2 = Zone(self.x, int(self.y + self.h * pct),self.w, int(self.h * (1-pct)), self, Panel("temp"))
            self.childs = [subz1, subz2]
        else:  # vertical spli
            subz1 = Zone(self.x, self.y, int(self.w * pct),self.h, self, self.panel)
            subz2 = Zone(int(self.x + self.w * pct), self.y,int(self.w * (1-pct)), self.h, self, Panel("temp"))
            self.childs = [subz1, subz2]
        self.removepanel()
        return subz1, subz2

    def resize(self, pct):  # change split pct
        self.splitpct = pct
        if self.splitdir == "h":
            self.childs[0].y = self.y
            self.childs[0].h = int(self.h * pct)
            self.childs[1].y = int(self.y + self.h * pct)
            self.childs[1].h = int(self.h * (1-pct))
        else:
            self.childs[0].x = self.x
            self.childs[0].w = int(self.w * pct)
            self.childs[1].x = int(self.x + self.w * pct)
            self.childs[1].w = int(self.w * (1-pct))

    def remove(self):  # remove me from my parent, my parent will have only one child, so put my sibling in place of my parent in my grandparent
        self.parent.childs.remove(self)  # remove me from my parent
        print("parent childs:"+str(len(self.parent.childs)))
        for i in range(len(self.parent.parent.childs)):
            if self.parent.parent.childs[i] == self.parent:# remove my parent from his parent
                self.parent.parent.childs[i] = self.parent.childs[0]  # put my sibling instead
                print("raplaced, grand parent childs:"+str(len(self.parent.parent.childs)))
        self.parent.parent.resize(self.parent.parent.splitpct)# resize grandparent subzones
        self.parent = None  # remove my parent from me to free the object

    def handlezoneclick(self, context, button, charx, chary):
        if button == 1:  # left
            if self.panel != None:
                if self.panel.isclicked(charx, chary):
                    context.focusedpanel = self.panel
                    self.panel.handlepanelclick(charx, chary)
                    return True
            for i in range(len(self.childs)):
                done = self.childs[i].handlezoneclick(context, button, charx, chary)
                if done:
                    return True

    def handlezonekeydown(context, key):
        if (key == pygame.K_m):
            context.focusedpanel.toggleminimised()

    def draw(self,context, scr, font):
        lineheigth = font.get_linesize()
        for i in range(len(self.childs)):
            self.childs[i].draw(context,scr, font)
        if self.panel != None:
            panelcolor = self.panel.getcolor(context)
            panellines = self.panel.draw()
            for i in range(len(panellines)):
                scr.blit(font.render(
                    panellines[i], True, panelcolor), (0, i*lineheigth))


class Panel:

    def __init__(self, title="", content="", status="normal"):
        self.controls = "□_|x"
        self.title = title
        self.status = status
        self.innercursorx = 0
        self.innercursory = 0
        self.updatecontent(content)

    def attachtozone(self, zone):
        self.zone = zone

    def updatecontent(self, content):
        self.content = content
        self.contentheigth = 0
        if len(self.content) > 0:
            self.contentheigth = 1
            if len(self.content[0]) > 1:  # if txt is an array (multiline)
                self.contentheigth = len(self.content)

    def toggleminimised(self):
        if self.status == "minimized":
            self.status = "normal"
            self.zone.parent.resize(.5)
        elif self.status == "normal":
            self.status = "maximized"
            self.zone.parent.resize(.9)
        else:
            self.status = "minimized"
            self.zone.parent.resize(.1)

    def getcolor(self,context):
        if context.focusedpanel == self:
            return (200, 200, 200)
        else:
            return (100, 100, 100)

    def isclicked(self, charx, chary):
        return charx >= self.zone.x and charx < self.zone.x + self.zone.w and chary >= self.zone.y and chary < self.zone.y + self.zone.h

    def handlecontrolclick(self, charx, chary):
        controlsminimize = -5  # "□_|x"
        controlssplith = -4
        controlssplitv = -3
        controlsclose = -2
        if chary == self.zone.y:
            if charx == self.zone.x + self.zone.w + controlsminimize:
                print("clicked minimize")
                self.toggleminimised()
            elif charx == self.zone.x + self.zone.w + controlssplith:
                print("clicked split h")
                self.zone.split("h", .5)
            elif charx == self.zone.x + self.zone.w + controlssplitv:
                print("clicked split v")
                self.zone.split("v", .5)
            elif charx == self.zone.x + self.zone.w + controlsclose:
                print("clicked close")
                self.zone.remove()

    def handlepanelclick(self, charx, chary):
        self.handlecontrolclick(charx, chary)

    def draw(self):
        txtarray = []
        for i in range(self.zone.y):
            txtarray.append("")
        txtarray.append(" "*self.zone.x+"╔"+self.title+"═"*(self.zone.w-2-len(self.title) -
                        len(self.controls))+self.controls+"╗")  # top border
        if self.contentheigth > 0:
            if self.contentheigth > 1:  # if txt is an array (multiline)
                for ti in range(self.contentheigth):
                    txtline = self.content[ti]
                    txtarray.append(" "*self.zone.x+"║"+txtline +
                                    " "*(self.zone.w-2-len(txtline))+"║")
            else:
                txtarray.append(" "*self.zone.x+"║"+self.content +
                                " "*(self.zone.w-2-len(self.content))+"║")
        for i in range(self.zone.h-2-self.contentheigth):
            txtarray.append(" "*self.zone.x+"║"+" "*(self.zone.w-2)+"║")
        txtarray.append(" "*self.zone.x+"╚"+"═" *
                        (self.zone.w-2)+"╝")  # bottom border
        return (txtarray)


class TxtHelper:
    def getline(ar, y):
        if (y < len(ar)):
            return ar[y]
        return ""

    def getchar(ar, x, y):
        if (y < len(ar)):
            if (x < len(ar[y])):
                return ar[y][x:x+1]
        return ""

    def mergetwoarrays(a, b):
        o = []
        for y in range(max(len(a), len(b))):
            to = ""
            la = TxtHelper.getline(a, y)
            lb = TxtHelper.getline(b, y)
            for x in range(max(len(la), len(lb))):
                tto = TxtHelper.getchar(a, x, y)
                cb = TxtHelper.getchar(b, x, y)
                if cb != "" and cb != " ":
                    tto = cb
                to += tto
            o.append(to)
        return o

    def mergearrays(aa):
        o = aa[0]
        for i in range(1, len(aa), 1):
            o = TxtHelper.mergetwoarrays(o, aa[i])
        return o





def initcontext():
    return Context()


def initrootzone(screenw, screenh):
    rootzone = Zone(0, 0, screenw-1, screenh-1)
    lzone, rzone = rootzone.split("v", .4)
    lzone.addpanel(Panel("Left", ["Big", "Square"]))
    rzone.addpanel(Panel("Right", ["with", "several", "text lines"]))
    return rootzone


def main():
    displayinfo = pygame.display.Info()
    screen = pygame.display.set_mode(
        (displayinfo.current_w, displayinfo.current_h), pygame.FULLSCREEN)
    # print(pygame.font.get_fonts())
    font = pygame.font.SysFont('lucidaconsole', 15)
    lineheigth = font.get_linesize()
    charwidth, charheigth = font.size(" ")
    maxlines = int(screen.get_height()/lineheigth)
    linewidth = int(screen.get_width()/charwidth)
    rootzone = initrootzone(linewidth, maxlines)
    context = initcontext()
    bgcolor = (30, 30, 30)
    clock = pygame.time.Clock()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                else:
                    rootzone.handlezonekeydown(context,  event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 1 - left click, 2 - middle click, 3 - right click, 4 - scroll up, 5 - scroll down
                if event.button == 1:  # left click
                    clickx, clicky = pygame.mouse.get_pos()
                    charx = int(clickx / charwidth)
                    chary = int(clicky / lineheigth)
                    print(str(charx) + " "+str(chary))
                    rootzone.handlezoneclick(context,  event.button, charx, chary)
        screen.fill(bgcolor)
        rootzone.draw(context,screen, font)
        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
    sys.exit()
