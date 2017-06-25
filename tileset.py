from itertools import chain

monsters = open('data/monsters.txt', 'r')
objects = open('data/objects.txt', 'r')
other = open('data/other.txt', 'r')

glyphs = []

for line in chain(*(f.readlines() for f in (monsters, objects, other))):
    if line.startswith('#'):
        start = line.index('(') + 1
        end = line.index(')')
        glyphs.append(line[start:end])

def find_nth(haystack, needle, n):
    i = -1
    for j in range(n):
        i = haystack.index(needle, i + 1)
    return i

def get_tile(name, offset=0):

    if name == 'empty':
        return 0, 37

    index = find_nth(glyphs, name, 1 + offset)
    x = index % 40
    y = index // 40

    return x, y

def get_tile_by_index(index):

    x = index % 40
    y = index // 40

    return x, y