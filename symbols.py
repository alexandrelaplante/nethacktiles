from constants import *


class Symbol(object):
    tile = None  # from nethacks's source txt files
    offset = 0  # nth occurance in the txt files
    letter = None
    fgcolour = '*'
    bgcolour = '*'
    weight = '*'
    mode = 'normal'


class SpecialVerticalWall(Symbol):
    letter = 'x'
    mode = 'special'
    tile = 'wall'
    offset = 0


class SpecialHorizontalWall(Symbol):
    letter = 'q'
    mode = 'special'
    tile = 'wall'
    offset = 1


class SpecialTopLeftCornerWall(Symbol):
    letter = 'l'
    mode = 'special'
    tile = 'wall'
    offset = 2


class SpecialTopRightCornerWall(Symbol):
    letter = 'k'
    mode = 'special'
    tile = 'wall'
    offset = 3


class SpecialBottomLeftCornerWall(Symbol):
    letter = 'm'
    mode = 'special'
    tile = 'wall'
    offset = 4


class SpecialBottomRightCornerWall(Symbol):
    letter = 'j'
    mode = 'special'
    tile = 'wall'
    offset = 5


class SpecialTotalJunctionWall(Symbol):
    letter = 'n'
    mode = 'special'
    tile = 'wall'
    offset = 6


class SpecialDownJunctionWall(Symbol):
    letter = 'v'
    mode = 'special'
    tile = 'wall'
    offset = 7


class SpecialUpJunctionWall(Symbol):
    letter = 'w'
    mode = 'special'
    tile = 'wall'
    offset = 8


class SpecialRightJunctionWall(Symbol):
    letter = 'u'
    mode = 'special'
    tile = 'wall'
    offset = 9


class SpecialLeftJunctionWall(Symbol):
    letter = 't'
    mode = 'special'
    tile = 'wall'
    offset = 10


class SpecialFloor(Symbol):
    letter = '~'
    mode = 'special'
    tile = 'floor of a room'


class SpecialOpenDoor(Symbol):
    letter = 'a'
    mode = 'special'
    tile = 'open door'


class ClosedDoor(Symbol):
    tile = 'closed door'
    letter = '+'
    fgcolour = YELLOW


class LitCorridor(Symbol):
    tile = 'lit corridor'
    letter = '#'
    weight = 'bold'


class Corridor(Symbol):
    tile = 'corridor'
    letter = '#'
    weight = 'normal'


class StaircaseUp(Symbol):
    tile = 'staircase up'
    letter = '<'


class StaircaseDown(Symbol):
    tile = 'staircase down'
    letter = '>'


class Fountain(Symbol):
    tile = 'fountain'
    letter = '{'
    fgcolour = BLUE


class Water(Symbol):
    tile = 'water'
    letter = '}'
    fgcolour = BLUE


class MoltenLava(Symbol):
    tile = 'molten lava'
    letter = '}'
    fgcolour = RED


class DarkPartOfARoom(Symbol):
    tile = 'dark part of a room'
    offset = 1
    letter = '.'
    weight = 'bold'


class FloorOfARoom(Symbol):
    tile = 'floor of a room'
    letter = '.'
    weight = 'normal'


class GoldPiece(Symbol):
    tile = 'gold piece'
    letter = '$'
    fgcolour = YELLOW


class Scroll(Symbol):
    tile = 'READ ME'
    letter = '?'
    fgcolour = defaultFG


class HorizontalWall(Symbol):
    tile = 'wall'
    offset = 1
    letter = '-'
    fgcolour = defaultFG


class VerticalWall(Symbol):
    tile = 'wall'
    offset = 0
    letter = '|'
    fgcolour = defaultFG


class Boulder(Symbol):
    tile = 'boulder'
    letter = '0'


class Altar(Symbol):
    tile = 'altar'
    letter = '_'


class Corpse(Symbol):
    tile = 'corpse'
    letter = '%'


class OpenDoorHorizontal(Symbol):
    tile = 'open door'
    letter = '-'
    fgcolour = YELLOW


class OpenDoorVertical(Symbol):
    tile = 'open door'
    offset = 1
    letter = '|'
    fgcolour = YELLOW


class Player(Symbol):
    tile = 'archeologist'
    letter = '@'
    weight = 'bold'


class Leprechaun(Symbol):
    tile = 'leprechaun'
    letter = 'l'
    fgcolour = GREEN


class Homunculus(Symbol):
    tile = 'homunculus'
    letter = 'i'
    fgcolour = GREEN


class Hobbit(Symbol):
    tile = 'hobbit'
    letter = 'h'
    fgcolour = GREEN


class Fox(Symbol):
    tile = 'fox'
    letter = 'h'
    fgcolour = RED


class Gnome(Symbol):
    tile = 'gnome'
    letter = 'G'
    fgcolour = YELLOW


class GnomeLord(Symbol):
    tile = 'gnome lord'
    letter = 'G'
    fgcolour = BLUE


class GuardianNaga(Symbol):
    tile = 'guardian naga'
    letter = 'N'
    fgcolour = GREEN


class RedDragon(Symbol):
    tile = 'red dragon'
    letter = 'D'
    fgcolour = RED


class BlackDragon(Symbol):
    tile = 'black dragon'
    letter = 'D'
    fgcolour = BLACK


class FloatingEye(Symbol):
    tile = 'floating eye'
    letter = 'e'
    fgcolour = BLUE


class GridBug(Symbol):
    tile = 'grid bug'
    letter = 'x'
    fgcolour = MAGENTA


class Ape(Symbol):
    tile = 'ape'
    letter = 'Y'
    fgcolour = YELLOW


class GoldenNaga(Symbol):
    tile = 'golden naga'
    letter = 'N'
    fgcolour = YELLOW


class Pony(Symbol):
    tile = 'pony'
    letter = 'u'
    fgcolour = YELLOW


class Newt(Symbol):
    tile = 'newt'
    letter = ':'
    fgcolour = YELLOW


class Gecko(Symbol):
    tile = 'gecko'
    letter = ':'
    fgcolour = GREEN


class GiantBat(Symbol):
    tile = 'giant bat'
    letter = 'B'
    fgcolour = RED


class Dog(Symbol):
    tile = 'dog'
    letter = 'e'
    weight = 'bold'


class Housecat(Symbol):
    tile = 'housecat'
    letter = 'f'
    weight = 'bold'


class Imp(Symbol):
    tile = 'imp'
    letter = 'i'
    fgcolour = RED


class RedGem(Symbol):
    tile = 'red / ruby'
    letter = '*'
    fgcolour = RED


class BlackGem(Symbol):
    tile = 'black / black opal'
    letter = '*'
    fgcolour = BLACK


class GreenGem(Symbol):
    tile = 'green / emerald'
    letter = '*'
    fgcolour = GREEN


class YellowGem(Symbol):
    tile = 'yellow / citrine'
    letter = '*'
    fgcolour = YELLOW


class BugBear(Symbol):
    tile = 'bugbear'
    letter = 'h'
    fgcolour = YELLOW


class Mimic(Symbol):
    tile = 'small mimic'
    letter = 'm'
    fgcolour = YELLOW


class WinterWolf(Symbol):
    tile = 'winter wolf'
    letter = 'd'
    fgcolour = CYAN


class Cockatrice(Symbol):
    tile = 'cockatrice'
    letter = 'c'
    fgcolour = YELLOW


class Rothe(Symbol):
    tile = 'rothe'
    letter = 'q'
    fgcolour = YELLOW


symbols = [c for c in Symbol.__subclasses__()]
