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
        self.focusedpanel = -1
    
class Panel:
    controls = "-□x"

    def __init__(self, x=0, y=0, w=0, h=0, title="", content="", status="normal", focus=False):
        self.x = x
        self.y = y
        self.w = max(w, len(title)+2+len(Panel.controls))
        self.h = h
        self.title = title
        self.status = status
        self.hasfocus = focus
        self.innercursorx = 0
        self.innercursory = 0
        self.updatecontent(content)

    def updatecontent(self,content):
        self.content = content
        self.contentheigth = 0
        if len(self.content) > 0:
            self.contentheigth = 1
            if len(self.content[0]) > 1:  # if txt is an array (multiline)
                self.contentheigth = len(self.content)
        self.updatecurrenth()

    def updatecurrenth(self):
        if self.status == "minimized":
            self.currenth = self.h
        else:
            self.currenth = max(self.h,self.contentheigth+2)

    def toggleminimised(self):
        if self.status == "minimized":
            self.status = "normal"
        else:
            self.status = "minimized"
        self.updatecurrenth()
        
    def getcolor(self):
        if self.hasfocus:
            return (200,200,200)
        else:
            return (100,100,100)
    def isclicked(self ,charx,chary):
        return charx>= self.x and charx <= self.x + self.w and chary >= self.y and chary <= self.y + self.currenth
    
    def handlecontrolclicked(self , charx, chary):
        controlsminpos = -4 #"-□x"
        controlsmaxpos = -3
        controlsclosepos = -2
        if  chary == self.y:
            if charx == self.x + self.w + controlsminpos :
                print("clicked minimize")
                self.toggleminimised() 
            elif charx == self.x + self.w + controlsmaxpos:
                print("clicked maximize")
                self.toggleminimised() 
            elif charx == self.x + self.w + controlsclosepos:
                print("clicked close")

    def handleclick(self , charx, chary):
        self.handlecontrolclicked(charx, chary)

    def draw(self):
        txtarray = []
        for i in range(self.y):
            txtarray.append("")
        txtarray.append(" "*self.x+"╔"+self.title+"═"*(self.w-2-len(self.title) -
                        len(Panel.controls))+Panel.controls+"╗")  # top border
        if self.status == "normal" and self.contentheigth >0 :
            if self.contentheigth > 1:  # if txt is an array (multiline)
                for ti in range(self.contentheigth):
                    txtline = self.content[ti]
                    txtarray.append(" "*self.x+"║"+txtline +
                                    " "*(self.w-2-len(txtline))+"║")
            else:
                txtarray.append(" "*self.x+"║"+self.content +
                                " "*(self.w-2-len(self.content))+"║")
            for i in range(self.h-2-self.contentheigth):
                txtarray.append(" "*self.x+"║"+" "*(self.w-2)+"║")
        txtarray.append(" "*self.x+"╚"+"═"*(self.w-2)+"╝")  # bottom border
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

def updatepanels(context,panels, action,button,charx=None,chary=None):
    if action=="click":
        if button == 1: #left
            ci=-1
            for i in range(len(panels)):
                panels[i].hasfocus=False
                if panels[i].isclicked(charx,chary):
                    ci=i
                    panels[i].handleclick(charx,chary)
            if ci>-1:
                panels[ci].hasfocus=True
                context.focusedpanel=ci

    if action=="keydown":
        key=button
        if(key==pygame.K_m):
            panels[context.focusedpanel].toggleminimised()

def initcontext():
    return Context()

def initpanels(screenw,screenh):
    tl = ["Big","Square"]
    sq1 = Panel(0, 0, screenw-1, screenh-1, "", tl, "normal")
    sq2 = Panel(50, 10, 50, 20, "title")
    sq3 = Panel(52, 11, 10, 10, "focused", "content","normal",True)
    txtb = Panel(10, 10, 1, 1, "Small text box!")
    txtb2 = Panel(10, 10, 1, 1, "smal box",["with","several","text lines"])
    return [sq1, sq2, sq3, txtb,txtb2]#low to high
 
def drawscreen(scr, font, panels):
    lineheigth = font.get_linesize()
    for i in range(len(panels)):
        panelcolor = panels[i].getcolor()
        panellines = panels[i].draw()
        for i in range(len(panellines)):
            scr.blit(font.render(panellines[i],
                    True, panelcolor), (0, i*lineheigth))
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
    context = initcontext()
    panels = initpanels(linewidth,maxlines)
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
                    updatepanels(context, panels, "keydown", event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 1 - left click, 2 - middle click, 3 - right click, 4 - scroll up, 5 - scroll down
                if event.button == 1: # left click
                    clickx, clicky = pygame.mouse.get_pos()
                    charx = int(clickx / charwidth)
                    chary = int(clicky / lineheigth)
                    print(str(charx)+ " "+str(chary))
                    updatepanels(context, panels, "click",event.button,charx,chary)
        screen.fill(bgcolor)
        drawscreen(screen, font, panels)
        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
    sys.exit()
