# -*- coding: utf-8 -*-
import telnetlib
import pygame
import re

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
MAGENTA = (255,0,255)
CYAN = (0,255,255)
WHITE = (255,255,255)

pygame.init()


myimage = pygame.image.load('geoduck20x12.bmp')
tileH, tileW = 20, 12  # tile size in sheet
W, H = tileW, tileH  # tile size

HOST = 'nethack.alt.org'

viewportWidth, viewportHeight = (1000, 1000)

SCREEN = pygame.display.set_mode((viewportWidth,viewportHeight), 0, 32)
FONT = pygame.font.Font('fonts/DejaVuSansMono.ttf', H-3)
FONTB = pygame.font.SysFont('fonts/DejaVuSansMono-Bold.ttf', H-3)

defaultBG = BLACK
defaultFG = WHITE

SCREEN.fill(defaultBG)
pygame.display.update()

connection = telnetlib.Telnet(HOST)

ttyW, ttyH = 120, 40

import os
os.popen('stty cols {}'.format(ttyW))
rows, columns = os.popen('stty size', 'r').read().split()
print(rows, columns)


def draw_char(l, x, y, mode, attr):
    # there's no 0 coordinate in the ansi codes
    x = (x - 1) * W
    y = (y - 1) * H

    if attr['weight'] == 'frame':
        pygame.draw.rect(SCREEN, defaultFG, (x, y, W, H), 1)
        return

    fgcolour = attr['fgcolour']
    bgcolour = attr['bgcolour']

    pygame.draw.rect(SCREEN, bgcolour, (x, y, W, H), 0)  # background
    sheetX, sheetY = 0, 0

    # IBM or DEC graphics
    if mode == 'special':

        letter_to_sheet_coordinates = {
            '0': (23, 20),
            'x': (30, 20),
            'q': (31, 20),  # horizontal
            'l': (32, 20),
            'k': (33, 20),
            'm': (34, 20),
            'j': (35, 20),  # bottom right corner
            'n': (36, 20),  # bottom right corner
            'v': (37, 20),  # junction left up right
            'w': (38, 20),  # junction left down right
            'u': (39, 20),  # junction left down up
            't': (0, 21),  # junction down up right
            '~': (10, 21),  # floor
            'a': (2, 21),
        }

        if l in letter_to_sheet_coordinates:
            sheetX, sheetY = letter_to_sheet_coordinates[l]

    # ASCII
    if mode == 'normal':
        if l == '+' and fgcolour == YELLOW:  # door (yellow)
            sheetX, sheetY = 4, 21
        elif l == '#':
            sheetX, sheetY = 9, 21
        elif l == '<': # and fgcolour == YELLOW:
            sheetX, sheetY = 11, 21
        elif l == '>': # and fgcolour == YELLOW:
            sheetX, sheetY = 12, 21
        elif l == '{' and fgcolour == BLUE:  # fountain
            sheetX, sheetY = 19, 21
        elif l == '}' and fgcolour == BLUE:  # water
            sheetX, sheetY = 20, 21
        elif l == '}' and fgcolour == BLUE:  # lava
            sheetX, sheetY = 22, 21
        elif l == '.' and fgcolour == defaultFG:
            sheetX, sheetY = 10, 21
        # can't tell if it's a wall or a dash.
        elif l == '-' and fgcolour == defaultFG:  # a wall
            sheetX, sheetY = 31, 20
        elif l == '|' and fgcolour == defaultFG:  # a wall
            sheetX, sheetY = 30, 20
        elif l == '$' and fgcolour == YELLOW:  # a money (yellow)
            sheetX, sheetY = 26, 19
        elif l == '?' and fgcolour == defaultFG:  # a money (yellow)
            sheetX, sheetY = 26, 17
        # can't tell if they're bolders or numbers
        # elif l == '0':
        #     sheetX, sheetY = 23, 20
        elif l == '-' and fgcolour == YELLOW:  # a door
            sheetX, sheetY = 2, 21
        elif l == '|' and fgcolour == YELLOW:  # a door
            sheetX, sheetY = 3, 21
        elif l == '@' and attr['weight'] == 'bold':  # our dude
            sheetX, sheetY = 15, 8

    draw = True
    if y == 0:
        draw = False  # just text on the first line

    # if we found a tile, draw it
    if draw and not(sheetX == 0 and sheetY == 0):
        SCREEN.blit(
            source=myimage,
            dest=(x, y, W, H),
            area=(sheetX*tileW, sheetY*tileH, tileW, tileH),
        )
    else:
        # if mode == 'special' and l != ' ':
        #     print('missing a special character: ', l)
        #     pygame.draw.rect(SCREEN, RED, (x, y, W, H), 2)
        font = FONT if attr['weight'] == 'bold' else FONT
        SCREEN.blit(font.render(l, True, fgcolour), (x, y))
    # if attr['weight'] == 'bold':
    #    pygame.draw.rect(SCREEN, (255,255,255), (x, y, W, H), 2)
        

defaultATTR = {
    'weight': 'normal',
    'underlined': False,
    'blinking': False,
    'fgcolour': defaultFG,
    'bgcolour': defaultBG,
}

class Parser(object):
    read = ''
    x, y = 1, 1  # there is no 0, 0
    mode = None
    attr = None

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
                draw_char(self.read[0], self.x, self.y, self.mode, self.attr)
                self.x += 1
                self.read = self.read[1:]

        draw_char(' ', self.x, self.y, self.mode, {'weight': 'frame'})
        pygame.display.update()

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
                getattr(parser, action)(match)
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
        SCREEN.fill(defaultBG)
        self.x, self.y = 1, 1

    def move_to_home(self, match):
        self.x, self.y = 1, 1

    def erase_rectangular_area(self, match):
        """erase rectangular area, dunno if this works can't find info on it"""
        a, b, c, d = match.group(0), match.group(1), match.group(2), match.group(3)
        for i in range(a, c + 1):
            for j in range(b, d + 1):
                draw_char(' ', i, self.y, self.mode, defaultATTR)

    def clear_line(self, match):
        # Esc[K   Clear line from cursor right    EL0
        # Esc[0K  Clear line from cursor right    EL0
        # Esc[1K  Clear line from cursor left EL1
        # Esc[2K  Clear entire line   EL2
        for i in range(self.x, ttyW):
            draw_char(' ', i, self.y, self.mode, defaultATTR)

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

parser = Parser()

while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        quit()

    elif event.type == pygame.KEYDOWN:
        # if event.key == pygame.K_ESCAPE: quit()
        connection.write(str(event.unicode))

    parser.read = connection.read_until('LOLZ', timeout=0.1)
    
    if parser.read:
        parser.parse()
