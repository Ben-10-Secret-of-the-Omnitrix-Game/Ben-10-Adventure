"""
Contains pygame.init() and related stuff

"""

import pygame
import sys

from .utils import GameAssets, init_resource_dirs

def draw_main_ui():
    pass

def init():
    global screen
    pygame.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode((500, 500))
    
def start():
    global ga, clock, fps
    # .utils.py
    init_resource_dirs()
    ga = GameAssets()
    clock = pygame.time.Clock()
    fps = 30
    
    # screen.blit(ga.background, (0, 0, 500, 500))
    # screen.blit(ga.play_button, (0, 0, 32, 32))
    # screen.blit(ga.play_button_64, (250, 160, 64, 64))
    # screen.blit(ga.ben10_1, (150, 150, 70, 205))
    # pygame.display.flip()
    # while True:
    #     event = pygame.event.poll()
    #     if event.type == pygame.QUIT:
    #         pygame.quit()
    #         sys.exit()
        
    #     pygame.display.flip()

def game_loop_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    clock.tick(fps)
    # screen.blit(ga.background, (0, 0, 500, 500))
    # screen.blit(ga.play_button, (0, 0, 32, 32))
    # screen.blit(ga.play_button_64, (200, 160, 64, 64))
    # screen.blit(ga.ben10_1, (150, 150, 70, 205))
    screen.fill(pygame.Color(255, 255, 255, 255))
    screen.blit(ga.omnitrix_secret_button, (100, 100, 176, 37))
    screen.blit(ga.omnitrix_secret_btn_simple, (100, 150, 176, 37))
    pygame.display.flip()
    

