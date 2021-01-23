"""
Contains pygame.init() and related stuff

"""

from os.path import join
from hotreload.reloader import Loader
import logging
import pygame
import sys

from .utils import Config, DEFAULT_GAMEDATA_PATH, GameAssets, init_resource_dirs
from .entity import Player, NPC
from .ui import ButtonSprite
from .weapon import BaseWeapon


win_size = (1280, 720)


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
    return pygame.transform.scale(bigSurf, size)

def draw_main_ui():
    screen.blit(vertical(win_size, (255, 213, 65, 255), (49, 62, 76, 255)), (0, 0))
    start_adventure_button = ButtonSprite(400, 400, [ga.start_adventure_button_x2])
    options_button = ButtonSprite(440, 470, [ga.options_button_x2])
    start_adventure_button.draw(screen)
    options_button.draw(screen)



def init():
    global screen, DEBUG, MAP_WIDTH, MAP_HEIGHT, TILE_SIZE, border_offset, game_config
    
    # game config for initialization
    game_config = Config(join(DEFAULT_GAMEDATA_PATH, 'game_data.json'), Config.JSON,
                             {
                                 'debug': True,
                                 'resolution': (1280, 720),
                                 'tile_size': 128,
                                 'map_size': (10, 10),
                             })
    # few global constants
    DEBUG = game_config.data['debug']
    RESOLUTION = game_config.data['resolution']
    TILE_SIZE = game_config.data['tile_size']
    MAP_WIDTH, MAP_HEIGHT = game_config.data['map_size']

    # pygame
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(RESOLUTION, flags=pygame.RESIZABLE)
    
    # Centralize map
    x_pad = TILE_SIZE    # prevent from float values
    y_pad = MAP_HEIGHT * TILE_SIZE # prevent from float values
    border_offset = (500, 100)
    print(x_pad, y_pad)
    print(border_offset)


def start():
    global screen, ga, clock, fps, script, ben, alien_v
    
    if DEBUG:
        script = Loader(join("ben_ten_adventure", "graphics.py"),
                        "ben_ten_adventure.graphics", 1)
    
    # .utils.py
    init_resource_dirs()
    ga = GameAssets()
    
    # world ticking
    clock = pygame.time.Clock()
    fps = 30

    # draw ui
    # draw_main_ui()
    

    alien_v_images = [ga.Alien_V_128_128, ga.Alien_V_128_128,
                      ga.Alien_V_128_128, ga.Alien_V_128_128]
    alien_v = NPC('', alien_v_images, x=border_offset[0], y=border_offset[1], speed=1)
    big_gun = BaseWeapon(100, 50)
    alien_v.set_weapon(big_gun)

    ben_images = [ga.ben10_1_128_128, ga.ben10_2_128_128,
                  ga.ben10_3_128_128, ga.ben10_4_128_128]
    ben = Player('Ben', ben_images, x=border_offset[0] + 150, y=border_offset[1] + 150, speed=15)
    


def handle_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEOEXPOSE:  # handles window minimising/maximising
            # screen.fill((0, 0, 0))
            screen.blit(pygame.transform.scale(
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
    global border_offset, ben, alien_v

    handle_event()

    clock.tick(fps)
    
    screen.fill((0, 0, 0))
    
    render_map()

    if DEBUG:
        if script.has_changed():
            pygame.time.wait(500)

    
    ben.render(screen)
    alien_v.render(screen)
    alien_v.go_to(ben)
    alien_v.attack(ben)
    
    
    
    # TODO replace with update
    pygame.display.flip()
    # Carefull! border_offset need to convert to isometrix coordinates first!
    # pygame.display.update((border_offset, border_offset / 2, border_offset, border_offset / 2))


class Activity:
    """
    Has states:
    PLAYING -   means we need to render player, tiles ...
    UI      -   means we need to render only ui elementes. Currenly user is in "user interface"
    """
    pass
