from constants import *
import pygame

pygame.init()

tileset = pygame.image.load(TILESET)
SCREEN = pygame.display.set_mode((viewportWidth, viewportHeight), 0, 32)
font = pygame.font.Font(FONT, H-3)
fontb = pygame.font.SysFont(FONTB, H-3)

SCREEN.fill(defaultBG)
pygame.display.update()

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
        elif l == '}' and fgcolour == RED:  # lava
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
            source=tileset,
            dest=(x, y, W, H),
            area=(sheetX*tileW, sheetY*tileH, tileW, tileH),
        )
    else:
        # if mode == 'special' and l != ' ':
        #     print('missing a special character: ', l)
        #     pygame.draw.rect(SCREEN, RED, (x, y, W, H), 2)
        current_font = fontb if attr['weight'] == 'bold' else font
        SCREEN.blit(current_font.render(l, True, fgcolour), (x, y))
    # if attr['weight'] == 'bold':
    #    pygame.draw.rect(SCREEN, (255,255,255), (x, y, W, H), 2)
