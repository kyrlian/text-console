import pygame
from renderer import Renderer

# https://docs.python.org/3/library/curses.html

class RendererPyGame(Renderer):

    def __init__(self):
        self.linewidth=0
        self.maxlines=0
        self.charwidth=0
        self.lineheigth=0
        pygame.init()
        displayinfo = pygame.display.Info()
        self.screen = pygame.display.set_mode((displayinfo.current_w, displayinfo.current_h), pygame.FULLSCREEN)
        self.font = self.pickfont()
        assert self.font is not None
        self.lineheigth = self.font.get_linesize()
        self.charwidth, charheigth = self.font.size(" ")
        self.maxlines = int(self.screen.get_height()/self.lineheigth)
        self.linewidth = int(self.screen.get_width()/self.charwidth)
        self.bgcolor = (30, 30, 30)
        self.screen.fill(self.bgcolor)
        self.clock = pygame.time.Clock()

    def pickfont(self):
        """ pick a mono font """
        availables = pygame.font.get_fonts()
        print("Available fonts : "+str(availables))
        candidates = ["lucidaconsole","ibmplexmono"]
        for candidate in candidates:
            if candidate in availables:
                print("Selected candidate font : "+candidate)
                return pygame.font.SysFont(candidate, 15)
        for available in availables:
            if "mono" in available:
                print("Selected mono font : "+available)
                return pygame.font.SysFont(available, 15)
        return None

    def renderline(self,line,color,x,y):
        assert self.font is not None
        self.screen.blit(self.font.render(line, True, color), (x, y*self.lineheigth))

    def refresh(self):
        pygame.display.flip()
        self.clock.tick(30)# cap to 30 fps
        self.screen.fill(self.bgcolor)

    def quit(self):
        pygame.quit()