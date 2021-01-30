import sqlite3
import pygame
from os.path import join


class SQLData:
    def __init__(self):
        self.fps = None
        self.npc_count = None
        self.players_friends_count = None
        self.scenes_res = [None, None, None]
        self.fps = []
        self.main_enemy = None

    def add_fps(self, fps):
        self.fps.append(fps)

    def average_fps(self):
        return sum(self.fps) / len(self.fps)

    def add_npc_count(self, npcs):
        self.npc_count += npcs


# class SQLSaver:
#     def __init__(self, file_path):
#         self.connection = sqlite3.connect(join('resources', 'sql_tables', file_path))
#
#     def save(self, sqldata: SQLData):
#         cur = self.connection.cursor()
#         enemy = cur.execute(f"""SELECT id FROM main_enemies
#                                     WHERE main_enemy = '{sqldata.main_enemy}'""").fetchall()[0][0]
#         results = [cur.execute(f"""SELECT id FROM algorithms
#                                     WHERE name = '{self.info_for_save[3]}'""").fetchall()[0][0]]
#         cur.execute(f"""INSERT INTO queries (text, color_theme, image, algorithm, fonts) VALUES
#                                 ('{self.info_for_save[0]}', {color},
#                                 {self.info_for_save[2]}, {al}, {len(self.font_list)})""")
#         self.connection.commit()
