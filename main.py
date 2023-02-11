#kyrlian, 2023

import sys
import pygame

from context import Context
from zone import Zone
from panel import Panel
from panelmp3player import PanelMp3Player
from panelclock import PanelClock
from paneltextinput import PanelTextInput

# single line borders - https://en.wikipedia.org/wiki/Box_Drawing
# 	        0 	1 	2 	3 	4 	5 	6 	7 	8 	9 	A 	B 	C 	D 	E 	F
# U+250x 	─ 	━ 	│ 	┃ 	┄ 	┅ 	┆ 	┇ 	┈ 	┉ 	┊ 	┋ 	┌ 	┍ 	┎ 	┏
# U+251x 	┐ 	┑ 	┒ 	┓ 	└ 	┕ 	┖ 	┗ 	┘ 	┙ 	┚ 	┛ 	├ 	┝ 	┞ 	┟
# U+252x 	┠ 	┡ 	┢ 	┣ 	┤ 	┥ 	┦ 	┧ 	┨ 	┩ 	┪ 	┫ 	┬ 	┭ 	┮ 	┯
# U+253x 	┰ 	┱ 	┲ 	┳ 	┴ 	┵ 	┶ 	┷ 	┸ 	┹ 	┺ 	┻ 	┼ 	┽ 	┾ 	┿
# U+254x 	╀ 	╁ 	╂ 	╃ 	╄ 	╅ 	╆ 	╇ 	╈ 	╉ 	╊ 	╋ 	╌ 	╍ 	╎ 	╏
# U+255x 	═ 	║ 	╒ 	╓ 	╔ 	╕ 	╖ 	╗ 	╘ 	╙ 	╚ 	╛ 	╜ 	╝ 	╞ 	╟
# U+256x 	╠ 	╡ 	╢ 	╣ 	╤ 	╥ 	╦ 	╧ 	╨ 	╩ 	╪ 	╫ 	╬ 	╭ 	╮ 	╯
# U+257x 	╰ 	╱ 	╲ 	╳ 	╴ 	╵ 	╶ 	╷ 	╸ 	╹ 	╺ 	╻ 	╼ 	╽ 	╾ 	╿
# blocks - https://en.wikipedia.org/wiki/Block_Elements
# 	█ 	Full block
# 	░ 	Light shade
# 	▒ 	Medium shade
# 	▓ 	Dark shade
# 	▙ 	Quadrant upper left and lower left and lower right
# 	▛ 	Quadrant upper left and upper right and lower left
# 	▜ 	Quadrant upper left and upper right and lower right
# 	▟ 	Quadrant upper right and lower left and lower right
# 	▀ 	Upper half block
# 	▄ 	Lower half block
# 	▌ 	Left half block
# 	▐ 	Right half block

def initrootzone(screenw, screenh):
    rootzone = Zone(0, 0, screenw-1, screenh-1, None, PanelClock("Clock"))
    zl, zr = rootzone.split("v", .4, PanelTextInput("Text editor",["Lorem","ipsum"]))
    zl.split("h", .2,PanelMp3Player("MP3 Player",r"D:\music\#Divers"))
    return rootzone

def pickfont():
    available = pygame.font.get_fonts()
    print("Available fonts : "+str(available))
    candidates = ["lucidaconsole","ibmplexmono"]
    for f in candidates:
        if f in available:
            print("Selected candidate font : "+f)
            return pygame.font.SysFont(f, 15)
    for f in available:
        if "mono" in f:
            print("Selected mono font : "+f)
            return pygame.font.SysFont(f, 15)

def main():
    displayinfo = pygame.display.Info()
    screen = pygame.display.set_mode(
        (displayinfo.current_w, displayinfo.current_h), pygame.FULLSCREEN)
    font = pickfont()
    lineheigth = font.get_linesize()
    charwidth, charheigth = font.size(" ")
    maxlines = int(screen.get_height()/lineheigth)
    linewidth = int(screen.get_width()/charwidth)
    rootzone = initrootzone(linewidth, maxlines)
    context = Context(rootzone.getnextpanel())
    bgcolor = (30, 30, 30)
    clock = pygame.time.Clock()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                else:
                    #TODO handle "key held down" for repeat (ex in text editor)
                    rootzone.handlezonekeydown(context,  event, pygame.key.get_mods())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 1 - left click, 2 - middle click, 3 - right click, 4 - scroll up, 5 - scroll down
                # if event.button == 1:  # left click
                    clickx, clicky = pygame.mouse.get_pos()
                    charx = int(clickx / charwidth)
                    chary = int(clicky / lineheigth)
                    print(f"Cliked {charx},{chary}")
                    rootzone.handlezoneclick(context,  event, charx, chary)
        screen.fill(bgcolor)
        rootzone.update()
        rootzone.draw(context,screen, font)
        pygame.display.flip()
        clock.tick(30)# cap to 30 fps


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
    sys.exit()
