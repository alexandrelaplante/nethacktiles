# -*- coding: utf-8 -*-
import telnetlib
import pygame
import re
import os

from constants import *
from parser import Parser

connection = telnetlib.Telnet(HOST)

os.popen('stty cols {}'.format(ttyW))
rows, columns = os.popen('stty size', 'r').read().split()
print(rows, columns)

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
        parser.grid.post_process()
        parser.grid.draw()
        pygame.display.update()
