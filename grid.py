import re
from constants import *
from draw import draw_cell

class Cell(object):
    letter = None
    attr = defaultATTR.copy()
    mode = 'normal'
    frame = False
    draw = True
    neighbours = None
    _dirty = True

    def is_on_the_board(self, neighbours):
        neighbour_letters = set(n.letter for n in neighbours.values() if n.letter)
        board_letters = set(('#', '.', '~'))
        intersection = neighbour_letters & board_letters
        return bool(intersection)

    def pp_save_neighbours(self, neighbours):
        self.neighbours = neighbours

    def pp_top_left_corner(self, neighbours):
        top_left_corner = (
           self.letter == '-'
           and self.attr['fgcolour'] == defaultFG
           and neighbours['up'].letter != '|'
           and neighbours['left'].letter != '-'
           and neighbours['down'].letter == '|'
        )
        if top_left_corner:
            self.mode = 'special'
            self.letter = 'l'

    def pp_top_right_corner(self, neighbours):
        top_left_corner = (
           self.letter == '-'
           and self.attr['fgcolour'] == defaultFG
           and neighbours['up'].letter != '|'
           and neighbours['right'].letter != '-'
           and neighbours['down'].letter == '|'
        )
        if top_left_corner:
            self.mode = 'special'
            self.letter = 'k'

    def pp_bottom_right_corner(self, neighbours):
        top_left_corner = (
           self.letter == '-'
           and self.attr['fgcolour'] == defaultFG
           and neighbours['up'].letter == '|'
           and neighbours['right'].letter != '-'
           and neighbours['down'].letter != '|'
        )
        if top_left_corner:
            self.mode = 'special'
            self.letter = 'j'

    def pp_bottom_left_corner(self, neighbours):
        top_left_corner = (
           self.letter == '-'
           and self.attr['fgcolour'] == defaultFG
           and neighbours['up'].letter == '|'
           and neighbours['left'].letter != '-'
           and neighbours['down'].letter != '|'
        )
        if top_left_corner:
            self.mode = 'special'
            self.letter = 'm'


class FakeCell(object):
    """Used to represent cells that are out of bounds"""
    def __getattr__(self, attr):
        return None

class Grid(object):
    _cells = None
    after_x = None
    after_y = None

    def __init__(self):
        self._cells = [
            [Cell() for x in range(ttyW*2)]
            for y in range(ttyH*2)
        ]

    def set_cell(self, letter, x, y, mode, attr):
        cell = self._cells[y][x]
        cell.letter = letter
        cell.mode = mode
        cell.attr = attr.copy()
        cell.draw = True
        cell._dirty = True

    def set_frame(self, x, y):
        cell = self._cells[y][x]
        cell.frame = True
        cell._dirty = True

    @property
    def cells(self):
        for y, row in enumerate(self._cells):
            for x, cell in enumerate(row):
                yield (cell, x, y)

    def clear(self):
        # for performance we just empty the screen and say nothing is dirty
        from draw import SCREEN
        SCREEN.fill(defaultBG)
        self.__init__()
        for cell, _, _ in self.cells:
            cell._dirty = False

    def get_neighbours(self, x, y):
        coords = (
            ('up', x, y - 1),
            ('right', x + 1, y),
            ('down', x, y + 1),
            ('left', x - 1, y),
        )

        neighbours = {
            'up': FakeCell(),
            'right': FakeCell(),
            'down': FakeCell(),
            'left': FakeCell(),
        }

        for direction, nx, ny in coords:
            try:
                neighbours[direction] = self._cells[ny][nx]
            except IndexError:
                pass

        return neighbours

    def post_process(self):
        # Post process individual cells
        for cell, x, y in self.cells:
            if not cell._dirty:
                continue
            neighbours = self.get_neighbours(x, y)
            post_process_functions = (
                f for f in dir(cell)
                if f.startswith('pp_')
            )
            for f in post_process_functions:
                getattr(cell, f)(neighbours)

        # Search for boxes of text to not draw tiles inside
        for y, row in enumerate(self._cells):
            line = ''.join(cell.letter if cell.letter else ' ' for cell in row)
            match = re.search(end_sequence_re, line)
            if match:
                start = match.start() - 2
                self.after_x = start
                self.after_y = y
                for cell, cx, cy in self.cells:
                    if cy <= y and cx >= start:
                        cell.draw = False

    def draw(self):
        for cell, x, y in self.cells:
            if cell._dirty:
                draw_cell(cell, x, y)
                cell._dirty = False
                if cell.frame:
                    cell.frame = False
                    cell._dirty = True

    def after_draw(self):
        # Draw a border around text boxes
        import pygame
        from draw import SCREEN
        if self.after_y and self.after_y > 1:
            x = (self.after_x + 1) * W
            y = (self.after_y - 1) * H
            max_x = max((x for cell, x, y in self.cells if cell.letter and cell.letter != ' '))
            max_x = (max_x) * W
            pygame.draw.rect(SCREEN, defaultFG, (x, 0, max_x-x, y+H), 1)
        self.after_x = None
        self.after_y = None
