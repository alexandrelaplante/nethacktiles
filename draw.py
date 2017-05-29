import pygame
from constants import *
import tileset


pygame.init()

tileset_image = pygame.image.load(TILESET)
SCREEN = pygame.display.set_mode((viewportWidth, viewportHeight), 0, 32)
font = pygame.font.Font(FONT, H-4)
fontb = pygame.font.SysFont(FONTB, H+7)

SCREEN.fill(defaultBG)
pygame.display.update()

def draw_cell(cell, grid_x, grid_y):
    l = cell.letter
    mode = cell.mode
    attr = cell.attr
    frame = cell.frame

    # there's no 0 coordinate in the ansi codes
    x = (grid_x - 1) * W
    y = (grid_y - 1) * H

    fgcolour = attr['fgcolour']
    bgcolour = attr['bgcolour']

    pygame.draw.rect(SCREEN, bgcolour, (x, y, W, H), 0)  # background
    sheetX, sheetY = 0, 0

    # IBM or DEC graphics
    if mode == 'special':

        letter_to_sheet_coordinates = {
            # '0': (23, 20),
            'x': tileset.get_tile('wall', 0),  # vertical
            'q': tileset.get_tile('wall', 1),  # horizontal
            'l': tileset.get_tile('wall', 2),  # top left corner
            'k': tileset.get_tile('wall', 3),  # top right corner
            'm': tileset.get_tile('wall', 4),  # bottom left corner
            'j': tileset.get_tile('wall', 5),  # bottom right corner
            'n': tileset.get_tile('wall', 6),  # total junction
            'v': tileset.get_tile('wall', 7),  # down junction
            'w': tileset.get_tile('wall', 8),  # up junction
            'u': tileset.get_tile('wall', 9),  # right junction
            't': tileset.get_tile('wall', 10),  # left junction
            '~': tileset.get_tile('floor of a room'),  # floor
            'a': tileset.get_tile('open door'),
        }

        if l in letter_to_sheet_coordinates:
            sheetX, sheetY = letter_to_sheet_coordinates[l]

    # ASCII
    if mode == 'normal':
        if l == '+' and fgcolour == YELLOW:
            sheetX, sheetY = tileset.get_tile('closed door')
        elif l == '#' and attr['weight'] == 'bold':
            sheetX, sheetY = tileset.get_tile('lit corridor')
        elif l == '#' and attr['weight'] == 'normal':
            sheetX, sheetY = tileset.get_tile('corridor')
        elif l == '<': # and fgcolour == YELLOW:
            sheetX, sheetY = tileset.get_tile('staircase up')
        elif l == '>': # and fgcolour == YELLOW:
            sheetX, sheetY = tileset.get_tile('staircase down')
        elif l == '{' and fgcolour == BLUE:
            sheetX, sheetY = tileset.get_tile('fountain')
        elif l == '}' and fgcolour == BLUE:
            sheetX, sheetY = tileset.get_tile('water')
        elif l == '}' and fgcolour == RED:
            sheetX, sheetY = tileset.get_tile('molten lava')
        elif l == '.' and attr['weight'] == 'bold':
            sheetX, sheetY = tileset.get_tile('dark part of a room', 1)
        elif l == '.' and attr['weight'] == 'normal':
            sheetX, sheetY = tileset.get_tile('floor of a room')
        # can't tell if it's a wall or a dash.
        elif l == '-' and fgcolour == defaultFG:
            sheetX, sheetY = tileset.get_tile('wall', 1)
        elif l == '|' and fgcolour == defaultFG:
            sheetX, sheetY = tileset.get_tile('wall')
        elif l == '$' and fgcolour == YELLOW:
            sheetX, sheetY = tileset.get_tile('gold piece')
        elif l == '?' and fgcolour == defaultFG:
            sheetX, sheetY = tileset.get_tile('READ ME')  # scroll
        # can't tell if they're bolders or numbers
        elif l == '0':
            sheetX, sheetY = tileset.get_tile('boulder')
        elif l == '-' and fgcolour == YELLOW:
            sheetX, sheetY = tileset.get_tile('open door')
        elif l == '|' and fgcolour == YELLOW:
            sheetX, sheetY = tileset.get_tile('open door', 1)
        elif l == 'l' and fgcolour == GREEN:
            sheetX, sheetY = tileset.get_tile('leprechaun')
        elif l == 'i' and fgcolour == GREEN:
            sheetX, sheetY = tileset.get_tile('homunculus')
        elif l == 'h' and fgcolour == GREEN:
            sheetX, sheetY = tileset.get_tile('hobbit')
        elif l == 'h' and fgcolour == RED:
            sheetX, sheetY = tileset.get_tile('fox')
        elif l == 'G' and fgcolour == YELLOW:
            sheetX, sheetY = tileset.get_tile('gnome')
        elif l == 'N' and fgcolour == GREEN:
            sheetX, sheetY = tileset.get_tile('guardian naga')
        elif l == 'D' and fgcolour == RED:
            sheetX, sheetY = tileset.get_tile('red dragon')
        elif l == 'D' and fgcolour == BLACK:
            sheetX, sheetY = tileset.get_tile('black dragon')
        elif l == 'G' and fgcolour == BLUE:
            sheetX, sheetY = tileset.get_tile('gnome lord')
        elif l == 'e' and fgcolour == BLUE:
            sheetX, sheetY = tileset.get_tile('floating eye')
        elif l == 'x' and fgcolour == MAGENTA:
            sheetX, sheetY = tileset.get_tile('grid bug')
        elif l == 'Y' and fgcolour == YELLOW:
            sheetX, sheetY = tileset.get_tile('ape')
        elif l == 'N' and fgcolour == YELLOW:
            sheetX, sheetY = tileset.get_tile('golden naga')
        elif l == 'u' and fgcolour == YELLOW:
            sheetX, sheetY = tileset.get_tile('pony')
        elif l == ':' and fgcolour == YELLOW:
            sheetX, sheetY = tileset.get_tile('newt')
        elif l == 'd' and attr['weight'] == 'bold':
            sheetX, sheetY = tileset.get_tile('dog')
        elif l == 'f' and attr['weight'] == 'bold':
            sheetX, sheetY = tileset.get_tile('housecat')
        elif l == '_':
            sheetX, sheetY = tileset.get_tile('altar')
        elif l == '%':
            sheetX, sheetY = tileset.get_tile('corpse')
        elif l == '@' and attr['weight'] == 'bold':  # our dude
            sheetX, sheetY = tileset.get_tile('archeologist')

    draw = False
    if 1 < grid_y < 23:
        # just text on the first line
        # just text on the last two lines
        draw = True

    draw = cell.draw and draw

    # if we found a tile, draw it
    if draw and not(sheetX == 0 and sheetY == 0):
        SCREEN.blit(
            source=tileset_image,
            dest=(x, y, W, H),
            area=(sheetX*tileW, sheetY*tileH, tileW, tileH),
        )
    else:
        # if mode == 'special' and l != ' ':
        #     print('missing a special character: ', l)
        #     pygame.draw.rect(SCREEN, RED, (x, y, W, H), 2)
        if draw and l != ' ' and False:  # show background behind letters
            sheetX, sheetY = tileset.get_tile('empty')
            SCREEN.blit(
                source=tileset_image,
                dest=(x, y, W, H),
                area=(sheetX*tileW, sheetY*tileH, tileW, tileH),
            )
        current_font = fontb if attr['weight'] == 'bold' else font
        SCREEN.blit(
            source=current_font.render(l, True, fgcolour),
            dest=(x, y, W, H),
            # special_flags=pygame.BLEND_ADD,
        )

    if frame:
        pygame.draw.rect(SCREEN, defaultFG, (x, y, W, H), 1)

    # if attr['weight'] == 'bold':
    #    pygame.draw.rect(SCREEN, (255,255,255), (x, y, W, H), 2)
