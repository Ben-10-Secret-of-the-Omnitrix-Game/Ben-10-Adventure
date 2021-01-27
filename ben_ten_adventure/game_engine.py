"""
Contains pygame.init() and related stuff

"""

from os.path import join
from random import randint
from pygame.mixer import pause
from pygame.transform import scale
from hotreload.reloader import Loader

import logging
import pygame
import sys
import pygame_gui

from .utils import Config, DEFAULT_GAMEDATA_PATH, GameAssets, init_resource_dirs
from .entity import Player, NPC
from .adventure_manager import SecretOfTheOmnitrix
# from .ui import HD, FULL_HD, draw_main_screen
from .weapon import BaseWeapon
from .animation import ButtonAnimation

from pprint import pprint

HD = (1280, 720)
FULL_HD = (1920, 1080)


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
    x_pad = TILE_SIZE    # prevent from float values
    y_pad = MAP_HEIGHT * TILE_SIZE # prevent from float values
    border_offset = (500, 100)


def start():
    global screen, ga, clock, fps, script, ben, adventure, MAP_WIDTH, MAP_HEIGHT, TILE_SIZE, npcs
    
    if DEBUG:
        script = Loader(join("ben_ten_adventure", "graphics.py"),
                        "ben_ten_adventure.graphics", 1)
    
    # .utils.py
    
    init_resource_dirs()
    ga = GameAssets()
    
    # world ticking
    clock = pygame.time.Clock()
    fps = 30
    
    # ui init
    # ...
    
    # Adventure
    adventure = SecretOfTheOmnitrix(screen, ga)
    

    npc_images = [ga.ben10_1_128_128, ga.ben10_2_128_128,
                  ga.ben10_3_128_128, ga.ben10_4_128_128]
    npcs = [NPC('', npc_images,
                x=randint(0, MAP_WIDTH * TILE_SIZE // 2),
                y=randint(0, MAP_HEIGHT * TILE_SIZE // 2),
                speed=randint(1, 3)) for _ in range(15)]
    big_gun = BaseWeapon(100, 50)

    ben_images = [ga.ben10_1_128_128, ga.ben10_2_128_128,
                  ga.ben10_3_128_128, ga.ben10_4_128_128]
    ben = Player('Ben', ben_images, x=250, y=250, speed=15)
    

def handle_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEOEXPOSE:  # handles window minimising/maximising
            # screen.fill((0, 0, 0))
            screen.blit(scale(
                screen, screen.get_size()), (0, 0))
            pygame.display.update()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
            # border_offset = screen.get_width() - TILE_SIZE[0] * MAP_WIDTH
        elif event.type == pygame.MOUSEMOTION:
            mouse_x_y = pygame.mouse.get_pos()
        elif event.type == pygame.KEYDOWN:
            btns_pressed = tuple(pygame.key.get_pressed())[79:83]
            ben.move(btns_pressed)


def render_map():
    for row in range(0, MAP_WIDTH):
        for col in range(0, MAP_HEIGHT):
            tile = script.Tile(row, col, border_offset=border_offset,
                               image=ga.wall_5_marine, tile_size=TILE_SIZE)
            tile.render_isometric_tile(screen)

            
def game_loop_handler():
    handle_event()
    screen.fill((0, 0, 0, 0)) 


    # if ACTION == Activity.MAIN_SCREEN:
    #     draw_main_screen()
    #     screen.blit(scale(ga.main_screen, screen.get_size()), (0, 0))
    #     manager.draw_ui(screen)
    #     pygame.display.update()
    #     return
    # elif ACTION == Activity.PAUSE:
    #     manager.draw_ui(screen)
    #     pygame.display.update()
    #     return
    # elif ACTION == Activity.PLAYING:
    #     manager.draw_ui(screen)
    #     pass
        
    
    # render_map()
    
    if DEBUG:
        if script.has_changed():
            pygame.time.wait(500)
    
    adventure.play_current()
    
    # ben.render(screen)
    # for npc in npcs:
    #     npc.render(screen)
    #     npc.random_move()
    #     npc.attack(ben)
    
    
    pygame.display.update()


class Activity:
    """
    Has states:
    PLAYING -   means we need to render player, tiles ...
    UI      -   means we need to render only ui elementes. Currenly user is in "user interface"
    """
    MAIN_SCREEN = 0
    PLAYING = 1
    PAUSE = 2
