import pygame
import cv2
import numpy
import pytmx
import sys
import logging

from .utils import Config, GameAssets, Movie, DEFAULT_RESOURCES_PATH, Camera
from .scene import Scene
from .graphics import Tile, RenderEntities
from .entity import Player, NPC, BaseEntity
from .weapon import BaseWeapon

from os.path import join, split
from pygame.transform import scale
from random import randint

# Task related imports
from .schedulers import DelayedTask, RepeatingTask, Task
from queue import PriorityQueue


class EntityManager:
    """This class was created for searching for collisions
        All entities must be added to an object of EntityManager class
        The object of this class is single, it helps to manipulate Entities easily"""

    def __init__(self):
        self.entity_list = []
        self.id_list = []
        self.collision_radius = 40
        self._render = RenderEntities()
        self.kills = 0

    def add_entity(self, entity):
        if self.can_add(entity):
            self.entity_list.append(entity)
            self.id_list.append(entity.id)
        else:
            self.id_list.remove(entity.id)
            for i in range(len(self.entity_list)):
                if self.entity_list[i].id == entity.id:
                    self.entity_list.pop(i)
                    break
            self.add_entity(entity)

    def get_list(self):
        return self.entity_list

    def get_id_list(self):
        return self.id_list

    def remove(self, entity):
        if entity.id not in self.id_list:
            return
        self.kills += 1
        self.id_list.remove(entity.id)
        for i in range(len(self.entity_list)):
            if self.entity_list[i].id == entity.id:
                self.entity_list.pop(i)
                break

    def can_add(self, entity):
        if entity.id in self.id_list:
            return False
        return True

    def is_collision(self, entity):
        col_count = 0
        for ent in self.entity_list:
            if ent.id != entity.id:
                if ((ent.x - entity.x) ** 2 + (ent.y - entity.y) ** 2) ** 0.5 < self.collision_radius:
                    col_count += 1
        return col_count

    def is_collision_coord(self, x, y):
        col_count = 0
        for ent in self.entity_list:
            if ((ent.x - x) ** 2 + (ent.y - y) ** 2) ** 0.5 < self.collision_radius:
                col_count += 1
        return col_count

    def render(self, screen=None, border_offset=[500, 100]):
        self._render.render(self.entity_list, screen, border_offset)

    def clear(self):
        self.entity_list = []
        self.id_list = []
        self.kills = 0


class AdventureScene:
    PLAYING = 0
    END = 1
    """
    Base class for every adventure.
    * Any adventure must inherit be inherited from it.
    """
    pass


class AdventureManager:
    """
    Manages adventure list
    Has properties:
        name    -   somehow displayed name of adventure
        config  -   configuration file. Instance of ben_ten_adventure.utils.config.Config
                    Config should contain information about (asset files, ... will exand soon) 

        that's all by now
    """
    pass


class Game:
    DEBUG = bool
    RESOLUTION = tuple
    TILE_SIZE = int
    MAP_WIDTH = int
    MAP_HEIGHT = int
    ACTION = int
    TICK_EVENT_ID = int

    def __init__(self):
        self.ga: GameAssets
        self.screen: pygame.Surface
        # self.task_manager = object
        self.task_manager: TaskManager
        # self.adventure = object
        # self.config = object
        self.config: Config
        self.border_offset = int
        self.entity_manager: EntityManager
        self.start = False
        self.end = False


class SecretOfTheOmnitrix(AdventureScene):
    def __init__(self, game: Game):
        from .game_engine import Activity
        self.activity = Activity()
        self.game = game
        self.finishing = False
        self.stages = [
            self.play_scene_1,
            self.play_scene_2,
            self.play_scene_3,
            self.play_scene_4,
            self.play_scene_5,
            self.play_scene_6,
            self.play_scene_7]
        self._index = 0
        self.init_funcs = [
            self.init_scene_1,
            self.init_scene_2,
            self.init_scene_3,
            self.init_scene_4,
            self.init_scene_5,
            self.init_scene_6,
            self.init_scene_7]

        self.play_data = {}
        self.game.ACTION = self.activity.PLAYING

    def init_scene_1(self):
        kwargs = {}
        kwargs['intro'] = Movie(join(DEFAULT_RESOURCES_PATH, "videos", "intro.mp4"))
        return kwargs

    def play_scene_1(self, kwargs):
        """
        First video. 
        """
        self.handle_event(kwargs)
        if not kwargs['intro'].tick(self.game.screen):
            print("Video ended")
            self.game.screen.fill((0, 0, 0))
            text = ["Ben's Omnitrix is broken. You can't use your power",
                    "You've got to find Azimuth and prevent the Universe from detonation",
                    'Use:',
                    'SPACE to shoot',
                    'P for pause',
                    'arrows to move',
                    '(tap SPACE to play)',
                    '-> scene 1 - save Myaxx from prison']
            font = pygame.font.Font(None, 40)
            for i in text:
                phrase = font.render(i, True, (255, 100, 100))
                if text.index(i) == len(text) - 1:
                    font = pygame.font.SysFont('Calibri', 45, italic=True)
                    phrase = font.render(i, True, (100, 255, 100))
                self.game.screen.blit(phrase, (100, (text.index(i) + 2) * 50))
            pygame.display.flip()

            self.handle_event('start')
            if self.game.start:
                return self.END

    def init_scene_2(self):
        kwargs = {}
        kwargs['map'] = pytmx.TiledMap(join(DEFAULT_RESOURCES_PATH, "maps", "scene_1.tmx"))
        self.game.MAP_WIDTH, self.game.MAP_HEIGHT = kwargs['map'].width, kwargs['map'].height

        kwargs['myaxx'] = NPC('Myaxx', entity_manager=self.game.entity_manager, image=[self.game.ga.Myaxx_128_128],
                              hp=50, x=600, y=500, speed=5)
        kwargs['npcs_count'] = 24
        kwargs['npc_images'] = [self.game.ga.volann1_128_128, self.game.ga.volann1_128_128,
                                self.game.ga.volann2_128_128, self.game.ga.volann2_128_128]
        kwargs['npcs'] = []
        kwargs['npcs_random'] = []
        for i in range(0, kwargs['npcs_count'], 2):
            kwargs['npcs'] += [NPC(str(i), image=kwargs['npc_images'],
                                   x=randint(kwargs['myaxx'].x - 300, kwargs['myaxx'].x + 300),
                                   y=randint(kwargs['myaxx'].y - 300, kwargs['myaxx'].y + 300),
                                   entity_manager=self.game.entity_manager,
                                   speed=randint(2, 5))]
            kwargs['npcs_random'] += [NPC(str(i + 1), image=kwargs['npc_images'],
                                          x=randint(0, self.game.MAP_WIDTH * self.game.TILE_SIZE),
                                          y=randint(0, self.game.MAP_HEIGHT * self.game.TILE_SIZE),
                                          entity_manager=self.game.entity_manager,
                                          speed=randint(1, 3))]
        ben_images = [self.game.ga.ben10_1_128_128, self.game.ga.ben10_2_128_128,
                      self.game.ga.ben10_3_128_128, self.game.ga.ben10_4_128_128]
        kwargs['player'] = Player('Ben', entity_manager=self.game.entity_manager, image=ben_images, x=250, y=250,
                                  speed=15)
        kwargs['player'].set_friends(kwargs['myaxx'])

        kwargs['blaster'] = BaseWeapon(50, 100, 20)
        kwargs['player'].set_weapon(kwargs['blaster'])

        def myaxx_follow_player(custom_self, current_tick):
            if custom_self.player.is_near(custom_self.myaxx):
                self.play_data.update({'win': True})
            elif custom_self.player.hp <= 0:
                self.play_data.update({'win': False})
            if custom_self.player.id not in self.game.entity_manager.id_list:
                custom_self.is_canceled = True
                return

        def npcs_attack_player(custom_self, current_tick):
            for npc in custom_self.npcs:
                npc.go_to(custom_self.player)
                npc.attack(custom_self.player)
            # npc.random_move()
            if custom_self.player.id not in self.game.entity_manager.id_list:
                custom_self.is_canceled = True
                return

        def npcs_random_move(custom_self, current_tick):
            for npc in custom_self.npcs:
                npc.random_move()

        # def vilgax_attack_player(custom_self, current_tick):
        #     custom_self.vilgax.go_to(custom_self.player)
        #     custom_self.vilgax.attack(custom_self.player)
        #     if custom_self.player.id not in self.game.entity_manager.id_list:
        #         self.play_data.update({'win': False})

        self.game.task_manager.schedule_repeating_task({
            'myaxx': kwargs['myaxx'],
            'player': kwargs['player'],
            'on_run': myaxx_follow_player
        }, period=15)

        self.game.task_manager.schedule_repeating_task({
            'npcs': kwargs['npcs'],
            'player': kwargs['player'],
            'on_run': npcs_attack_player
        }, period=15)

        self.game.task_manager.schedule_repeating_task({
            'npcs': kwargs['npcs_random'],
            'on_run': npcs_random_move
        }, period=15)
        # self.game.task_manager.schedule_repeating_task({
        #     'vilgax': kwargs['vilgax'],
        #     'player': kwargs['player'],
        #     'on_run':  vilgax_attack_player
        # }, period=15)

        kwargs['camera'] = Camera()

        self.game.sql_data.player = 'Ben'
        self.game.sql_data.add_npc_count(kwargs['npcs_count'])
        self.game.sql_data.friends_count(len(kwargs['player'].friends_ids))
        self.game.sql_data.main_enemy = 'Vilgax'

        return kwargs

    def play_scene_2(self, kwargs):
        """
        Fight between Ben 10 and prisoners. Save Myaxx
        """
        if 'win' in kwargs:
            if kwargs['win']:
                self.game.sql_data.scenes_res[0] = 'Win'
            else:
                self.game.sql_data.save()
            return self.END

        self.render_map(kwargs)
        self.handle_event(kwargs)
        self.game.entity_manager.render(self.game.screen)
        while len(self.game.entity_manager.get_id_list()) < 20:
            kwargs['npcs_count'] += 2
            kwargs['npcs'] += [NPC(str(kwargs['npcs_count']), image=kwargs['npc_images'],
                                   x=randint(0, self.game.MAP_WIDTH * self.game.TILE_SIZE),
                                   y=randint(0, self.game.MAP_HEIGHT * self.game.TILE_SIZE),
                                   entity_manager=self.game.entity_manager,
                                   speed=randint(1, 3))]
            kwargs['npcs_random'] += [NPC(str(kwargs['npcs_count'] - 1), image=kwargs['npc_images'],
                                          x=randint(0, self.game.MAP_WIDTH * self.game.TILE_SIZE),
                                          y=randint(0, self.game.MAP_HEIGHT * self.game.TILE_SIZE),
                                          entity_manager=self.game.entity_manager,
                                          speed=randint(1, 3))]


    def init_scene_3(self):
        kwargs = {}
        kwargs['from_prison'] = Movie(join(DEFAULT_RESOURCES_PATH, "videos", "vilgax_ready.mp4"))
        return kwargs

    def play_scene_3(self, kwargs):
        """
        Flying to Azmuth's planet
        """
        self.handle_event(kwargs)
        if not kwargs['from_prison'].tick(self.game.screen):
            print("Video ended")
            self.game.start = False
            self.game.screen.fill((0, 0, 0))
            text = ["You're in a right way! You've saved Myaxx",
                    "You've got to fight Vilgax, or he will kill destroy your ship",
                    'Find Azimuth and save Omnitrix than,',
                    'To fight with Vilgax you need to kill 10 of his drones',
                    '(tap SPACE to play)',
                    '-> scene 2 - fight with Vilgax']
            font = pygame.font.Font(None, 40)
            for i in text:
                phrase = font.render(i, True, (255, 100, 100))
                if text.index(i) == len(text) - 1:
                    font = pygame.font.SysFont('Calibri', 45, italic=True)
                    phrase = font.render(i, True, (100, 255, 100))
                self.game.screen.blit(phrase, (100, (text.index(i) + 2) * 50))
            pygame.display.flip()

            self.handle_event('start')
            if self.game.start:
                return self.END

    def init_scene_4(self):
        kwargs = {}
        kwargs['map'] = pytmx.TiledMap(join(DEFAULT_RESOURCES_PATH, "maps", "scene_2.tmx"))
        self.game.MAP_WIDTH, self.game.MAP_HEIGHT = kwargs['map'].width, kwargs['map'].height

        kwargs['vilgax'] = NPC('Vilgax', entity_manager=self.game.entity_manager,
                               image=[self.game.ga.Vilgax1_128_128, self.game.ga.Vilgax1_128_128,
                                      self.game.ga.Vilgax2_128_128, self.game.ga.Vilgax2_128_128],
                               hp=500, x=200, y=0, speed=5)
        weapon = BaseWeapon(30, 80, 40)
        kwargs['vilgax'].set_weapon(weapon)
        kwargs['vilgax'].unattackable = True
        kwargs['npcs_count'] = 25
        kwargs['npc_images'] = [self.game.ga.Drone1_128_128, self.game.ga.Drone1_128_128,
                                self.game.ga.Drone2_128_128, self.game.ga.Drone2_128_128]
        kwargs['npcs'] = []
        for i in range(0, kwargs['npcs_count']):
            kwargs['npcs'] += [NPC(str(i), image=kwargs['npc_images'],
                                   x=randint(kwargs['vilgax'].x - 500, kwargs['vilgax'].x + 500),
                                   y=randint(kwargs['vilgax'].y - 500, kwargs['vilgax'].y + 500),
                                   entity_manager=self.game.entity_manager,
                                   speed=randint(1, 3))]

        ben_images = [self.game.ga.ben10_1_128_128, self.game.ga.ben10_2_128_128,
                      self.game.ga.ben10_3_128_128, self.game.ga.ben10_4_128_128]
        kwargs['player'] = Player('Ben', entity_manager=self.game.entity_manager, image=ben_images, x=250, y=250,
                                  speed=15)

        kwargs['blaster'] = BaseWeapon(50, 120, 20)
        kwargs['player'].set_weapon(kwargs['blaster'])

        kwargs['base_enitity'] = BaseEntity(1000, 1000, 'Base', entity_manager=self.game.entity_manager)

        def npcs_attack_player(custom_self, current_tick):
            for npc in custom_self.npcs:
                if custom_self.vilgax.unattackable:
                    npc.go_to(custom_self.player)
                    npc.attack(custom_self.player)
                    # npc.random_move()
                else:
                    npc.go_to(custom_self.base_entity)

                if custom_self.player.hp <= 0:
                    self.play_data.update({'win': False})
                    custom_self.is_canceled = True

        def vilgax_attack_player(custom_self, current_tick):
            if not custom_self.vilgax.unattackable:
                custom_self.vilgax.go_to(custom_self.player)
                custom_self.vilgax.attack(custom_self.player)
                if custom_self.player.hp <= 0:
                    self.play_data['win'] = False
                    custom_self.is_canceled = True
                elif custom_self.vilgax.hp <= 0:
                    self.play_data['win'] = True

        self.game.task_manager.schedule_repeating_task({
            'npcs': kwargs['npcs'],
            'player': kwargs['player'],
            'vilgax': kwargs['vilgax'],
            'base_entity': kwargs['base_enitity'],
            'on_run': npcs_attack_player
        }, period=15)

        self.game.task_manager.schedule_repeating_task({
            'vilgax': kwargs['vilgax'],
            'player': kwargs['player'],
            'on_run': vilgax_attack_player
        }, period=15)

        kwargs['camera'] = Camera()

        self.game.sql_data.add_npc_count(kwargs['npcs_count'])

        return kwargs

    def play_scene_4(self, kwargs):
        """
        Fighting with Vilgax
        """
        if 'win' in kwargs:
            if kwargs['win']:
                self.game.sql_data.scenes_res[1] = 'Win'
            else:
                self.game.sql_data.save()
            return self.END
        self.handle_event(kwargs)
        self.render_map(kwargs)
        font = pygame.font.Font(None, 40)
        fps_value = str(self.game.entity_manager.kills)

        self.game.entity_manager.render(self.game.screen)
        fps_stat = font.render('KILLS: ' + fps_value, True, (0, 0, 255))
        self.game.screen.blit(fps_stat, (1000, 200))

        if self.game.entity_manager.kills >= 10:
            kwargs['vilgax'].unattackable = False

        if kwargs['vilgax'].hp <= 0:
            kwargs['win'] = True

        while len(self.game.entity_manager.get_id_list()) - 2 < 25:
            kwargs['npcs_count'] += 1
            kwargs['npcs'] += [NPC(str(kwargs['npcs_count']), image=kwargs['npc_images'],
                                   x=randint(0, self.game.MAP_WIDTH * self.game.TILE_SIZE),
                                   y=randint(0, self.game.MAP_HEIGHT * self.game.TILE_SIZE),
                                   entity_manager=self.game.entity_manager,
                                   speed=randint(1, 3))]

    def init_scene_5(self):
        kwargs = {}
        kwargs['flying'] = Movie(join(DEFAULT_RESOURCES_PATH, "videos", "flying2.mp4"))
        return kwargs

    def play_scene_5(self, kwargs):
        """
        flight to Zenon
        """
        self.handle_event(kwargs)
        if not kwargs['flying'].tick(self.game.screen):
            print("Video ended")
            self.game.start = False
            self.game.screen.fill((0, 0, 0))
            text = ["Vilgax has gone away, you are on the Zenon now",
                    "Your ship is broken, but Azimuth is near",
                    'Find Azimuth and be careful',
                    "Azimuth won't agree to fix Omnitrix, you've got to insist"
                    '(tap SPACE to play)',
                    '-> scene 3 - save Omnitrix']
            font = pygame.font.Font(None, 40)
            for i in text:
                phrase = font.render(i, True, (255, 100, 100))
                if text.index(i) == len(text) - 1:
                    font = pygame.font.SysFont('Calibri', 45, italic=True)
                    phrase = font.render(i, True, (100, 255, 100))
                self.game.screen.blit(phrase, (100, (text.index(i) + 2) * 50))
            pygame.display.flip()

            self.handle_event('start')
            if self.game.start:
                self.game.start = False
                return self.END

    def init_scene_6(self):
        kwargs = {}
        kwargs['map'] = pytmx.TiledMap(join(DEFAULT_RESOURCES_PATH, "maps", "scene_3_grass.tmx"))
        self.game.MAP_WIDTH, self.game.MAP_HEIGHT = kwargs['map'].width, kwargs['map'].height

        ben_images = [self.game.ga.ben10_1_128_128, self.game.ga.ben10_2_128_128,
                      self.game.ga.ben10_3_128_128, self.game.ga.ben10_4_128_128]
        kwargs['player'] = Player('Ben', entity_manager=self.game.entity_manager, image=ben_images, x=250, y=250,
                                  speed=15)
        azimuth_bio_images = [self.game.ga.Azimuth_Bio1_128_128, self.game.ga.Azimuth_Bio1_128_128,
                              self.game.ga.Azimuth_Bio2_128_128, self.game.ga.Azimuth_Bio2_128_128]
        kwargs['azimuth_images'] = [self.game.ga.Azimuth1_128_128, self.game.ga.Azimuth1_128_128,
                                    self.game.ga.Azimuth2_128_128, self.game.ga.Azimuth2_128_128]
        kwargs['azimuth'] = NPC('Azimuth', entity_manager=self.game.entity_manager, image=azimuth_bio_images, hp=300,
                                x=100, y=300, speed=3)
        kwargs['blaster'] = BaseWeapon(20, 120, 20)
        kwargs['player'].set_weapon(kwargs['blaster'])

        def check_azimuth(custom_self, current_tick):
            if custom_self.azimuth.hp <= 0:
                custom_self.azimuth = NPC('Azimuth', entity_manager=self.game.entity_manager,
                                          image=custom_self.new_images, hp=300,
                                          x=800, y=500, speed=1)
                custom_self.azimuth.unattackable = True
            if custom_self.azimuth.unattackable and not custom_self.azimuth.is_near(custom_self.player):
                custom_self.azimuth.go_to(custom_self.player)
            elif not custom_self.azimuth.unattackable and not custom_self.azimuth.is_near(custom_self.player):
                custom_self.azimuth.random_move()
            elif custom_self.azimuth.unattackable and custom_self.azimuth.is_near(custom_self.player):
                self.play_data['win'] = True
                custom_self.is_canceled = True

        self.game.task_manager.schedule_repeating_task({
            'new_images': kwargs['azimuth_images'],
            'azimuth': kwargs['azimuth'],
            'player': kwargs['player'],
            'on_run': check_azimuth
        }, period=15)

        kwargs['camera'] = Camera()

        self.play_data = kwargs
        return kwargs

    def play_scene_6(self, kwargs):
        self.handle_event(kwargs)
        self.render_map(kwargs)
        self.game.entity_manager.render(self.game.screen)
        if 'win' in self.play_data and self.play_data['win']:
            return self.END

    def init_scene_7(self):
        kwargs = {}
        kwargs['map'] = pytmx.TiledMap(join(DEFAULT_RESOURCES_PATH, "maps", "scene_3_sand.tmx"))
        self.game.MAP_WIDTH, self.game.MAP_HEIGHT = kwargs['map'].width, kwargs['map'].height
        kwargs['vilgax'] = NPC('Vilgax', entity_manager=self.game.entity_manager,
                               image=[self.game.ga.Vilgax1_128_128, self.game.ga.Vilgax1_128_128,
                                      self.game.ga.Vilgax2_128_128, self.game.ga.Vilgax2_128_128],
                               hp=500, x=200, y=0, speed=5)
        weapon = BaseWeapon(10, 80, 50)
        kwargs['vilgax'].set_weapon(weapon)
        ben_images = [self.game.ga.ben10_1_128_128, self.game.ga.ben10_2_128_128,
                      self.game.ga.ben10_3_128_128, self.game.ga.ben10_4_128_128]
        kwargs['player'] = Player('Ben', entity_manager=self.game.entity_manager, image=ben_images, x=250, y=250,
                                  speed=15)
        azimuth_bio_images = [self.game.ga.Azimuth1_128_128, self.game.ga.Azimuth1_128_128,
                              self.game.ga.Azimuth2_128_128, self.game.ga.Azimuth2_128_128]
        kwargs['azimuth_images'] = [self.game.ga.Azimuth1_128_128, self.game.ga.Azimuth1_128_128,
                                    self.game.ga.Azimuth2_128_128, self.game.ga.Azimuth2_128_128]
        kwargs['azimuth'] = NPC('Azimuth', entity_manager=self.game.entity_manager, image=azimuth_bio_images, hp=300,
                                x=100, y=300, speed=3)
        kwargs['player'].set_friends(kwargs['azimuth'])
        kwargs['bomb'] = BaseWeapon(80, 200, 20)
        kwargs['player'].set_weapon(kwargs['bomb'])
        kwargs['npcs_count'] = 25
        kwargs['npc_images'] = [self.game.ga.Drone1_128_128, self.game.ga.Drone1_128_128,
                                self.game.ga.Drone2_128_128, self.game.ga.Drone2_128_128]
        kwargs['npcs'] = []
        for i in range(0, kwargs['npcs_count']):
            kwargs['npcs'] += [NPC(str(i), image=kwargs['npc_images'],
                                   x=randint(kwargs['vilgax'].x - 500, kwargs['vilgax'].x + 500),
                                   y=randint(kwargs['vilgax'].y - 500, kwargs['vilgax'].y + 500),
                                   entity_manager=self.game.entity_manager,
                                   speed=randint(1, 3))]

        def vilgax_attack_player(custom_self, current_tick):
            custom_self.vilgax.go_to(custom_self.player)
            custom_self.vilgax.attack(custom_self.player)
            if custom_self.player.hp <= 0:
                self.play_data['win'] = False
                custom_self.is_canceled = True
            elif custom_self.vilgax.hp <= 0:
                self.play_data['win'] = True
                custom_self.is_canceled = True

        self.game.task_manager.schedule_repeating_task({
            'vilgax': kwargs['vilgax'],
            'player': kwargs['player'],
            'on_run': vilgax_attack_player
        }, period=15)

        def npcs_attack_player(custom_self, current_tick):
            for npc in custom_self.npcs:
                npc.go_to(custom_self.player)
                npc.attack(custom_self.player)
                # npc.random_move()
            if custom_self.player.hp <= 0:
                self.play_data.update({'win': False})
                custom_self.is_canceled = True
                return
            if 'win' in self.play_data:
                custom_self.is_canceled = True
                return

        self.game.task_manager.schedule_repeating_task({
            'npcs': kwargs['npcs'],
            'player': kwargs['player'],
            'vilgax': kwargs['vilgax'],
            'on_run': npcs_attack_player
        }, period=15)

        self.play_data = kwargs
        return kwargs

    def play_scene_7(self, kwargs):
        self.handle_event(kwargs)
        self.render_map(kwargs)
        self.game.entity_manager.render(self.game.screen)
        if 'win' in self.play_data:
            if self.play_data['win']:
                self.game.sql_data.scenes_res[2] = 'Win'
            self.game.sql_data.save()
            return self.END

    def play_current(self):
        if self.game.ACTION != self.activity.PAUSE:
            if not self.play_data:
                print(self._index)
                initialization_function = self.init_funcs[self._index]
                self.play_data = initialization_function()

            stage = self.stages[self._index]
            print(self.play_data)
            if 'win' in self.play_data:
                print(self._index)
            if stage(kwargs=self.play_data) == self.END:
                # print('win' in self.play_data)
                if 'win' in self.play_data and not self.play_data['win']:
                    self._index = 1
                    self.game.entity_manager.clear()
                    initialization_function = self.init_funcs[self._index]
                    self.play_data = initialization_function()

                elif self._index + 1 < len(self.stages):
                    self._index += 1
                    self.game.entity_manager.clear()
                    initialization_function = self.init_funcs[self._index]
                    self.play_data = initialization_function()
                else:
                    self.finishing = True
                    self.game.end = False
                    self.game.screen.fill((0, 0, 0))
                    text = ["You win!",
                            "Introduction:",
                            "Earth is in danger",
                            "Luckly you've got a chance to choose what really mean to you",
                            "What will you choose - a life of your loved one or to save entire humanity from extinction?",
                            'tap L or O for Life or Omnitrix']
                    font = pygame.font.Font(None, 40)
                    self.game.screen.blit(self.game.ga.Omnitrix, (300, 300))
                    self.game.screen.blit(self.game.ga.Azimuth2_128_128, (900, 200))
                    for i in text:
                        phrase = font.render(i, True, (255, 100, 100))
                        if text.index(i) == len(text) - 1:
                            font = pygame.font.SysFont('Calibri', 45, italic=True)
                            phrase = font.render(i, True, (100, 255, 100))
                        self.game.screen.blit(phrase, (100, (text.index(i) + 2) * 50))
                    pygame.display.flip()

                    self.handle_event('end')
        else:
            pygame.mixer.music.pause()
            self.handle_event('pause')
            font = pygame.font.Font(None, 50)
            text = font.render('To continue press P', True, (100, 255, 100))
            self.game.screen.blit(text, (640, 500))

    def render_map(self, kwargs):
        for layer in kwargs['map'].layers:
            for x, y, image in layer.tiles():
                file_name = split(image[0])[-1]
                asset_name = file_name.split('.')[0]
                tile_size = self.game.TILE_SIZE
                border_offset = (abs(self.game.RESOLUTION[0] - tile_size * self.game.MAP_WIDTH) // 2 - tile_size // 2,
                                 -self.game.MAP_HEIGHT // 2 * tile_size // 2 + self.game.RESOLUTION[1] // 2)
                tile = Tile(x, y, border_offset, image=getattr(self.game.ga, asset_name), tile_size=tile_size)
                tile.render_isometric_tile(self.game.screen)

    def handle_event(self, kwargs):
        for event in pygame.event.get():
            if kwargs == 'start':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.game.start = True
            elif kwargs == 'end':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        text = ["Then...",
                                "You're very a kind and honest person,",
                                "Share your love and tenderness with others on Earth!"
                                ]
                        font = pygame.font.SysFont('Calibri', 30)
                        for i in text:
                            phrase = font.render(i, True, (100, 100, 255))
                            self.game.screen.blit(phrase, (650, 400 + (text.index(i)) * 50))
                        pygame.display.flip()
                        pygame.time.wait(8000)
                        sys.exit()
                    elif event.key == pygame.K_o:
                        text = ["Then...",
                                "You're a very strong and cold-blooded person,",
                                "You're born to be a hero",
                                'You are worthy to own Omnitrix!']
                        font = pygame.font.SysFont('Calibri', 30)
                        for i in text:
                            phrase = font.render(i, True, (100, 100, 255))
                            self.game.screen.blit(phrase, (650, 400 + (text.index(i)) * 50))
                        pygame.display.flip()
                        pygame.time.wait(8000)
                        sys.exit()
            else:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEOEXPOSE:  # handles window minimising/maximising
                    self.game.screen.blit(scale(
                        self.game.screen, self.game.screen.get_size()), (0, 0))
                    pygame.display.update()
                    # border_offset = self.game.screen.get_width() - TILE_SIZE[0] * MAP_WIDTH
                elif event.type == pygame.MOUSEMOTION:
                    mouse_x_y = pygame.mouse.get_pos()
                elif event.type == pygame.KEYDOWN:
                    if kwargs != 'pause':
                        btns_pressed = tuple(pygame.key.get_pressed())[79:83]
                        if kwargs and 'player' in kwargs:
                            kwargs['player'].move(btns_pressed)

                        if event.key == pygame.K_SPACE:
                            try:
                                kwargs['player'].attack()
                            except KeyError:
                                pass
                    if event.key == pygame.K_p:
                        if self.game.ACTION == self.activity.PAUSE:
                            self.game.ACTION = self.activity.PLAYING
                        elif self._index not in [0, 2, 4]:
                            self.game.ACTION = self.activity.PAUSE
                elif event.type == self.game.TICK_EVENT_ID:
                    if self.game.ACTION != self.activity.PAUSE:
                        self.game.task_manager.tick()


class TaskManager:
    def __init__(self):
        self.queue = PriorityQueue()
        self.tasks = {}

        self.current_tick = 0
        self.id = -1

    def schedule_repeating_task(self, task_data, period=20):
        """
        task_data: dict with params and functions
        period: int value in ticks (20 ticks = 1 second)
        """
        task_class = type("AutoCreatedRepeatingTask", (RepeatingTask, object), task_data)
        self.add_task(task_class(period))

    def schedule_delayed_task(self, task_data, delay=20):
        """
        task_data: dict with params and functions
        delay: int value in ticks (20 ticks = 1 second)
        """
        task_class = type("AutoCreatedDelayedTask", (RepeatingTask, object), task_data)
        self.add_task(task_class(delay))

    def schedule_delayed_repeating_task(self, task_data: dict, delay=20, period=20):
        """
        task_data: dict with params and functions
        delay: int value in ticks (20 ticks = 1 second)
        period: int value in ticks (20 ticks = 1 second)
        
        check out help(schedulers.DelayedRepeatingTask) for more information
        """
        task_class = type("AutoCreatedDelayedRepeatingTask", (RepeatingTask, object), task_data)
        self.add_task(task_class(delay, period))

    def add_task(self, task):
        assert isinstance(task, Task), "You're only allowed to schedule tasks inhereted from Task class"
        if task.is_repeating:
            if task.period <= 0:
                task.period = 1
        elif task.is_delayed:
            if task.delay <= 0:
                task.delay = 1
        elif task.is_delayed_repeating:
            if task.period <= 0:
                task.period = 1
            if task.delay <= 0:
                task.delay = 1

        self.handle(task)

    def handle(self, task):
        next_run = 0
        if task.is_repeating:
            next_run = self.current_tick + task.period
        elif task.is_delayed or task.is_delayed_repeating:
            next_run = self.current_tick + task.delay
        assert next_run != 0, "Something went wrong when scheduling next run of the Task." + str(task)

        self.id += 1

        task.id = self.id
        self.tasks[self.id] = task
        # TODO replace id(task) with priority of Tasks
        self.queue.put((next_run, id(task), task))

    def tick(self):

        self.current_tick += 1
        if self.queue.empty():
            return
        next_run, obj_id, task = self.queue.get()

        # delete if task is canceled
        if task.is_canceled:
            del self.tasks[task.id]
            task.on_cancel()
            return

        if task.is_repeating:
            next_run = self.current_tick + task.period
            # TODO replace id(task) with priority of Tasks
            self.queue.put((next_run, id(task), task))
            task.on_run(self.current_tick)
        elif task.is_delayed:
            task.is_canceled = True
            task.on_run(self.current_tick)
        elif task.is_delayed_repeating:
            next_run = self.current_tick + task.period
            # TODO replace id(task) with priority of Tasks
            self.queue.put((next_run, id(task), task))
            task.on_run(self.current_tick)

    def shutdown(self):
        if not self.queue.is_empty():
            self.queue.join()
        if self.tasks:
            for task in self.tasks:
                task.on_cancel()
                task.is_canceled = True
            self.tasks = []
        self.id = -1
