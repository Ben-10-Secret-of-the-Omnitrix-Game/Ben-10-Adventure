# add stuff to start
"""
finally should be like:


if __name__ == '__main__':
    engine.start()
"""
import logging
import coloredlogs

import pygame

from os.path import join

from .tests import utils_test
from . import game_engine

<<<<<<< HEAD
DEBUG=False

def main():
    coloredlogs.install(level='DEBUG')
    
    if DEBUG:
        script = Loader(join("ben_ten_adventure", "game_engine.py"), "ben_ten_adventure.game_engine", 1)
        script.init()
        script.start()
    
        while True:
            # game_engine.game_loop_handler()
            if script.has_changed():
                pygame.time.wait(500)
            script.game_loop_handler()
    else:
        game_engine.init()
        game_engine.start()
        while True:
            game_engine.game_loop_handler()
        
=======

def main():
    coloredlogs.install(level='DEBUG')
    
    game_engine.init()
    game_engine.start() # and script.start() is the same
    # script.start()

    while True:
        game_engine.game_loop_handler()
        # if script.has_changed():
        #     pygame.time.wait(100)
        # script.game_loop_handler()
>>>>>>> origin/main

    # run it if you need to check functionality fast and it doesn't depends on pygame initialization.
    # Make sure to comment game_engine.init() and script.start() and the rest related to game_engine and script.
    # utils_test.run_tests()


if __name__ == '__main__':
    main()
