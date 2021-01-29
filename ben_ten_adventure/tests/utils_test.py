from ben_ten_adventure.utils import GameAssets, init_resource_dirs
import logging


def test_init_resource_dirs():
    init_resource_dirs()


def test_GameAssets():
    ga = GameAssets()


def run_tests():
    test_init_resource_dirs()
    test_GameAssets()
    logging.info("Tests completed")
