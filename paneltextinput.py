from panel import Panel
import pygame
from cursor import Cursor

class PanelTextInput(Panel):

    def initcontent(self, content):
        self.cursor = Cursor()
        # TODO handle an x,y content ?
        # and position the text on display
        # edit would need to "place" the text at the correct line (not reuild before.after)
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
        restoftext = self.textbeforecursor + self.cursor.symbol + self.textaftercursor
        linewidth = self.getlinewidth()
        while len(restoftext) > 0 :
            nbtake = min(linewidth, len(restoftext))
            line = restoftext[0:nbtake]
            nbtaken = len(line)
            if "\n" in line:
                line = line.split("\n")[0]
                nbtaken = len(line)+1
            restoftext = restoftext[nbtaken:]
            self.content.append(line.replace("\t","  "))
        self.cursor.cyclecursor()

    def recalctextbeforeafter(self):
        self.fulltext = self.textbeforecursor + self.textaftercursor
        self.cursor.position = min(max(0, self.cursor.position), len(self.fulltext))
        self.textbeforecursor = self.fulltext[0:self.cursor.position]
        self.textaftercursor = self.fulltext[self.cursor.position:]
        self.fulltext = self.textbeforecursor + self.textaftercursor

    def handlepanelkeydown(self, event, keymods):
        # Check for backspace
        if event.key == pygame.K_BACKSPACE:
            self.textbeforecursor = self.textbeforecursor[:-1]# get text input from 0 to -1 i.e. end.
            self.cursor.position -= 1
        elif event.key == pygame.K_DELETE:
            self.textaftercursor = self.textaftercursor[1:]
            # backspace doesnt change cursor position in text
        elif event.key == pygame.K_UP:
            # depends:because of CRLF, same x on previous line is probably not a full line width before
            self.cursor.position -= self.getlinewidth()
        elif event.key == pygame.K_DOWN:
            self.cursor.position += self.getlinewidth()
        elif event.key == pygame.K_LEFT:
            self.cursor.position -= 1
        elif event.key == pygame.K_RIGHT:
            self.cursor.position += 1
        elif event.key == pygame.K_HOME:
            self.cursor.position =0
        elif event.key == pygame.K_END:
            self.cursor.position = len(self.fulltext)
        elif event.key == pygame.K_RETURN:
            self.textbeforecursor += "\n"
            self.cursor.position += 1
        else:  # Unicode standard is used for string formation
            if event.unicode.isprintable():
                self.textbeforecursor += event.unicode
                self.cursor.position += 1
        self.recalctextbeforeafter()

    def handletextclick(self, event, charx, chary):
        # calculate char line and col
        linecliked = chary - self.zone.y - 2  # add -x control lines if needed
        columncliked = charx - self.zone.x - 2
        # reposition cursor in text
        linewidth = self.getlinewidth()
        self.cursor.position = linecliked * linewidth + columncliked
        self.recalctextbeforeafter()

    def handlepanelclick(self, event, charx, chary):
        self.handletextclick(event, charx, chary)
        self.handlecontrolclick(event, charx, chary)
