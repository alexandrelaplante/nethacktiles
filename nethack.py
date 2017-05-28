# -*- coding: utf-8 -*-
import telnetlib
import pygame
import re

from constants import *

connection = telnetlib.Telnet(HOST)

import os
os.popen('stty cols {}'.format(ttyW))
rows, columns = os.popen('stty size', 'r').read().split()
print(rows, columns)


from parser import Parser
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
        pygame.display.update()
