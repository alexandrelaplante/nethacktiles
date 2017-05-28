from constants import *
from draw import draw_char

class Cell(object):
    attr = None
    mode = None

class Grid(object):
    grid = None

    def __init__(self):
        self.grid = [[Cell() for x in range(ttyW)] for y in range(ttyH)]

    def set_cell(self, letter, x, y, mode, attr):
        draw_char(letter, x, y, mode, attr)

    def clear(self):
        from draw import SCREEN
        SCREEN.fill(defaultBG)