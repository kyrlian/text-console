import pygame
import curses

module = "pygame"

if module == "pygame":
    K_UP = pygame.K_UP
    K_DOWN = pygame.K_DOWN
    K_b = pygame.K_b
    K_c = pygame.K_c
    K_h = pygame.K_h
    K_m = pygame.K_m
    K_s = pygame.K_s
    K_t = pygame.K_t
    K_v = pygame.K_v
    K_w = pygame.K_w
    K_x = pygame.K_x
    K_SPACE = pygame.K_SPACE
    K_RIGHT = pygame.K_RIGHT
    K_LEFT = pygame.K_LEFT
    K_UP = pygame.K_UP
    K_DOWN = pygame.K_DOWN
    K_HOME = pygame.K_HOME
    K_END = pygame.K_END
    K_BACKSPACE = pygame.K_BACKSPACE
    K_DELETE = pygame.K_DELETE
    K_RETURN = pygame.K_RETURN
    QUIT = pygame.QUIT
    K_ESCAPE = pygame.K_ESCAPE
    MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN
else:
    K_UP = curses.KEY_UP
    K_DOWN = curses.KEY_DOWN
    K_b = curses.KEY_b
    K_c = curses.KEY_c
    K_h = curses.KEY_h
    K_m = curses.KEY_m
    K_s = curses.KEY_s
    K_t = curses.KEY_t
    K_v = curses.KEY_v
    K_w = curses.KEY_w
    K_x = curses.KEY_x
    K_SPACE = curses.KEY_SPACE
    K_RIGHT = curses.KEY_RIGHT
    K_LEFT = curses.KEY_LEFT
    K_UP = curses.KEY_UP
    K_DOWN = curses.KEY_DOWN
    K_HOME = curses.KEY_HOME
    K_END = curses.KEY_END
    K_BACKSPACE = curses.KEY_BACKSPACE
    K_DELETE = curses.KEY_DELETE
    K_RETURN = curses.KEY_RETURN
