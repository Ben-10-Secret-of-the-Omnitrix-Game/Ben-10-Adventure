"""
Contains pygame.init() and related stuff

"""

import pygame
import sys

from .utils import GameAssets, init_resource_dirs

def draw_main_ui():
    pass

def start():
    pygame.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode((1280, 720))
    
    # .utils.py
    init_resource_dirs()
    ga = GameAssets()
    
    screen.blit(ga.play_button, (0, 0, 32, 32))
    screen.blit(ga.play_button_64, (0, 32, 64, 64))
    pygame.display.flip()
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        pygame.display.flip()

