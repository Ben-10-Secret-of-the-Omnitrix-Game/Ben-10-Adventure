import pygame
import cv2
import numpy
import pytmx
import sys

from .utils import Movie, DEFAULT_RESOURCES_PATH, Camera
from .scene import Scene
from .graphics import Tile
from .entity import Player, NPC

from os.path import join, split
from pygame.transform import scale


class AdventureScene:
    PLAYING = 0
    END = 1
    """
    Base class for every adventure.
    * Any adventure must inherit be inherited from it.
    """
    pass
        

class AdventureManager:
    """
    Manages adventure list
    Has properties:
        name    -   somehow displayed name of adventure
        config  -   configuration file. Instance of ben_ten_adventure.utils.config.Config
                    Config should contain information about (asset files, ... will exand soon) 

        that's all by now
    """
    pass


class SecretOfTheOmnitrix(AdventureScene):
    def __init__(self, screen, ga):
        self.screen = screen
        self.ga = ga
        self.stages = [
            self.play_scene_1,
            self.play_scene_2,
            self.play_scene_3,
            self.play_scene_4,
            self.play_scene_5]
        self._index = 0
        self.init_funcs = [
            self.init_scene_1,
            self.init_scene_2,
            self.init_scene_2,
            self.init_scene_3,
            self.init_scene_4,
            self.init_scene_5]

        self.play_data = {}
        
    def init_scene_1(self):
        kwargs = {}
        kwargs['intro'] = Movie(join(DEFAULT_RESOURCES_PATH, "videos", "ben_10_test2.mp4"))
        return kwargs
        
        
    def play_scene_1(self, kwargs):
        """
        First video. 
        """
        self.handle_event(kwargs)
        if not kwargs['intro'].tick(self.screen):
            print("Video ended")
            return self.END
        print("Running")

        
    def init_scene_2(self):
        kwargs = {}
        kwargs['map'] = pytmx.TiledMap(join(DEFAULT_RESOURCES_PATH, "maps", "scene_1.tmx"))
        ben_images = [self.ga.ben10_1_128_128, self.ga.ben10_2_128_128,
                  self.ga.ben10_3_128_128, self.ga.ben10_4_128_128]
        kwargs['player'] = Player('Ben', ben_images, x=250, y=250, speed=15)
        kwargs['camera'] = Camera()
        return kwargs
        
    
    def play_scene_2(self, kwargs):
        """
        Fight between Ben 10 and prisoners. Save Myaxx
        """
        self.handle_event(kwargs)
        
        self.render_map(kwargs)
        kwargs['player'].render(self.screen)
        kwargs['camera'].update(kwargs['player'])
        
    
    def init_scene_3(self):
        pass
    
    def play_scene_3(self, kwargs):
        """
        Flying to Azmuth's planet
        """
        self.handle_event(kwargs)
    
    def init_scene_4(self):
        pass
    
    def play_scene_4(self, kwargs):
        """
        Fighting with Vilgax
        """
        self.handle_event(kwargs)
    
    def init_scene_5(self):
        pass
    
    def play_scene_5(self, kwargs):
        """
        Urge Azmuth to keep omnitrix in Ben's hand.  
        """
        self.handle_event(kwargs)
    
    def play_current(self):
        if not self.play_data:
            initialization_function = self.init_funcs[self._index]
            self.play_data = initialization_function()
        
        
        stage = self.stages[self._index]
        if stage(kwargs=self.play_data) == self.END:
            if self._index + 1 < len(self.stages):
                self._index += 1 
                initialization_function = self.init_funcs[self._index]
                self.play_data = initialization_function()
            else:
                # finish adventure
                print("Finish")
    
    def render_map(self, kwargs):
            for layer in kwargs['map'].layers:
                for x, y, image in layer.tiles():
                    file_name = split(image[0])[-1]
                    asset_name = file_name.split('.')[0]
                    tile = Tile(x, y, (600, 100), image=getattr(self.ga, asset_name), tile_size=128)
                    tile.render_isometric_tile(self.screen)
                    
    def handle_event(self, kwargs):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEOEXPOSE:  # handles window minimising/maximising
                # screen.fill((0, 0, 0))
                self.screen.blit(scale(
                    self.screen, self.screen.get_size()), (0, 0))
                pygame.display.update()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                # border_offset = self.screen.get_width() - TILE_SIZE[0] * MAP_WIDTH
            elif event.type == pygame.MOUSEMOTION:
                mouse_x_y = pygame.mouse.get_pos()
            elif event.type == pygame.KEYDOWN:
                btns_pressed = tuple(pygame.key.get_pressed())[79:83]
                if 'player' in kwargs:
                    kwargs['player'].move(btns_pressed)
