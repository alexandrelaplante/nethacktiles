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
parser = Parser()


# import cProfile, pstats, StringIO
# pr = cProfile.Profile()
# pr.enable()


running = True
while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        quit()

    elif event.type == pygame.KEYDOWN:
        # if event.key == pygame.K_ESCAPE:
        #     running = False

        connection.write(str(event.unicode))

    parser.read = connection.read_until('LOLZ', timeout=0.1)
    
    if parser.read:
        parser.parse()
        parser.grid.post_process()
        parser.grid.draw()
        parser.grid.after_draw()
        pygame.display.update()


# pr.disable()
# s = StringIO.StringIO()
# sortby = 'cumulative'
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
# lines = [line for line in s.getvalue().split('\n')]
# for line in lines[::-1]:
#     print line