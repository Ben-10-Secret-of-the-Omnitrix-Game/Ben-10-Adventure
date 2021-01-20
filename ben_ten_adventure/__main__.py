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

from ben_ten_adventure.tests import utils_test
from ben_ten_adventure import game_engine


if __name__ == '__main__':
    coloredlogs.install(level='DEBUG')
    script = Loader(join("ben_ten_adventure", "game_engine.py"), "ben_ten_adventure.game_engine", 1)
    
    game_engine.init()
    # game_engine.start()
    script.start()
    
    while True:
        # game_engine.game_loop_handler()
        if script.has_changed():
            pygame.time.wait(500)
        script.game_loop_handler()

    # utils_test.run_tests()
    
