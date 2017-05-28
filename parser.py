# -*- coding: utf-8 -*-
import re
from constants import *
from grid import Grid

class Parser(object):
    read = ''
    x, y = 1, 1  # there is no 0, 0
    mode = None
    attr = None
    grid = Grid()

    def __init__(self):
        self.mode = 'normal'
        self.attr = defaultATTR.copy()

    def parse(self):
        print(self.read)
        while self.read:
            if self.read[0] in ('','', '\r', '\n'):

                found_match = self.parse_special()
                if found_match:
                    continue

                self.read = self.read[1:]

            else:  # just a letter
                self.grid.set_cell(self.read[0], self.x, self.y, self.mode, self.attr)
                self.x += 1
                self.read = self.read[1:]

        self.grid.set_frame(self.x, self.y)

    def parse_special(self):
        """
        Parses the input and sets the new state of the parser,
        returns True if a match was found.
        https://en.wikipedia.org/wiki/ANSI_escape_code
        """
        actions = (
            ('\r', '_return'),
            ('\n', 'new_line'),
            ('', 'backspace'),
            (r'\[(\d*)(;\d+)?(;\d+)?m', 'set_attributes'),
            (r'\[(\d+);(\d+)[Hf]', 'move_arbitrary_position'),
            (r'\[(\d*)A', 'move_up'),
            (r'\[(\d*)B', 'move_down'),
            (r'\[(\d*)C', 'move_forwards'),
            (r'\[(\d*)D', 'move_left'),
            (r'\[(\d+)d', 'change_line'),
            (r'\[2J', 'clear_screen_and_home_cursor'),
            (r'\[;?H', 'move_to_home'),
            (r'\[(\d+);(\d+);(\d+);(\d+)z', 'erase_rectangular_area'),
            (r'\[K', 'clear_line'),
            (r'\(B', 'set_united_states_g0_characters'),
            (r'\(0', 'set_g0_special_characters'),
            (r'[^a-zA-Z=>]*[a-zA-Z=>]', 'unrecognized_escape_sequence'),
        )

        for regex, action in actions:
            match = re.match(regex, self.read)
            if match:
                self.read = self.read[len(match.group(0)):]
                getattr(self, action)(match)
                return True

        return False

    def _return(self, match):
        self.x = 1

    def new_line(self, match):
        self.y += 1

    def backspace(self, match):
        # go back by one
        self.x = max(1, self.x - 1)

    def move_arbitrary_position(self, match):
        # put the cursor at arbitrary position
        self.x = int(match.group(2))
        self.y = int(match.group(1))

    def move_up(self, match):
        # move up by value, default 1
        self.y -= int(match.group(1) or 1)

    def move_down(self, match):
        # move down by value, default 1
        self.y += int(match.group(1) or 1)

    def move_forwards(self, match):
        # move forwards by value, default 1
        self.x += int(match.group(1) or 1)

    def move_left(self, match):
        # move left by value, default 1
        self.x -= int(match.group(1) or 1)

    def change_line(self, match):
        self.y = int(match.group(1))

    def clear_screen_and_home_cursor(self, match):
        self.grid.clear()
        self.x, self.y = 1, 1

    def move_to_home(self, match):
        self.x, self.y = 1, 1

    def erase_rectangular_area(self, match):
        """erase rectangular area, dunno if this works can't find info on it"""
        a, b, c, d = match.group(0), match.group(1), match.group(2), match.group(3)
        for i in range(a, c + 1):
            for j in range(b, d + 1):
                self.grid.set_cell(' ', i, self.y, self.mode, defaultATTR)

    def clear_line(self, match):
        # Esc[K   Clear line from cursor right    EL0
        # Esc[0K  Clear line from cursor right    EL0
        # Esc[1K  Clear line from cursor left EL1
        # Esc[2K  Clear entire line   EL2
        for i in range(self.x, ttyW):
            self.grid.set_cell(' ', i, self.y, self.mode, defaultATTR)

    def set_united_states_g0_characters(self, match):
        # Set United States G0 character set
        self.mode = 'normal'

    def set_g0_special_characters(self, match):
        # Set G0 special chars. & line set
        self.mode = 'special'

    def unrecognized_escape_sequence(self, match):
        # unrecognized escape sequence
        # print('Unrecognized sequence: ESC' + match.group(0)[1:])
        pass


    def set_attributes(self, match):
        if match.group(1):
            iattr = int(match.group(1))
            self.set_attribute(iattr)
            if match.group(2):
                iattr = match.group(2)[1:]
                self.set_attribute(iattr)
                if match.group(3):
                    iattr = match.group(3)[1:]
                    self.set_attribute(iattr)
        else:
            self.set_attribute(0)


    def set_attribute(self, iattr):
        attr = self.attr
        # tty ansi attr
        # 0  → Normal (default). 
        if iattr == 0:
            attr['weight'] = 'normal'
            attr['fgcolour'] = defaultFG
            attr['bgcolour'] = defaultBG
        # 1  → Bold.
        if iattr == 1: attr['weight'] = 'bold'
        # 2  → Faint, decreased intensity (ISO 6429).
        # 3  → Italicized (ISO 6429).
        # 4  → Underlined.
        # 5  → Blink (appears as Bold).
        # 7  → Inverse.
        # 8  → Invisible, i.e., hidden (VT300).
        # 9  → Crossed-out characters (ISO 6429).
        # 21 → Doubly-underlined (ISO 6429).
        # 22 → Normal (neither bold nor faint).
        # 23 → Not italicized (ISO 6429).
        # 24 → Not underlined.
        # 25 → Steady (not blinking).
        # 27 → Positive (not inverse).
        # 28 → Visible, i.e., not hidden (VT300).
        # 29 → Not crossed-out (ISO 6429).
        # 30 → Set foreground color to Black.
        if iattr == 30: attr['fgcolour'] = BLACK
        # 31 → Set foreground color to Red.
        if iattr == 31: attr['fgcolour'] = RED
        # 32 → Set foreground color to Green.
        if iattr == 32: attr['fgcolour'] = GREEN
        # 33 → Set foreground color to Yellow.
        if iattr == 33: attr['fgcolour'] = YELLOW
        # 34 → Set foreground color to Blue.
        if iattr == 34: attr['fgcolour'] = BLUE
        # 35 → Set foreground color to Magenta.
        if iattr == 35: attr['fgcolour'] = MAGENTA
        # 36 → Set foreground color to Cyan.
        if iattr == 36: attr['fgcolour'] = CYAN
        # 37 → Set foreground color to White.
        if iattr == 37: attr['fgcolour'] = WHITE
        # 39 → Set foreground color to default (original).
        if iattr == 39: attr['fgcolour'] = defaultFG
        # 40 → Set background color to Black.
        if iattr == 40: attr['bgcolour'] = BLACK
        # 41 → Set background color to Red.
        if iattr == 41: attr['bgcolour'] = RED
        # 42 → Set background color to Green.
        if iattr == 42: attr['bgcolour'] = GREEN
        # 43 → Set background color to Yellow.
        if iattr == 42: attr['bgcolour'] = YELLOW
        # 44 → Set background color to Blue.
        if iattr == 44: attr['bgcolour'] = BLUE
        # 45 → Set background color to Magenta.
        if iattr == 45: attr['bgcolour'] = MAGENTA
        # 46 → Set background color to Cyan.
        if iattr == 46: attr['bgcolour'] = CYAN
        # 47 → Set background color to White.
        if iattr == 47: attr['bgcolour'] = WHITE
        # 49 → Set background color to default (original).
        if iattr == 49: attr['bgcolour'] = defaultBG
