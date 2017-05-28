from constants import *
from draw import draw_cell

class Cell(object):
    letter = None
    attr = defaultATTR.copy()
    mode = 'normal'
    _dirty = True
    frame = False

class Grid(object):
    cells = None

    def __init__(self):
        self.cells = [
            [Cell() for x in range(ttyW*2)]
            for y in range(ttyH*2)
        ]

    def set_cell(self, letter, x, y, mode, attr):
        cell = self.cells[y][x]
        cell.letter = letter
        cell.mode = mode
        cell.attr = attr.copy()
        cell._dirty = True

    def set_frame(self, x, y):
        cell = self.cells[y][x]
        cell.frame = True
        cell._dirty = True

    def clear(self):
        from draw import SCREEN
        SCREEN.fill(defaultBG)
        self.__init__()

    def draw(self):
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                if cell._dirty:
                    draw_cell(cell, x, y)
                    cell._dirty = False
                    cell.frame = False
