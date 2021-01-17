# add stuff to start
"""
finally should be like:


if __name__ == '__main__':
    engine.start()
"""
import logging
import coloredlogs
import pygame

from hotreload import Loader
from os.path import join

from .tests import utils_test
from . import game_engine


if __name__ == '__main__':
    coloredlogs.install(level='DEBUG')
    script = Loader(join("ben_ten_adventure", "game_engine.py"), "ben_ten_adventure.game_engine", 1)
    
    game_engine.init()
    script.start()
    
    while True:
        if script.has_changed():
            pygame.time.wait(500)
        script.game_loop_handler()

    # utils_test.run_tests()
    
