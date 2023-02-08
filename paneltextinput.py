from panel import Panel
import pygame

class PanelTextInput(Panel):

    def initcontent(self,content):
        self.cursorpos = 0
        self.cursorsymbols=["░","▓"] # 	█░▒▓
        self.cursorsymbol=self.cursorsymbols[0]
        self.textbeforecursor = content
        self.textaftercursor = ""
        self.marginleft = 1
        self.marginrigth = 1

    def cyclecursor(self):
        i = self.cursorsymbols.index(self.cursorsymbol)
        nexti = (i+1)%len(self.cursorsymbols)
        self.cursorsymbol = self.cursorsymbols[nexti]

    def updatecontent(self):
        #user edits textbeforecursor
        self.fulltext = self.textbeforecursor + self.textaftercursor
        #handle line breaks
        if self.zone != None: # self.zone is None during construction
            innerzonew = self.zone.w
        else:
            innerzonew=10
        linewidth = innerzonew - 2 - self.marginleft - self.marginrigth 
        self.content = []
        restoftext = self.textbeforecursor +  self.cursorsymbol + self.textaftercursor
        while len(restoftext)>0:
            nbtake = min(linewidth,len(restoftext))
            line = restoftext[0:nbtake]
            self.content.append(line)
            restoftext = restoftext[nbtake:]
        print(self.content)
        self.cyclecursor()

    def movecursorleftright(self,dir):
        self.cursorpos = min( max(0, self.cursorpos + dir),len(self.fulltext) )
        self.textbeforecursor = self.fulltext[0:self.cursorpos]
        self.textaftercursor = self.fulltext[self.cursorpos:]
        #next updatecontent will rebuild full text

    def handlepanelkeydown(self, event, keymods):
            # Check for backspace
            if event.key == pygame.K_BACKSPACE:
                # get text input from 0 to -1 i.e. end.
                self.textbeforecursor = self.textbeforecursor[:-1]
            elif event.key == pygame.K_UP:
                #TODO move cursor up, manage line break :)
                print("TODO move cursor up")
            elif event.key == pygame.K_DOWN:
                #TODO move cursor down, manage line break :)
                print("TODO move cursor down")
            elif event.key == pygame.K_LEFT:
                self.movecursorleftright(-1)
            elif event.key == pygame.K_RIGHT:
                self.movecursorleftright(1)
            # Unicode standard is used for string formation
            else:
                self.textbeforecursor += event.unicode