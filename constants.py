HOST = 'nethack.alt.org'

viewportWidth, viewportHeight = (1920, 1080)

ttyW, ttyH = 150, 40

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)

defaultBG = BLACK
defaultFG = WHITE

tileW, tileH = 15, 25  # tile size in sheet
# tileW, tileH = 32, 32 # tile size in sheet
# tileW, tileH = 22, 32 # tile size in sheet
W, H = tileW, tileH  # tile size

TILESET = 'geoduck25x15.bmp'
# TILESET = 'nevanda32x32.png'
# TILESET = 'absurd22x32.png'
FONT = 'fonts/DejaVuSansMono.ttf'
# FONTB = 'fonts/DejaVuSansMono-Bold.ttf'
FONTB = 'fonts/DejaVuSansMono.ttf'

ENABLE_SCALING = False

defaultATTR = {
    'weight': 'normal',
    'underlined': False,
    'blinking': False,
    'fgcolour': defaultFG,
    'bgcolour': defaultBG,
}

import re
end_sequences = (
    re.escape('--More--'),
    re.escape('(end)'),
    re.escape('Watch which game?'),
    re.escape(' => '),
    r'\(\d of \d\)',
)

regex = '({})'.format('|'.join(end_sequences))
end_sequence_re = re.compile(regex)