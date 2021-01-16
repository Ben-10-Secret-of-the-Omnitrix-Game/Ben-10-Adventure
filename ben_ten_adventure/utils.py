from os.path import join, exists
from os import mkdir


DEFAULT_RESOURCES_PATH = "Ben-10-Adventure/resources"


def init_resource_dirs():
    if not exists(join("resources")):
        mkdir("resources")

class RawData:
    pass


class Config:
    """

    """
    pass


class GameAssets:
    def __init__(self, game_config: Config):
        pass

    # def _load_resources(self):
