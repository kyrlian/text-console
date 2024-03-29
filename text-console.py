#!python3
""" main """
#kyrlian, 2023

import sys
import pygame

from rendererpygame import RendererPyGame
from context import Context
from zone import Zone
from panelmp3player import PanelMp3Player
from panelclock import PanelClock
from paneltextinput import PanelTextInput
from eventconverter import EventConverter
import eventconverter 

def initrootzone(screenw, screenh):
    """ init root zone """
    rootzone = Zone(0, 0, screenw-1, screenh-1, None, PanelClock("Clock")) #create root zone with a clock
    zleft, zText = rootzone.split("v", .4, PanelTextInput("Text editor",["Lorem","ipsum"]))# split verticaly, clock will be reatached to left, add a text editor on right
    # zleft.split("h", .2,PanelMp3Player("MP3 Player",r"D:\music"))# split left zone horizontally, clock will be reatatched to top, add an mp3 player on bottom
    zClock, zMp3 = zleft.split("h", .2,PanelMp3Player("MP3 Player",r"D:\music"))# split left zone horizontally, clock will be reatatched to top, add an mp3 player on bottom
    # zPlayer, zBrowser = zMp3.split("h", .2,PanelDirectoryBrowser("MP3 Browser",[r"D:\music\#Divers",".mp3"])) #split mp3 player zone horizontally, player will stay on top, add a file browser below
    # zPlayer.panel.linkpanel(zBrowser.panel) # register the file browser with the mp3 player
    # zBrowser.panel.registerfileclickaction(zPlayer.panel.play) # register the player play() method on browser click
    return rootzone

def main():
    """ main """
    mode = "pygame"
    renderer = RendererPyGame()
    converter = EventConverter(mode,renderer.charwidth, renderer.lineheigth)
    rootzone = initrootzone(renderer.linewidth, renderer.maxlines)
    context = Context(rootzone.getnextpanel())
    done = False
    while not done:
        #    event = screen.getch() # curses
        for event in pygame.event.get():
            commonevent = converter.convert(event)
            assert commonevent is not None
            if commonevent.type == eventconverter.TYPE_QUIT:
                done = True
            elif commonevent.type == eventconverter.TYPE_KEYDOWN:
                if commonevent.key == eventconverter.KEY_ESCAPE:
                    done = True
                else:
                    #TODO handle "key held down" for repeat (ex in text editor)
                    rootzone.handlezonekeydown(context, commonevent)
            elif commonevent.type == eventconverter.TYPE_MOUSEBUTTONDOWN:
                # 1 - left click, 2 - middle click, 3 - right click, 4 - scroll up, 5 - scroll down
                charx = commonevent.mousex
                chary = commonevent.mousey
                print(f"Cliked {charx},{chary}")
                rootzone.handlezoneclick(context,  event, charx, chary)
        rootzone.update()
        rootzone.draw(context,renderer)
        renderer.refresh()
    renderer.quit()

if __name__ == '__main__':
    main()
    sys.exit()
