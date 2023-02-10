from panel import Panel
import pygame
from cursor import Cursor

class PanelTextInput(Panel):

    def initcontent(self, content):
        self.cursor = Cursor()
        self.textlines=["l1","l2"]
        self.textbeforecursor = content
        self.textaftercursor = ""
        self.fulltext = self.textbeforecursor + self.textaftercursor
        self.marginleft = 1
        self.marginrigth = 1

    def getlinewidth(self):
        if self.zone != None:  # self.zone is None during construction
            innerzonew = self.zone.w
        else:
            innerzonew = 10
        return innerzonew - 2 - self.marginleft - self.marginrigth

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
        self.content = self.content + self.textlines
        self.cursor.cyclecursor()

    def recalctextbeforeafter(self):
        self.fulltext = self.textbeforecursor + self.textaftercursor
        self.cursor.position = min(max(0, self.cursor.position), len(self.fulltext))
        self.textbeforecursor = self.fulltext[0:self.cursor.position]
        self.textaftercursor = self.fulltext[self.cursor.position:]
        self.fulltext = self.textbeforecursor + self.textaftercursor

    def placecharatcursor(self,c):
        cursorx=self.cursor.char()
        cursory=self.cursor.line()
        tmpline = self.textlines[cursory]
        newline = tmpline[0:cursorx] + c + tmpline[cursorx:]
        self.cursor.position[0] +=1
        self.textlines[cursory] = newline

    def backspace(self):
        cursorx=self.cursor.char()
        cursory=self.cursor.line()
        tmpline = self.textlines[cursory]
        #todo if cursor at 0 merge lines
        newline = tmpline[0:cursorx-1] + tmpline[cursorx:]
        self.cursor.position[0] = max(0,self.cursor.position[0]-1)
        self.textlines[cursory] = newline

    def handlepanelkeydown(self, event, keymods):
        # Check for backspace
        if event.key == pygame.K_BACKSPACE:
            #self.textbeforecursor = self.textbeforecursor[:-1]# get text input from 0 to -1 i.e. end.
            #self.cursor.position -= 1
            self.backspace()
        elif event.key == pygame.K_DELETE:
            self.textaftercursor = self.textaftercursor[1:]
            # backspace doesnt change cursor position in text
        elif event.key == pygame.K_UP:
            # depends:because of CRLF, same x on previous line is probably not a full line width before
            self.cursor.position -= self.getlinewidth()
        elif event.key == pygame.K_DOWN:
            self.cursor.position += self.getlinewidth()
        elif event.key == pygame.K_LEFT:
            # self.cursor.position -= 1
            self.cursor.position[0] = max(self.cursor.position[0]-1, 0)
        elif event.key == pygame.K_RIGHT:
            self.cursor.position[0] = min(self.cursor.position[0]-1, len(self.textlines[self.cursor.position[1]])-1)
            # self.cursor.position += 1
        elif event.key == pygame.K_HOME:
            self.cursor.position =[0,0]
        elif event.key == pygame.K_END:
            self.cursor.position = len(self.fulltext)
        elif event.key == pygame.K_RETURN:
            self.textbeforecursor += "\n"
            self.cursor.position += 1
        else:  # Unicode standard is used for string formation
            if event.unicode.isprintable():
                self.placecharatcursor(event.unicode)
                #self.textbeforecursor += event.unicode
                #self.cursor.position += 1
        #self.recalctextbeforeafter()

    def handletextclick(self, event, charx, chary):
        # calculate char line and col
        linecliked = chary - self.zone.y - 2  # add -x control lines if needed
        columncliked = charx - self.zone.x - 2
        # reposition cursor in text
        self.cursor.position[1] = min(linecliked, len(self.textlines)-1)
        self.cursor.position[0] = min(columncliked, len(self.textlines[self.cursor.position[1]])-1)
        #linewidth = self.getlinewidth()
        #self.cursor.position = linecliked * linewidth + columncliked
        #self.recalctextbeforeafter()

    def handlepanelclick(self, event, charx, chary):
        self.handletextclick(event, charx, chary)
        self.handlecontrolclick(event, charx, chary)
