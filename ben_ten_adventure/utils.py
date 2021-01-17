import logging
import json

from os.path import join, exists
from os import mkdir


DEFAULT_RESOURCES_PATH = join("resources")
DEFAULT_GAMEDATA_PATH = join("game_data")


def init_resource_dirs():
    if not exists(DEFAULT_RESOURCES_PATH):
        mkdir(DEFAULT_RESOURCES_PATH)
    if not exists(DEFAULT_GAMEDATA_PATH):
        mkdir(DEFAULT_GAMEDATA_PATH)


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
        with open(join(DEFAULT_GAMEDATA_PATH, self.file_path), 'w', encoding='utf-8') as f:
            if self.file_type == self.JSON:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
    
    def load(self):
        if not exists(self.file_path):
            self.save()
        
        if self.file_type == self.JSON:
            with open(join(DEFAULT_GAMEDATA_PATH, self.file_path), 'w', encoding='utf-8') as f:
                self.data = json.load(f)
        
        self.data = self.data if len(self.data) > 0 else self.default
        # if in self.data == self.default (see above) in this case we need to save file. 
        self.save()
                

class GameAssets:
    def __init__(self):
        pass

        
