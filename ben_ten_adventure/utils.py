import logging
import json

import pygame
from pygame import mixer
import cv2
import numpy

from os.path import join, exists
from os import mkdir
from pprint import pprint

DEFAULT_RESOURCES_PATH = join("resources")
DEFAULT_GAMEDATA_PATH = join("game_data")


def init_resource_dirs():
    if not exists(DEFAULT_RESOURCES_PATH):
        mkdir(DEFAULT_RESOURCES_PATH)
    if not exists(DEFAULT_GAMEDATA_PATH):
        mkdir(DEFAULT_GAMEDATA_PATH)


class Movie:

    def __init__(self, file_path):
        self.video = cv2.VideoCapture(file_path)
        self.start_audio = False
        mixer.init()
        mixer.music.load(join(DEFAULT_RESOURCES_PATH, "videos", "ben_10_test2.mp3"))

    def tick(self, screen):
        if not self.start_audio:
            mixer.music.set_volume(0.01)
            mixer.music.play()
            self.start_audio = True
        retval, frame = self.video.read()
        if not retval:
            return False
        # Rotate it, because for some reason it otherwise appears flipped.
        # frame = numpy.rot90(frame)
        frame = numpy.rot90(numpy.fliplr(frame))
        # The video uses BGR colors and PyGame needs RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Create a PyGame surface
        surf = pygame.surfarray.make_surface(frame)
        # Show the PyGame surface!
        screen.blit(surf, (0, 0))
        pygame.display.update((100, 100, 200, 200))
        pygame.time.Clock().tick(180)
        return True


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - target.rect.width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - target.rect.height // 2)


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
