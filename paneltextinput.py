""" Text editor panel """
# kyrlian, 2023

import os
import pygame
from panel import Panel
from cursor import Cursor


class PanelTextInput(Panel):
    """ Text editor panel """

    def __init__(self, title="Text editor", initargs=None, status="normal"):
        Panel.__init__(self, title, initargs, status)
        self.textcursor = Cursor() #cursor in the orginal text
        self.wrappedcursor = Cursor(["░",""])#cursor in the wraped text
        self.textlines = self.loadcontent(initargs)
        self.wordwrapflag = False
        self.wrappinginfo = []
        self.wrapedlines = []
    
    def loadcontent(self, initargs):
        """ Load file or text content """
        if isinstance(initargs, str) and os.path.isfile(initargs):
            text_file = open(initargs, 'r')
            lines = text_file.readlines()
            text_file.close()
            return lines        
        if isinstance(initargs, str):
            return [initargs]
        if isinstance(initargs, list):
            return initargs
        return []

    def getlinewidth(self):
        """ get max line width """
        if self.zone is not None:  # self.zone is None during construction
            innerzonew = self.zone.w
        else:
            innerzonew = 10
        return innerzonew - 2

    def wordwrap(self, textlines):
        """ compute word wraped text """
        # when building the wrapped matrix, build wrappinginfo[wrapedline]=(sourceline, start pos), to be able to convert back
        # have 2 cursors: wrappedcursor (used for display, relative to wraped text), and textcursor (used for edit, relative to original text) - convert from wrappedcursor to textcursor using wrappinginfo (see movewrapedcursor)
        # read pos of wrapped cursor, move wrapped cursor, but edit at text cursor pos
        # during wrap, recalc wrapedcursor pos & refresh wrappinginfo
        wrapedlines = []
        wrappinginfo = []
        linewidth = self.getlinewidth()
        for idx, line in enumerate(textlines):
            if len(line) > linewidth:
                restofline = line
                startofwraped = 0
                while len(restofline) > 0:
                    thisline = restofline[0:linewidth]
                    taken = len(thisline)
                    # update wrapped cursor position
                    if self.textcursor.getline() == idx and self.textcursor.getchar() >= startofwraped and self.textcursor.getchar() < startofwraped + taken:
                        self.wrappedcursor.position = [self.textcursor.getchar() - startofwraped, len(wrapedlines)]
                    restofline = restofline[taken:]
                    wrapedlines.append(thisline)
                    wrappinginfo.append((idx, startofwraped))
                    startofwraped += taken
            else:
                wrapedlines.append(line)
                wrappinginfo.append((idx, 0))
        self.wrappinginfo = wrappinginfo
        self.wrapedlines = wrapedlines
        return wrapedlines

    def blendcursorintext(self, cursor, textlines):
        """ blend cursor in text array """
        cursorx = cursor.getchar()
        cursory = cursor.getline()
        cursorline = textlines[cursory]
        textlineswcursor = []+textlines
        charatcursor = None
        if cursorx < len(cursorline):
            charatcursor = cursorline[cursorx]
        textlineswcursor[cursory] = cursorline[:cursorx] + \
            cursor.cyclecursor(charatcursor) + cursorline[cursorx+1:]
        return textlineswcursor

    def updatecontent(self):
        blended = self.blendcursorintext(self.textcursor, self.textlines)
        if self.wordwrapflag:
            wrapped = self.wordwrap(blended)
            # wrappedandblended = self.blendcursorintext(self.wrappedcursor, wrapped) #blend the wrapped cursor for debug
            # self.content = wrappedandblended
            self.content = wrapped
        else:
            self.wrapedlines = blended
            # If not in wrap mode keep both cursors in sync
            self.wrappedcursor.position = self.textcursor.position
            self.content = blended

    def movewrapedcursor(self, wcursorx, wcursory):
        """ move wraped cursor and update text cursor pos """
        if self.wordwrapflag:
            self.wrappedcursor.placeincontent(wcursorx, wcursory, self.wrapedlines)
            sourceline, startchar = self.wrappinginfo[self.wrappedcursor.getline()]
            self.movetextcursor(startchar+self.wrappedcursor.getchar(), sourceline)
        else:
            # allow wrap text ops to work in non wrap mode - by having wrappedcursor=textcursor
            self.wrappedcursor.placeincontent(wcursorx, wcursory, self.textlines)
            self.movetextcursor(wcursorx, wcursory)

    def movetextcursor(self, cursorx, cursory):
        """ move text cursor """
        self.textcursor.placeincontent(cursorx, cursory, self.textlines)

    def insertlineat(self, cursory, cursorx):
        """ insert line """
        # cut current line at x, add new line with cut content
        linetocut = self.textlines[cursory]
        leftpart = linetocut[0:cursorx]
        rightpart = linetocut[cursorx:]
        self.textlines[cursory] = leftpart
        self.textlines.insert(cursory+1, rightpart)
        # update of wraped cursor will be done during next wraping compute
        self.movetextcursor(0, cursory+1)

    def insertcharat(self, char, y, x):
        """ insert char """
        tmpline = self.textlines[y]
        self.textlines[y] = tmpline[0:x] + char + tmpline[x:]
        # update of wraped cursor will be done during next wraping compute
        self.movetextcursor(x+1, y)

    def rmcharat(self, y, x):
        """ remove char """
        tmpline = self.textlines[y]
        self.textlines[y] = tmpline[0:x-1] + tmpline[x:]
        # update of wraped cursor will be done during next wraping compute
        self.movetextcursor(x-1, y)

    def joinlines(self, y1, y2):
        """ join two lines """
        newcursorx = len(self.textlines[y1])
        self.textlines[y1] = self.textlines[y1]+self.textlines[y2]
        self.textlines.pop(y2)
        # update of wraped cursor will be done during next wraping compute
        self.movetextcursor(newcursorx, y1)

    def handletextkeydown(self, event, keymods):
        """ handle generic key down """
        textcursorx = self.textcursor.getchar()
        textcursory = self.textcursor.getline()
        wrapedcursorx = self.wrappedcursor.getchar()
        wrapedcursory = self.wrappedcursor.getline()
        print(
            f"handlepanelkeydown: textcursory:{textcursory}, textcursorx:{textcursorx}.")
        print(
            f"handlepanelkeydown: wrapedcursory:{wrapedcursory}, wrapedcursorx:{wrapedcursorx}.")
        # MOVES are done on wraped cursor & translated
        if event.key == pygame.K_UP:
            #TODO:up/down doesnt work in wordwrap mode (left goes left+up, right goes right+up)
            self.movewrapedcursor(wrapedcursorx, wrapedcursory-1)
        elif event.key == pygame.K_DOWN:
            self.movewrapedcursor(wrapedcursorx, wrapedcursory+1)
        elif event.key == pygame.K_LEFT:
            if wrapedcursorx > 0:
                self.movewrapedcursor(wrapedcursorx-1, wrapedcursory)
            else:
                self.movewrapedcursor(wrapedcursorx, wrapedcursory-1)
        elif event.key == pygame.K_RIGHT:
            if wrapedcursorx < len(self.wrapedlines[wrapedcursory]):
                self.movewrapedcursor(wrapedcursorx+1, wrapedcursory)
            else:
                self.movewrapedcursor(wrapedcursorx, wrapedcursory+1)
        elif event.key == pygame.K_HOME:
            self.movewrapedcursor(0, 0)
        elif event.key == pygame.K_END:
            self.movewrapedcursor(
                len(self.wrapedlines[len(self.wrapedlines)-1]), len(self.wrapedlines))
        # EDITS are done on text cursor
        elif event.key == pygame.K_BACKSPACE:
            if textcursorx > 0:
                self.rmcharat(textcursory, textcursorx)
            else:
                self.joinlines(textcursory-1, textcursory)
        elif event.key == pygame.K_DELETE:
            if textcursorx < len(self.textlines[textcursory]):
                self.rmcharat(textcursory, textcursorx+1)
            else:
                self.joinlines(textcursory, textcursory+1)
        elif event.key == pygame.K_RETURN:
            self.insertlineat(textcursory, textcursorx)
        elif event.key == pygame.K_TAB:
            # TAB is 2 spaces
            self.insertcharat(" ", textcursory, textcursorx)
            self.insertcharat(" ", textcursory, textcursorx)
        else:  # Unicode standard is used for string formation
            if event.unicode.isprintable():
                self.insertcharat(event.unicode, textcursory, textcursorx)

    def togglewordwrap(self):
        """ toggle wordwrap """ 
        self.wordwrapflag = not self.wordwrapflag
        print(f"wordwrap:{self.wordwrapflag}")

    def handlepanelcontrolkeydown(self, event, keymods):
        """ Handle controls by key """
        if keymods & pygame.KMOD_CTRL:  # CTRL keys
            if event.key == pygame.K_w:  # toggle wordwrap
                self.togglewordwrap()

    def handlepanelkeydown(self, event, keymods):
        self.handlecontrolkeydown(event, keymods)
        self.handlepanelcontrolkeydown(event, keymods)
        self.handletextkeydown(event, keymods)

    def handletextclick(self, event, charx, chary):
        """ handle click in text area """
        if self.zone is not None:
            # calculate char line and col
            displaycursory = chary - self.zone.y - 2  # add -x control lines if needed
            displaycursorx = charx - self.zone.x - 2
            # will handle test if wordwrap on or off
            self.movewrapedcursor(displaycursorx+1, displaycursory+1)

    def handlepanelclick(self, event, charx, chary):
        self.handletextclick(event, charx, chary)
        self.handlecontrolclick(event, charx, chary)
