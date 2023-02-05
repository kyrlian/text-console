import sys
import pygame

from zone import Zone
from panel import Panel

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

class Context:
    def __init__(self):
        self.focusedpanel = None

def initcontext():
    return Context()

def initrootzone(screenw, screenh):
    rootzone = Zone(0, 0, screenw-1, screenh-1)
    childs = rootzone.split("v", .4)
    childs[0].attachpanel(Panel("Left", ["Big", "Square"]))
    childs[0].attachpanel(Panel("Right", ["with", "several", "text lines"]))
    return rootzone

def main():
    displayinfo = pygame.display.Info()
    screen = pygame.display.set_mode(
        (displayinfo.current_w, displayinfo.current_h), pygame.FULLSCREEN)
    # print(pygame.font.get_fonts())
    font = pygame.font.SysFont('lucidaconsole', 15)
    lineheigth = font.get_linesize()
    charwidth, charheigth = font.size(" ")
    maxlines = int(screen.get_height()/lineheigth)
    linewidth = int(screen.get_width()/charwidth)
    rootzone = initrootzone(linewidth, maxlines)
    context = initcontext()
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
                    rootzone.handlezonekeydown(context,  event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 1 - left click, 2 - middle click, 3 - right click, 4 - scroll up, 5 - scroll down
                if event.button == 1:  # left click
                    clickx, clicky = pygame.mouse.get_pos()
                    charx = int(clickx / charwidth)
                    chary = int(clicky / lineheigth)
                    print(str(charx) + " "+str(chary))
                    rootzone.handlezoneclick(context,  event.button, charx, chary)
        screen.fill(bgcolor)
        rootzone.draw(context,screen, font)
        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
    sys.exit()
