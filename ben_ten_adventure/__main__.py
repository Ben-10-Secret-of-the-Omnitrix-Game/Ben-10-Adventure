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
    logger = logging.getLogger(__name__)
    coloredlogs.install(level='DEBUG', logger=logger)
    # game_engine.start()
    utils_test.run_tests()
    
