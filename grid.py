from constants import *
from draw import draw_cell

class Cell(object):
    letter = None
    attr = defaultATTR.copy()
    mode = 'normal'
    frame = False
    draw = True
    _dirty = True

    def pp_not_a_boulder(self, neighbours):
        if self.letter == '0':
            neighbour_letters = set(n.letter for n in neighbours.values() if n.letter)
            board_letters = set(('#', '.', '-', '|'))
            intersection = neighbour_letters & board_letters
            not_near_the_board = not(intersection)

            if not_near_the_board:
                self.draw = False

    def pp_not_a_wall(self, neighbours):
        not_a_wall = (
            self.letter == '-'
            and self.attr['fgcolour'] == defaultFG
            and neighbours['left'].letter == ' '
            and neighbours['right'].letter == ' '
        )
        if not_a_wall:
            self.draw = False

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
        cell._dirty = True

    def set_frame(self, x, y):
        cell = self._cells[y][x]
        cell.frame = True
        cell._dirty = True

    def clear(self):
        self.__init__()

    @property
    def cells(self):
        for y, row in enumerate(self._cells):
            for x, cell in enumerate(row):
                yield (cell, x, y)

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


    def draw(self):
        for cell, x, y in self.cells:
            if cell._dirty:
                draw_cell(cell, x, y)
                cell.frame = False
                cell._dirty = False
