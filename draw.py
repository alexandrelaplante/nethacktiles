import pygame
from collections import defaultdict

import tileset
from constants import *
from symbols import symbols    


pygame.init()

tileset_image = pygame.image.load(TILESET)
SCREEN = pygame.display.set_mode((viewportWidth, viewportHeight), 0, 32)
font = pygame.font.Font(FONT, H-4)
fontb = pygame.font.SysFont(FONTB, H+7)

SCREEN.fill(defaultBG)
pygame.display.update()


letter_to_symbol = defaultdict(list)

for symbol in symbols:
    letter_to_symbol[symbol.letter].append(symbol)


def get_symbol_from_cell(cell):
    def we_have_a_match(cell, symbol):
        return (
            cell.letter == symbol.letter
            and cell.mode == symbol.mode
            and (cell.attr['fgcolour'] == symbol.fgcolour or symbol.fgcolour == '*')
            and (cell.attr['bgcolour'] == symbol.bgcolour or symbol.bgcolour == '*')
            and (cell.attr['weight'] == symbol.weight or symbol.weight == '*')
        )
    
    if cell.letter in letter_to_symbol:
        possible_symbols = letter_to_symbol[cell.letter]
        for symbol in possible_symbols:
            if we_have_a_match(cell, symbol):
                sheetX, sheetY = tileset.get_tile(
                    symbol.tile,
                    symbol.offset
                )
                return sheetX, sheetY

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

    sheetX, sheetY = 0, 0

    symbol = get_symbol_from_cell(cell)
    if symbol:
        sheetX, sheetY = symbol

    # This is the area of the board where tiles are possible.
    draw = cell.draw and 1 < grid_y < 23

    # if we found a tile, draw it
    if draw and symbol:
        SCREEN.blit(
            source=tileset_image,
            dest=(x, y, W, H),
            area=(sheetX*tileW, sheetY*tileH, tileW, tileH),
        )
    else:
        pygame.draw.rect(SCREEN, bgcolour, (x, y, W, H), 0)  # background
        if l != ' ':
            # if mode == 'special':
            #     print('missing a special character: ', l)
            #     pygame.draw.rect(SCREEN, RED, (x, y, W, H), 2)
            if draw:  # show background behind letters
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
