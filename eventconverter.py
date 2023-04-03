import pygame
import curses

KEY_a=1
KEY_b=2
KEY_c=3
KEY_h=4
KEY_m=5
KEY_q=6
KEY_s=16
KEY_t=17
KEY_v=18
KEY_w=19
KEY_x=20
KEY_RIGHT=31
KEY_LEFT=32
KEY_UP=33
KEY_DOWN=34
KEY_SPACE=35
KEY_HOME=36
KEY_END=37
KEY_BACKSPACE=38
KEY_DELETE=39
KEY_RETURN=40
KEY_ESCAPE=41
KEY_TAB=42

TYPE_QUIT=101
TYPE_KEYDOWN = 102
TYPE_MOUSEBUTTONDOWN = 103

KMOD_CTRL=201

# TODO merge with renderer ? (commonInterface ?)
class CommonEvent():
    def __init__(self, type,key, keymod, unicode, btn,mx,my):
        self.type = type
        self.key = key
        self.btn = btn
        self.mousex = mx
        self.mousey = my
        self.keymods = keymod
        self.unicode = unicode
     
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
            commmoneventtype=None
            commmoneventkey=None
            commmoneventkeymod=None
            commoneventunicode=None
            commmoneventbtn=None
            commmoneventmx=None 
            commmoneventmy=None
            if event.type == pygame.QUIT:
                commmoneventtype =TYPE_QUIT
            elif event.type == pygame.KEYDOWN:
                commmoneventtype = TYPE_KEYDOWN
                conv = {
                    pygame.K_UP:KEY_UP,
                    pygame.K_DOWN:KEY_DOWN,
                    pygame.K_b:KEY_b,
                    pygame.K_c:KEY_c,
                    pygame.K_h:KEY_h,
                    pygame.K_m:KEY_m,
                    pygame.K_s:KEY_s,
                    pygame.K_t:KEY_t,
                    pygame.K_v:KEY_v,
                    pygame.K_w:KEY_w,
                    pygame.K_x:KEY_x,
                    pygame.K_SPACE:KEY_SPACE,
                    pygame.K_RIGHT:KEY_RIGHT,
                    pygame.K_LEFT:KEY_LEFT,
                    pygame.K_UP:KEY_UP,
                    pygame.K_DOWN:KEY_DOWN,
                    pygame.K_HOME:KEY_HOME,
                    pygame.K_END:KEY_END,
                    pygame.K_TAB:KEY_TAB,
                    pygame.K_BACKSPACE:KEY_BACKSPACE,
                    pygame.K_DELETE:KEY_DELETE,
                    pygame.K_RETURN:KEY_RETURN,
                    pygame.K_ESCAPE:KEY_ESCAPE
                }
                if event.key in conv: commmoneventkey=conv[event.key]
                commoneventunicode = event.unicode #keep unicode as-is
                if pygame.key.get_mods() & pygame.KMOD_CTRL:  # CTRL keys
                    commmoneventkeymod = KMOD_CTRL
            elif event.type == pygame.MOUSEBUTTONDOWN:
                commmoneventtype = TYPE_MOUSEBUTTONDOWN
                clickx, clicky = pygame.mouse.get_pos()
                # btn= TODO read button status left/right/mid
                commmoneventmx = int(clickx / self.charwidth)
                commmoneventmy = int(clicky / self.lineheigth)
            return CommonEvent(commmoneventtype, commmoneventkey, commmoneventkeymod, commoneventunicode, commmoneventbtn,commmoneventmx,commmoneventmy)

    def convertfromcurses(self,event):
        commmoneventtype=None
        commmoneventkey=None
        commmoneventkeymod=None
        commoneventunicode=None
        commmoneventbtn=None
        commmoneventmx=None 
        commmoneventmy=None
        if event == curses.KEY_MOUSE:
            commmoneventtype = TYPE_MOUSEBUTTONDOWN
            mid, mx, my, mz, mbstate = curses.getmouse()
            # btn= TODO read button status left/right/mid
        else :
            commmoneventtype =TYPE_KEYDOWN
            conv = {
                curses.KEY_SPACE:KEY_SPACE,
                ord('q'): KEY_q
            }
            if event in conv: commmoneventkey=conv[event]
        return CommonEvent(commmoneventtype, commmoneventkey, commmoneventkeymod, commoneventunicode, commmoneventbtn,commmoneventmx,commmoneventmy)

