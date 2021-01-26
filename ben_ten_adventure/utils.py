import logging
import json

import pygame
import pyglet


from os.path import join, exists
from os import mkdir
from pprint import pprint

from .game_engine import RESOLUTION, VIDEOS


DEFAULT_RESOURCES_PATH = join("resources")
DEFAULT_GAMEDATA_PATH = join("game_data")


def init_resource_dirs():
    if not exists(DEFAULT_RESOURCES_PATH):
        mkdir(DEFAULT_RESOURCES_PATH)
    if not exists(DEFAULT_GAMEDATA_PATH):
        mkdir(DEFAULT_GAMEDATA_PATH)


loaded_videos = {}


def load_additional_resources():
    for file_name in VIDEOS:
        loaded_videos[file_name] = pyglet.media.load(
            join(DEFAULT_RESOURCES_PATH, file_name))


key = pyglet.window.key


class Movie(pyglet.window.Window):
    def __init__(self, file_name):
        super().__init__(*RESOLUTION, fullscreen=False)
        self.x, self.y = 0, 0

        self.player = pyglet.media.Player()
        assert loaded_videos != {}, \
        "Make sure game_engine.VIDEOS is not emptry and you ran load_additional_resources firstly"
        self.player.queue(loaded_videos[file_name])
        self.sprites = {'video': None}

        self.alive = 1

    def on_draw(self):
        self.render()

    def on_close(self):
        self.alive = 0

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == 65307:  # [ESC]
            self.alive = 0
        elif symbol == key.LCTRL:
            self.player.play()

    def render(self):
        self.clear()

        if self.player.playing:
            if self.sprites['video'] is None:
                texture = self.player.get_texture()
                if texture:
                    self.sprites['video'] = pyglet.sprite.Sprite(texture)
            else:
                self.sprites['video'].draw()

        self.flip()

    def run(self):
        while self.alive == 1:
            self.render()
            event = self.dispatch_events()


class RawData:
    pass


class Config:
    JSON = 0

    def __init__(self, file_path, file_type=JSON, default=[]):
        """
        Note you must save everything related to Configs to game_data dir!
        file_path -> full path to file with extension. E.g. join("world", "level1", "level1.json")
        file_type -> currently supporting only Json format. Yaml format in plans.  
        """
        self.file_path = file_path
        self.file_type = file_type
        self.default = default
        self.data = []
        self.changed = False

        self.load()

    def save(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            if self.file_type == self.JSON:
                json.dump(self.data, f, ensure_ascii=False, indent=4)

    def load(self):
        if not exists(self.file_path):
            self.save()

        if self.file_type == self.JSON:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)

        self.data = self.data if len(self.data) > 0 else self.default
        # if in self.data == self.default (see above) in this case we need to save file.
        self.save()


class GameAssets:
    def __init__(self):
        self.config = Config(join(DEFAULT_RESOURCES_PATH,
                                  "manifest.json"), Config.JSON)
        self._load_resources()

    def _load_resources(self):
        if len(self.config.data) < 1:
            logging.error(
                f"Tried to load {join(DEFAULT_GAMEDATA_PATH, 'manifest.json')} but it's empty.\
                If you already have images, run scripts/combine_images_into_single.py")
            return
        image = pygame.image.load(
            join(DEFAULT_RESOURCES_PATH, "_compiled.png"))
        # we don't need to convert, becuase scripts/combine_images_into_single.py already done it.
        # TODO add check for alpha if someone made fake manifest.json

        for image_data in self.config.data:
            name, offset_x, offset_y, size_x, size_y = image_data.values()
            logging.info(f"Loading {name} with size {size_x}, {size_y}")
            cropped = image.subsurface((offset_x, offset_y, size_x, size_y))
            self.__setattr__(name, cropped)

        logging.info(f"Loaded {len(self.config.data)} images")
