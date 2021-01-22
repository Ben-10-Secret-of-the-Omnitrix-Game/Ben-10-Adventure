"""
Contains pygame.init() and related stuff

"""

import logging
import pygame
import sys

from .utils import GameAssets, init_resource_dirs
from .graphics import Tile
from hotreload import Loader

from os.path import join
from os import environ

import ctypes

environ['SDL_VIDEO_CENTERED'] = '1'
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

if screensize[0] > 1920:
    win_size = (1920, 1080)
elif screensize[0] > 1280:
    win_size = (1280, 720)
else:
    win_size = (720, 480)


def draw_main_ui():
    pass


def init():
    global screen, MAP_WIDTH, MAP_HEIGHT, TILE_SIZE, border_offset
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((win_size), flags=pygame.RESIZABLE)
    MAP_WIDTH = 5
    MAP_HEIGHT = 5
    TILE_SIZE = (32, 32)
    # TODO replace with more approximate offset
    border_offset = screen.get_width() / 2 + TILE_SIZE[0] * MAP_WIDTH


def start():
    global ga, clock, fps, script
    script = Loader(join("ben_ten_adventure", "graphics.py"), "ben_ten_adventure.graphics", 1)
    # .utils.py
    init_resource_dirs()
    ga = GameAssets()
    clock = pygame.time.Clock()
    fps = 30


def game_loop_handler():
    global border_offset
    screen.fill((0, 0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEOEXPOSE:  # handles window minimising/maximising
            screen.fill((0, 0, 0))
            screen.blit(pygame.transform.scale(screen, screen.get_size()), (0, 0))
            pygame.display.update()
            border_offset = screen.get_width() - TILE_SIZE[0] * MAP_WIDTH
        elif event.type == pygame.MOUSEMOTION:
            mouse_x_y = pygame.mouse.get_pos()

    clock.tick(fps)
    if script.has_changed():
        pygame.time.wait(500)
    for row in range(0, MAP_WIDTH):
        for col in range(0, MAP_HEIGHT):
            tile = script.Tile(row, col, border_offset=border_offset, image=ga.snow, tile_size=TILE_SIZE)
            tile.render_isometric_tile(screen)
    # 
    # TODO replace with update
    pygame.display.flip()
    # Carefull! border_offset need to convert to isometrix coordinates first! 
    # pygame.display.update((border_offset, border_offset / 2, border_offset, border_offset / 2))
