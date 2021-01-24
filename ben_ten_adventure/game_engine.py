"""
Contains pygame.init() and related stuff

"""

from os.path import join

from pygame.mixer import pause
from pygame.transform import scale
from hotreload.reloader import Loader

import logging
import pygame
import sys
import pygame_gui

from .utils import Config, DEFAULT_GAMEDATA_PATH, GameAssets, init_resource_dirs
from .entity import Player, NPC
from .ui import ButtonSprite
from .weapon import BaseWeapon
from .animation import ButtonAnimation



HD = (1280, 720)
FULL_HD = (1920, 1080)

def vertical(size, startcolor, endcolor):
    """
    Draws a vertical linear gradient filling the entire surface. Returns a
    surface filled with the gradient (numeric is only 2-3 times faster).
    """
    height = size[1]
    bigSurf = pygame.Surface((1, height)).convert_alpha()
    dd = 1.0/height
    sr, sg, sb, sa = startcolor
    er, eg, eb, ea = endcolor
    rm = (er-sr)*dd
    gm = (eg-sg)*dd
    bm = (eb-sb)*dd
    am = (ea-sa)*dd
    for y in range(height):
        bigSurf.set_at((0, y),
                       (int(sr + rm*y),
                        int(sg + gm*y),
                        int(sb + bm*y),
                        int(sa + am*y))
                       )
    return scale(bigSurf, size)

def draw_main_screen():
    # background_gradient = vertical(win_size, (118, 174, 62, 255), (9, 48, 21, 255))

    if RESOLUTION <= HD:
        sab = pygame_gui.elements.UIButton(pygame.Rect(500, 360, 272, 50), '', manager=manager)
        sab.drawable_shape.states['normal'].surface.blit(ga.start_adventure_button_x2, (0, 0))
        sab.drawable_shape.active_state.has_fresh_surface = True
        
        ob = pygame_gui.elements.UIButton(pygame.Rect(540, 410, *ga.options_button_x2.get_rect()[2:]), '', manager=manager)
        ob.drawable_shape.states['normal'].surface.blit(ga.options_button_x2, (0, 0))
        ob.drawable_shape.active_state.has_fresh_surface = True
    elif RESOLUTION >= FULL_HD:
        sab_size = ga.start_adventure_button_x2.get_rect()[2:]
        sab_new = scale(ga.start_adventure_button_x2, (sab_size[0] * 2, sab_size[1] * 2))
        sab = pygame_gui.elements.UIButton(pygame.Rect(350, 300, *sab_new.get_rect()[2:]), '', manager=manager)
        sab.drawable_shape.states['normal'].surface.blit(sab_new, (0, 0))
        sab.drawable_shape.active_state.has_fresh_surface = True
        
        ob_size = ga.options_button_x2.get_rect()[2:]
        ob_new = scale(ga.options_button_x2, (ob_size[0] * 2, ob_size[1] * 2))
        ob = pygame_gui.elements.UIButton(pygame.Rect(450, 400, *ob_new.get_rect()[2:]), '', manager=manager)
        ob.drawable_shape.states['normal'].surface.blit(ob_new, (0, 0))
        ob.drawable_shape.active_state.has_fresh_surface = True



def init():
    global screen, DEBUG, MAP_WIDTH, MAP_HEIGHT, TILE_SIZE, ACTION, border_offset, game_config, RESOLUTION
    
    # game config for initialization
    game_config = Config(join(DEFAULT_GAMEDATA_PATH, 'game_data.json'), Config.JSON,
                             {
                                 'debug': True,
                                 'resolution': HD,
                                 'tile_size': 128,
                                 'map_size': (10, 10),
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
    ACTION = Activity.MAIN_SCREEN

    # pygame
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(RESOLUTION, flags=pygame.RESIZABLE)
    
    # Centralize map
    x_pad = TILE_SIZE    # prevent from float values
    y_pad = MAP_HEIGHT * TILE_SIZE # prevent from float values
    border_offset = (500, 100)


def start():
    global screen, ga, clock, fps, script, ben, alien_v, manager
    
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
    manager = pygame_gui.UIManager(RESOLUTION)
    

    alien_v_images = [ga.ben10_1_128_128, ga.ben10_2_128_128,
                  ga.ben10_3_128_128, ga.ben10_4_128_128]
    alien_v = NPC('', alien_v_images, x=border_offset[0], y=border_offset[1], speed=1)
    big_gun = BaseWeapon(100, 50)
    alien_v.set_weapon(big_gun)

    ben_images = [ga.ben10_1_128_128, ga.ben10_2_128_128,
                  ga.ben10_3_128_128, ga.ben10_4_128_128]
    ben = Player('Ben', ben_images, x=border_offset[0] + 150, y=border_offset[1] + 150, speed=15)
    
    


def handle_event():
    global manager
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
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                print("Clicked")
        manager.process_events(event)
        


def render_map():
    for row in range(0, MAP_WIDTH):
        for col in range(0, MAP_HEIGHT):
            tile = script.Tile(row, col, border_offset=border_offset,
                               image=ga.wall_5_marine, tile_size=TILE_SIZE)
            tile.render_isometric_tile(screen)

            
def game_loop_handler():
    time_delta = clock.tick(fps) / 1000.0
    handle_event()
    
    screen.fill((0, 0, 0, 0)) 


    manager.update(time_delta)

    if ACTION == Activity.MAIN_SCREEN:
        draw_main_screen()
        screen.blit(scale(ga.main_screen, screen.get_size()), (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()
        return
    elif ACTION == Activity.PAUSE:
        manager.draw_ui(screen)
        pygame.display.update()
        return
    elif ACTION == Activity.PLAYING:
        manager.draw_ui(screen)
        pass
        
    
    render_map()
    
    if DEBUG:
        if script.has_changed():
            pygame.time.wait(500)
    
    ben.render(screen)
    alien_v.render(screen)
    alien_v.go_to(ben)
    alien_v.attack(ben)
    
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
