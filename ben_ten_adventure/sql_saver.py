import sqlite3
import pygame
from os.path import join


class SQLData:
    def __init__(self):
        self.fps = []
        self.npc_count = 0
        self.players_friends_count = 0
        self.scenes_res = ['Game Over', 'Game Over', 'Game Over']
        self.fps = []
        self.main_enemy = None
        self.saver = SQLSaver('sql_game_data.db')
        self.player = None

    def add_fps(self, fps):
        self.fps.append(fps)

    def average_fps(self):
        return sum(self.fps) / len(self.fps)

    def add_npc_count(self, npcs):
        self.npc_count += npcs

    def friends_count(self, friends):
        self.players_friends_count += friends

    def save(self):
        self.saver.save(self)


class SQLSaver:
    def __init__(self, file_path):
        from .utils import DEFAULT_RESOURCES_PATH
        self.connection = sqlite3.connect(join(DEFAULT_RESOURCES_PATH, file_path))

    def save(self, sqldata):
        cur = self.connection.cursor()
        fps = round(sqldata.average_fps(), 1)
        try:
            enemy = cur.execute(f"""SELECT id FROM main_enemies
                                        WHERE main_enemy = '{sqldata.main_enemy}'""").fetchall()[0][0]
        except IndexError:
            cur.execute(f"""INSERT INTO main_enemies(main_enemy) VALUES ('{sqldata.main_enemy}')""")
            enemy = cur.execute(f"""SELECT id FROM main_enemies
                                                    WHERE main_enemy = '{sqldata.main_enemy}'""").fetchall()[0][0]
        results = [cur.execute(f"""SELECT id FROM scene_results
                                    WHERE scene_result = '{sqldata.scenes_res[i]}'""").fetchall()[0][0]
                   for i in range(3)]
        cur.execute(f"""INSERT INTO main (player, NPC_Count, player_friends_count, average_fps, scene1_result,
         scene2_result, scene3_result, main_enemy) VALUES
                                ('{sqldata.player}', {sqldata.npc_count}, {sqldata.players_friends_count},
                                {fps}, {results[0]}, {results[1]}, {results[2]}, {enemy})""")
        self.connection.commit()
