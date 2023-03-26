import pygame
import curses

K_RIGHT=12
K_LEFT=13
K_UP=14
K_DOWN=15
K_b=2
K_c=3
K_h=4
K_m=5
K_q=25
K_s=6
K_t=7
K_v=8
K_w=9
K_x=10
K_SPACE=11
K_HOME=16
K_END=17
K_BACKSPACE=18
K_DELETE=19
K_RETURN=20
QUIT=21
K_ESCAPE=22
KEYDOWN = 23
MOUSEBUTTONDOWN = 24


# TODO merge with renderer (commonInterface ?)
class CommonEvent():
    def __init__(self, type,key, btn,mx,my):
        self.type = type
        self.key = key
        self.btn = btn
        self.mousex = mx
        self.mousey = my
     
class EventConverter():
    def __init__(self, mode="pygame", charwidth=1, lineheigth=1):
        self.mode  = mode
        self.charwidth = charwidth
        self.lineheigth = lineheigth

    def convert(self,event):
        if self.mode == "pygame":
            return self.convertfrompygame(event)
        elif self.mode=="curses":
            return self.convertfromcurses(event)
            
    def convertfrompygame(self,event):
            type=None
            key=None
            btn=None
            mx=None 
            my=None
            if event.type == pygame.QUIT:
                type =QUIT
            elif event.type == pygame.KEYDOWN:
                type =KEYDOWN
                conv = {
                    pygame.K_UP:K_UP,
                    pygame.K_DOWN:K_DOWN,
                    pygame.K_b:K_b,
                    pygame.K_c:K_c,
                    pygame.K_h:K_h,
                    pygame.K_m:K_m,
                    pygame.K_s:K_s,
                    pygame.K_t:K_t,
                    pygame.K_v:K_v,
                    pygame.K_w:K_w,
                    pygame.K_x:K_x,
                    pygame.K_SPACE:K_SPACE,
                    pygame.K_RIGHT:K_RIGHT,
                    pygame.K_LEFT:K_LEFT,
                    pygame.K_UP:K_UP,
                    pygame.K_DOWN:K_DOWN,
                    pygame.K_HOME:K_HOME,
                    pygame.K_END:K_END,
                    pygame.K_BACKSPACE:K_BACKSPACE,
                    pygame.K_DELETE:K_DELETE,
                    pygame.K_RETURN:K_RETURN,
                    pygame.K_ESCAPE:K_ESCAPE
                }
                if event.key in conv: key=conv[event.key]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                type = MOUSEBUTTONDOWN
                clickx, clicky = pygame.mouse.get_pos()
                # btn= TODO read button status left/right/mid
                mx = int(clickx / self.charwidth)
                my = int(clicky / self.lineheigth)
            return CommonEvent(type, key, btn,mx,my)

    def convertfromcurses(self,event):
        type=None
        key=None
        btn=None
        mx=None 
        my=None
        if event == curses.KEY_MOUSE:
            type = MOUSEBUTTONDOWN
            mid, mx, my, mz, mbstate = curses.getmouse()
            # btn= TODO read button status left/right/mid
        else :
            type =KEYDOWN
            conv = {
                curses.KEY_SPACE:K_SPACE,
                ord('q'): K_q
            }
            if event in conv: key=conv[event]
        return CommonEvent(type, key, btn,mx,my)

