"""
Contains pygame.init() and related stuff

"""

from os.path import join
from random import randint
from pygame import event
from pygame.mixer import pause
from pygame.transform import scale
from hotreload.reloader import Loader

import logging
import pygame
import sys
import pygame_gui

from .utils import Config, DEFAULT_GAMEDATA_PATH, GameAssets, init_resource_dirs
from .entity import Player, NPC
from .manager import EntityManager, SecretOfTheOmnitrix, Game, TaskManager
# from .ui import HD, FULL_HD, draw_main_screen
from .weapon import BaseWeapon
from .animation import ButtonAnimation

from pprint import pprint

HD = (1280, 720)
FULL_HD = (1920, 1080)

class Activity:
    """
    Has states:
    PLAYING -   means we need to render player, tiles ...
    UI      -   means we need to render only ui elementes. Currenly user is in "user interface"
    """
    MAIN_SCREEN = 0
    PLAYING = 1
    PAUSE = 2


def init():
    global screen, DEBUG, MAP_WIDTH, MAP_HEIGHT, TILE_SIZE, ACTION, border_offset, game_config, RESOLUTION

    # game config for initialization
    game_config = Config(join(DEFAULT_GAMEDATA_PATH, 'game_data.json'), Config.JSON,
                         {
                             'debug': True,
                             'resolution': HD,
                             'tile_size': 128,
                             'map_size': (10, 10),
                             'videos': ('Ben10_TEST_movie.mp4')
                         })

    if game_config.data['resolution'] == HD:
        game_config.data['resolution'] = FULL_HD
        game_config.save()
        game_config.load()
    # few global constants
    DEBUG = game_config.data['debug']
    RESOLUTION = tuple(game_config.data['resolution'])
    TILE_SIZE = game_config.data['tile_size']
    MAP_WIDTH, MAP_HEIGHT = game_config.data['map_size']
    # VIDEOS = game_config.data['videos']

    ACTION = Activity.MAIN_SCREEN

    # pygame
    pygame.init()
    pygame.font.init()
    flags = pygame.NOFRAME | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE
    screen = pygame.display.set_mode(RESOLUTION, flags=flags)

    # Centralize map
    x_pad = TILE_SIZE  # prevent from float values
    y_pad = MAP_HEIGHT * TILE_SIZE  # prevent from float values
    border_offset = (500, 100)


def start():
    global screen, ga, clock, fps, script, adventure, MAP_WIDTH, MAP_HEIGHT, TILE_SIZE, task_manager, tick_delay, frames_played, TICK_EVENT_ID

    if DEBUG:
        script = Loader(join("ben_ten_adventure", "graphics.py"),
                        "ben_ten_adventure.graphics", 1)

    # .utils.py

    init_resource_dirs()
    ga = GameAssets()

    # world ticking
    clock = pygame.time.Clock()
    fps = 120
    #   Game ticking
    task_manager = TaskManager()
    # tick_delay = fps // 20
    TICK_EVENT_ID = pygame.USEREVENT + 10
    pygame.time.set_timer(TICK_EVENT_ID, 500, False)
    # ui init
    # ...
    
    # Game data class
    game = Game()
    game.ga = ga
    game.screen = screen
    game.task_manager = task_manager
    # game.adventure
    game.config = game_config
    game.border_offset = border_offset
    
    game.DEBUG = DEBUG
    game.RESOLUTION = RESOLUTION
    game.TILE_SIZE = TILE_SIZE
    game.MAP_WIDTH = MAP_WIDTH
    game.MAP_HEIGHT = MAP_HEIGHT
    game.ACTION = ACTION
    game.TICK_EVENT_ID = TICK_EVENT_ID
    game.entity_manager = EntityManager()
    # Adventure
    adventure = SecretOfTheOmnitrix(game)

    

def render_map():
    for row in range(0, MAP_WIDTH):
        for col in range(0, MAP_HEIGHT):
            tile = script.Tile(row, col, border_offset=border_offset,
                               image=ga.wall_5_marine, tile_size=TILE_SIZE)
            tile.render_isometric_tile(screen)


def game_loop_handler():
    screen.fill((0, 0, 0, 0))

    # pygame.display.flip()
    if DEBUG:
        if script.has_changed():
            pygame.time.wait(500)

    adventure.play_current()
    if DEBUG:
        font = pygame.font.Font(None, 40)
        fps_stat = font.render('FPS: ' + str(round(clock.get_fps(), 1)), True, (255, 0, 0))
        screen.blit(fps_stat, (500, 100))
        
    pygame.display.update()
    clock.tick(fps)
