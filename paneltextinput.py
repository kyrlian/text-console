import pygame
import os
from panel import Panel
from cursor import Cursor
from texthelper import TextHelper 

class PanelTextInput(Panel):

    def initcontent(self, fileorteext=["Loading...","Please wait..."]):
        self.cursor = Cursor()
        self.textlines=self.loadcontent(fileorteext)
        #self.textbeforecursor = content
        #self.textaftercursor = ""
        #self.fulltext = self.textbeforecursor + self.textaftercursor
        self.marginleft = 1
        self.marginrigth = 1
    
    def loadcontent(self,fileorteext):
        if os.path.isfile(fileorteext):
            text_file = os.open(fileorteext,'r')
            lines = text_file.readlines()
            text_file.close()
            return lines
        else:
            if TextHelper.ismultiline(fileorteext):
                return fileorteext
            else:
                return [fileorteext]

    def getlinewidth(self):
        if self.zone != None:  # self.zone is None during construction
            innerzonew = self.zone.w
        else:
            innerzonew = 10
        return innerzonew - 2 - self.marginleft - self.marginrigth

    def wordwrap(self,content):
        #TODO
        return content
    
    def updatecontent(self):
        self.content = []
        # control line
            # TODO add a control line (Open, Save...)
        # text content
        #restoftext = self.textbeforecursor + self.cursor.symbol + self.textaftercursor
        #linewidth = self.getlinewidth()
        # while len(restoftext) > 0 :
        #     nbtake = min(linewidth, len(restoftext))
        #     line = restoftext[0:nbtake]
        #     nbtaken = len(line)
        #     if "\n" in line:
        #         line = line.split("\n")[0]
        #         nbtaken = len(line)+1
        #     restoftext = restoftext[nbtaken:]
        #     self.content.append(line.replace("\t","  "))
        self.content = self.content + self.wordwrap(self.textlines)
        self.cursor.cyclecursor()

    # def recalctextbeforeafter(self):
    #     self.fulltext = self.textbeforecursor + self.textaftercursor
    #     self.cursor.position = min(max(0, self.cursor.position), len(self.fulltext))
    #     self.textbeforecursor = self.fulltext[0:self.cursor.position]
    #     self.textaftercursor = self.fulltext[self.cursor.position:]
    #     self.fulltext = self.textbeforecursor + self.textaftercursor

    def movecursor(self,cursorx,cursory):
        #print(f"movecursor {cursorx},{cursory}")
        newy = min(max(0,cursory),len(self.textlines)-1)
        self.cursor.setline(newy)
        self.cursor.setchar(min(max(0,cursorx),len(self.textlines[newy])))

    def insertlineat(self,cursory):
        self.textlines.insert(cursory+1,"")
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
        self.textlines[y1] = self.textlines[y1]+self.textlines[y2]
        self.textlines.pop(y2)
        
    def handlepanelkeydown(self, event, keymods):
        cursorx=self.cursor.char()
        cursory=self.cursor.line()
        print(f"handlepanelkeydown: cursory:{cursory}, cursorx:{cursorx}.")
        if event.key == pygame.K_BACKSPACE:
            if cursorx > 0:
                self.rmcharat(cursory,cursorx-1)
            else:
                self.joinlines(cursory-1,cursory)
        elif event.key == pygame.K_DELETE:
            if cursorx < len(self.textlines[cursory]):
                self.rmcharat(cursory,cursorx)
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
            self.insertlineat(cursory)
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
