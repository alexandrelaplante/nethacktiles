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
    DOUBLEBUF|HWSURFACE|RESIZABLE,
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

    symbol = None
    symbol2 = None

    if cell.tile is not None:
        tile1, tile2 = cell.tile
        symbol = tileset.get_tile_by_index(tile1)
        sheetX, sheetY = symbol
        if tile2:
            pass
            # symbol2 = tileset.get_tile_by_index(tile2)
            # sheetX2, sheetY2 = symbol2
    else:
        symbol = get_symbol_from_cell(cell)
        if symbol:
            sheetX, sheetY = symbol

    # This is the area of the board where tiles are possible.
    draw = cell.draw and 1 < grid_y < 23

    def draw_tile(sheetX, sheetY):
        draw_surface.blit(
            source=tileset_image,
            dest=(x, y, W, H),
            area=(sheetX*tileW, sheetY*tileH, tileW, tileH),
        )

    def draw_background():
        pygame.draw.rect(draw_surface, bgcolour, (x, y, W, H), 0)

    # if we found a tile, draw it
    if draw and symbol:
        draw_tile(sheetX, sheetY)
        # if symbol2:
        #     draw_tile(sheetX, sheetY)
    else:

        if l and l != ' ':

            current_font = fontb if attr['weight'] == 'bold' else font
            xoffset = 0

            if draw:  # show background behind letters
                draw_tile(*tileset.get_tile('empty'))
                # attempting to center the letter in the tile
                xoffset = current_font.metrics(l)[0][0] / 2
            else:
                draw_background()

            draw_surface.blit(
                source=current_font.render(l, True, fgcolour),
                dest=(x+xoffset, y-4, W, H),
            )
        else:
            draw_background()

    if frame:
        pygame.draw.rect(draw_surface, defaultFG, (x, y, W, H), 1)
