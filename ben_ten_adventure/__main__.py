# add stuff to start
"""
finally should be like:


if __name__ == '__main__':
    engine.start()
"""
from . import game_engine
import logging
import coloredlogs

from .tests import utils_test

if __name__ == '__main__':
    coloredlogs.install(level='DEBUG')
    game_engine.start()
    utils_test.run_tests()
    
