import curses
from renderer import Renderer

# https://docs.python.org/3/library/curses.html

class RendererCurses(Renderer):

    def __init__(self):
        screen = curses.initscr() 
        #curses.noecho() 
        curses.curs_set(0) 
        screen.keypad(1) 
        curses.mousemask(1)

    def renderline(self,line,color,x,y):
        pass #TODO

    def refresh(self):
        pass #TODO

    def quit(self):
        curses.endwin()