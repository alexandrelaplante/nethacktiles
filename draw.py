import pygame
from collections import defaultdict

import tileset
from constants import *
from pygame.locals import *
from symbols import symbols    


pygame.init()

tileset_image = pygame.image.load(TILESET)

SCREEN = pygame.display.set_mode(
    (viewportWidth, viewportHeight),
    DOUBLEBUF|HWSURFACE|RESIZABLE|FULLSCREEN,
    0
)
draw_surface = pygame.Surface(size=(ttyW * W, ttyH * H))
font = pygame.font.Font(FONT, H)
fontb = pygame.font.SysFont(FONTB, H+7)

draw_surface.fill(defaultBG)
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
        draw_surface.blit(
            source=tileset_image,
            dest=(x, y, W, H),
            area=(sheetX*tileW, sheetY*tileH, tileW, tileH),
        )
    else:
        pygame.draw.rect(draw_surface, bgcolour, (x, y, W, H), 0)  # background
        if l and l != ' ':
            # if mode == 'special':
            #     print('missing a special character: ', l)
            #     pygame.draw.rect(draw_surface, RED, (x, y, W, H), 2)

            current_font = fontb if attr['weight'] == 'bold' else font
            xoffset = 0

            if draw:  # show background behind letters
                sheetX, sheetY = tileset.get_tile('empty')
                draw_surface.blit(
                    source=tileset_image,
                    dest=(x, y, W, H),
                    area=(sheetX*tileW, sheetY*tileH, tileW, tileH),
                )
                # attempting to center the letter in the tile
                xoffset = current_font.metrics(l)[0][0] / 2

            draw_surface.blit(
                source=current_font.render(l, True, fgcolour),
                dest=(x+xoffset, y-4, W, H),
            )

    if frame:
        pygame.draw.rect(draw_surface, defaultFG, (x, y, W, H), 1)

    # if attr['weight'] == 'bold':
    #    pygame.draw.rect(draw_surface, (255,255,255), (x, y, W, H), 2)
