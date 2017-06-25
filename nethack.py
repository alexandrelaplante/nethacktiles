# -*- coding: utf-8 -*-
import telnetlib
import pygame
from pygame.locals import *
import re
import os

from constants import *
from parser import Parser
from draw import SCREEN, draw_surface


connection = telnetlib.Telnet(HOST)

os.popen('stty cols {}'.format(ttyW))
rows, columns = os.popen('stty size', 'r').read().split()
parser = Parser()


# import cProfile, pstats, StringIO
# pr = cProfile.Profile()
# pr.enable()


running = True
try:
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_ESCAPE:
            #     running = False

            connection.write(str(event.unicode))

        elif event.type == VIDEORESIZE:
            pass
            # SCREEN = pygame.display.set_mode(event.dict['size'], HWSURFACE|RESIZABLE)
            # viewportWidth, viewportHeight = event.dict['size']

        parser.read = connection.read_until('LOLZ', timeout=0.1)

        if parser.read:
            parser.parse()
            parser.grid.post_process()
            parser.grid.draw()
            parser.grid.after_draw()

            if ENABLE_SCALING:
                surface = pygame.transform.scale(
                    draw_surface,
                    (viewportWidth, viewportHeight),
                )
            else:
                surface = draw_surface
            SCREEN.blit(surface, (0, 0))
            pygame.display.update()
except:
    pass


# pr.disable()
# s = StringIO.StringIO()
# sortby = 'cumulative'
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
# lines = [line for line in s.getvalue().split('\n')]
# for line in lines[::-1]:
#     print line