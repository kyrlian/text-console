#kyrlian, 2023

import pygame
import os
from panel import Panel
from cursor import Cursor
from texthelper import TextHelper 

class PanelTextInput(Panel):

    def initcontent(self, initargs=["Loading...","Please wait..."]):
        self.cursor = Cursor()
        self.textlines=self.loadcontent(initargs)
        self.marginleft = 1
        self.marginrigth = 1
    
    def loadcontent(self,initargs):
        if  isinstance(initargs, str) and os.path.isfile(initargs):
            text_file = os.open(initargs,'r')
            lines = text_file.readlines()
            text_file.close()
            return lines
        else:
            if isinstance(initargs, str):
                return [initargs]
            elif isinstance(initargs, list):
                return initargs
            else:
                return []

    def getlinewidth(self):
        if self.zone != None:  # self.zone is None during construction
            innerzonew = self.zone.w
        else:
            innerzonew = 10
        return innerzonew - 2 - self.marginleft - self.marginrigth

    def wordwrap(self,content):
        #TODO ? problem is when.. 
        # if I do on load, I add char returns to the original file - bad
        # if I do on display I create a temp content array, but cursor is relative to text, and if I wordwrap the lines change, need to move the cursor accordingly
        return content
    
    def placecursor(self,textlines):
        cursorx=self.cursor.getchar()
        cursory=self.cursor.getline()
        cursorline = textlines[cursory]
        tmpcontent = []+textlines
        charatcursor = None
        if cursorx <  len(cursorline):
            charatcursor =cursorline[cursorx]
        tmpcontent[cursory] = cursorline[:cursorx] + self.cursor.cyclecursor(charatcursor) + cursorline[cursorx+1:]
        return tmpcontent

    def updatecontent(self):
        self.content = []
        # control line
            # TODO add a control line (Open, Save...)
        # text
        self.content += self.placecursor(self.textlines)
        
    def movecursor(self,cursorx,cursory):
        #print(f"movecursor {cursorx},{cursory}")
        newy = min(max(0,cursory),len(self.textlines)-1)
        self.cursor.setline(newy)
        self.cursor.setchar(min(max(0,cursorx),len(self.textlines[newy])))

    def insertlineat(self,cursory,cursorx):
        #cut current line at x, add new line with cut content
        linetocut  = self.textlines[cursory] 
        leftpart = linetocut[0:cursorx]
        rightpart = linetocut[cursorx+1:]
        self.textlines[cursory] = leftpart
        self.textlines.insert(cursory+1,rightpart)
        self.movecursor(0,cursory+1)

    def insertcharat(self,char,y,x):
        tmpline = self.textlines[y]
        self.textlines[y] =  tmpline[0:x] + char + tmpline[x:]
        self.movecursor(x+1,y)

    def rmcharat(self,y,x):
        tmpline = self.textlines[y]
        self.textlines[y] = tmpline[0:x-1] + tmpline[x:]
        self.movecursor(x-1,y)

    def joinlines(self,y1,y2):
        newcursorx=len( self.textlines[y1])
        self.textlines[y1] = self.textlines[y1]+self.textlines[y2]
        self.textlines.pop(y2)
        self.movecursor(newcursorx,y1)

    def handlepanelkeydown(self, event, keymods):
        cursorx=self.cursor.getchar()
        cursory=self.cursor.getline()
        print(f"handlepanelkeydown: cursory:{cursory}, cursorx:{cursorx}.")
        if event.key == pygame.K_BACKSPACE:
            if cursorx > 0:
                self.rmcharat(cursory,cursorx)
            else:
                self.joinlines(cursory-1,cursory)
        elif event.key == pygame.K_DELETE:
            if cursorx < len(self.textlines[cursory]):
                self.rmcharat(cursory,cursorx+1)
            else:
                self.joinlines(cursory,cursory+1)
        elif event.key == pygame.K_UP:
            self.movecursor(cursorx,cursory-1)
        elif event.key == pygame.K_DOWN:
            self.movecursor(cursorx,cursory+1)
        elif event.key == pygame.K_LEFT:
            if cursorx > 0:
                self.movecursor(cursorx-1,cursory)
            else:
                self.movecursor(cursorx,cursory-1)
        elif event.key == pygame.K_RIGHT:
            if cursorx < len(self.textlines[cursory]):
                self.movecursor(cursorx+1,cursory)
            else:
                self.movecursor(cursorx,cursory+1)
        elif event.key == pygame.K_HOME:
            self.movecursor(0,0)
        elif event.key == pygame.K_END:
             self.movecursor( len(self.textlines[ len(self.textlines)-1]) ,len(self.textlines))
        elif event.key == pygame.K_RETURN:
            self.insertlineat(cursory,cursorx)
        elif event.key == pygame.K_TAB:
            #TAB is 2 spaces
            self.insertcharat(" ",cursory,cursorx)
            self.insertcharat(" ",cursory,cursorx)
        else:  # Unicode standard is used for string formation
            if event.unicode.isprintable():
                self.insertcharat(event.unicode,cursory,cursorx)

    def handletextclick(self, event, charx, chary):
        # calculate char line and col
        cursory = chary - self.zone.y - 2  # add -x control lines if needed
        cursorx = charx - self.zone.x - 2
        self.movecursor(cursorx,cursory)

    def handlepanelclick(self, event, charx, chary):
        self.handletextclick(event, charx, chary)
        self.handlecontrolclick(event, charx, chary)
