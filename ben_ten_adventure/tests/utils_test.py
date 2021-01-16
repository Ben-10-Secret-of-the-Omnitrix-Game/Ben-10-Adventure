from ..utils import init_resource_dirs
import logging
import coloredlogs



def test_init_resource_dirs():
    init_resource_dirs()


def run_tests():
    logger = logging.getLogger(__name__)
    coloredlogs.install(level='DEBUG', logger=logger)
    
    test_init_resource_dirs()
    logger.info("Tests completed")    
