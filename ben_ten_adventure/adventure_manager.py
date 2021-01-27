import pygame
import cv2
import numpy
import pytmx

from .utils import Movie, DEFAULT_RESOURCES_PATH
from .scene import Scene
from .graphics import Tile

from os.path import join, split


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
        kwargs['intro'] = Movie(join(DEFAULT_RESOURCES_PATH, "Ben10_TEST_movie.mp4"))
        kwargs['screen'] = self.screen
        return kwargs
        
    def play_scene_1(self, kwargs):
        """
        First video. 
        """
        if not kwargs['intro'].tick(self.screen):
            print("Video ended")
            return self.END
        print("Running")

        
    def init_scene_2(self):
        kwargs = {}
        kwargs['map'] = pytmx.TiledMap(join(DEFAULT_RESOURCES_PATH, "maps", "scene_1.tmx"))
        return kwargs
        
    def render_map(self, kwargs):
            for layer in kwargs['map'].layers:
                for x, y, image in layer.tiles():
                    file_name = split(image[0])[-1]
                    asset_name = file_name.split('.')[0]
                    tile = Tile(x, y, (600, 100), image=getattr(self.ga, asset_name), tile_size=128)
                    tile.render_isometric_tile(self.screen)
    
    def play_scene_2(self, kwargs):
        """
        Fight between Ben 10 and prisoners. Save Myaxx
        """
        self.render_map(kwargs)
    
    def init_scene_3(self):
        pass
    
    def play_scene_3(self):
        """
        Flying to Azmuth's planet
        """
        pass
    
    def init_scene_4(self):
        pass
    
    def play_scene_4(self):
        """
        Fighting with Vilgax
        """
        pass
    
    def init_scene_5(self):
        pass
    
    def play_scene_5(self):
        """
        Urge Azmuth to keep omnitrix in Ben's hand.  
        """
        pass
    
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
    