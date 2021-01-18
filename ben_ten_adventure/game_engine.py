"""
Contains pygame.init() and related stuff

"""

import logging
import pygame
import sys

from .utils import GameAssets, init_resource_dirs
from .isometric_graphics import Tile
from hotreload import Loader
from os.path import join

def draw_main_ui():
    pass

def init():
    global screen
    pygame.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode((1920, 780), flags=pygame.RESIZABLE)
    
def start():
    global ga, clock, fps, script
    script = Loader(join("ben_ten_adventure", "isometric_graphics.py"), "ben_ten_adventure.isometric_graphics", 1)
    # .utils.py
    init_resource_dirs()
    ga = GameAssets()
    clock = pygame.time.Clock()
    fps = 30
    

def game_loop_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    clock.tick(fps)
    screen.fill((0, 0, 0, 0))
    if script.has_changed():
        pygame.time.wait(500)
    for row in range(10, 20):
        for col in range(10, 20):
            
            # tile = script.Tile(row, col, image=ga.wall_4_272 if row % 2 == 0 or col % 2 == 0 else ga.wall_4_272, wall_height=-150, tile_size=(192 / 2, 192 / 2))
            tile = script.Tile(row, col, image=ga.wall_4_272,tile_size=(96 / 2, 96 / 2))
            tile.render_isometric_tile(screen)
            # logging.info(f"Rendered tile on {row} {col}. ")
    pygame.display.flip()
    

