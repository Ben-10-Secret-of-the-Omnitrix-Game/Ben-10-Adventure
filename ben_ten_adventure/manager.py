import pygame
import cv2
import numpy
import pytmx
import sys
import logging

from .utils import Config, GameAssets, Movie, DEFAULT_RESOURCES_PATH, Camera
from .scene import Scene
from .graphics import Tile, RenderEntities
from .entity import Player, NPC
from .weapon import BaseWeapon

from os.path import join, split
from pygame.transform import scale
from random import randint

# Task related imports
from .schedulers import DelayedTask, RepeatingTask, Task
from queue import PriorityQueue

MAP_WIDTH, MAP_HEIGHT, TILE_SIZE = 10, 10, 128
PAUSE_GAME = False


class EntityManager:
    """This class was created for searching for collisions
        All entities must be added to an object of EntityManager class
        The object of this class is single, it helps to manipulate Entities easily"""

    def __init__(self):
        self.entity_list = []
        self.id_list = []
        self.collision_radius = 30
        self._render = RenderEntities()

    def add_entity(self, entity):
        if self.can_add(entity):
            self.entity_list.append(entity)
            self.id_list.append(entity.id)

    def get_list(self):
        return self.entity_list

    def get_id_list(self):
        return self.id_list

    def remove(self, entity):
        if entity.id not in self.id_list:
            return
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
        for ent in self.entity_list:
            if ent.id != entity.id:
                if ((ent.x - entity.x) ** 2 + (ent.y - entity.y) ** 2) ** 0.5 < self.collision_radius:
                    return True
        return False

    def render(self, screen=None, border_offset=[500, 100]):
        self._render.render(self.entity_list, screen, border_offset)


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


class SecretOfTheOmnitrix(AdventureScene):
    def __init__(self, game: Game):
        self.game = game
        self.stages = [
            self.play_scene_1,
            self.play_scene_2,
            self.play_scene_3,
            self.play_scene_4,
            self.play_scene_5]
        self._index = 1
        self.init_funcs = [
            self.init_scene_1,
            self.init_scene_2,
            self.init_scene_2,
            self.init_scene_3,
            self.init_scene_4,
            self.init_scene_5]

        self.play_data = {}
        self.game.ACTION = self.activity.PLAYING

    def init_scene_1(self):
        kwargs = {}
        kwargs['intro'] = Movie(join(DEFAULT_RESOURCES_PATH, "videos", "ben_10_test2.mp4"))
        return kwargs

    def play_scene_1(self, kwargs):
        """
        First video. 
        """
        self.handle_event(kwargs)
        if not kwargs['intro'].tick(self.game.screen):
            print("Video ended")
            return self.END

    def init_scene_2(self):
        kwargs = {}
        kwargs['map'] = pytmx.TiledMap(join(DEFAULT_RESOURCES_PATH, "maps", "scene_1.tmx"))
        npc_images = [self.game.ga.ben10_1_128_128, self.game.ga.ben10_2_128_128,
                      self.game.ga.ben10_3_128_128, self.game.ga.ben10_4_128_128]
        kwargs['npcs'] = [NPC(str(i + 1), image=npc_images,
                              x=randint(0, MAP_WIDTH * TILE_SIZE // 2),
                              y=randint(0, MAP_HEIGHT * TILE_SIZE // 2),
                              entity_manager=self.game.entity_manager,
                              speed=randint(1, 3)) for i in range(5)]
        ben_images = [self.game.ga.ben10_1_128_128, self.game.ga.ben10_2_128_128,
                      self.game.ga.ben10_3_128_128, self.game.ga.ben10_4_128_128]
        kwargs['player'] = Player('Ben', entity_manager=self.game.entity_manager, image=ben_images, x=250, y=250, speed=15)
        kwargs['myaxx'] = NPC('Myaxx', entity_manager=self.game.entity_manager, image=[self.game.ga.Myaxx_ov_render], hp=50, x=600, y=500, speed=5)
        kwargs['player'].set_friends(kwargs['myaxx'])
        kwargs['vilgax'] = NPC('Vilgax', image=[self.game.ga.Alien_V_128_128], entity_manager=self.game.entity_manager, hp=250, x=700, y=600, speed=5)
        kwargs['vilgax'].attack_pause = 40
        kwargs['vilgax'].damage = 100
        kwargs['player'].set_friends(kwargs['myaxx'])

        kwargs['atom_fn_bomb'] = BaseWeapon(180, 1000, 50)
        kwargs['player'].set_weapon(kwargs['atom_fn_bomb'])

        def myaxx_follow_player(custom_self, current_tick):
            if custom_self.player.is_near(custom_self.myaxx):
                self.game.sql_data.scenes_res[0] = 'Win'
                # self.game.sql_data.save()
                self.play_data.update({"win": True})
                print("WIN")
            
        
        def npcs_attack_player(custom_self, current_tick):
            for npc in custom_self.npcs:
                npc.go_to(custom_self.player)
                npc.attack(custom_self.player)
                npc.random_move()
        
        def vilgax_attack_player(custom_self, current_tick):
            custom_self.vilgax.go_to(custom_self.player)
            custom_self.vilgax.attack(custom_self.player)
            if kwargs['player'].id not in self.game.entity_manager.get_id_list():
                self.play_data.update({"win": False})
                # return self.END
        
        self.game.task_manager.schedule_repeating_task({
            'myaxx': kwargs['myaxx'],
            'player': kwargs['player'],
            'on_run': myaxx_follow_player
            }, period=15)
        
        self.game.task_manager.schedule_repeating_task({
            'npcs': kwargs['npcs'],
            'player': kwargs['player'],
            'on_run':  npcs_attack_player
        }, period=15)
        
        self.game.task_manager.schedule_repeating_task({
            'vilgax': kwargs['vilgax'],
            'player': kwargs['player'],
            'on_run':  vilgax_attack_player
        }, period=15)
        # self.game.task_manager.schedule_repeating_task({
        #     "kwargs": kwargs,
        #     "on_run": lambda custom_self, current_tick: self.render_map(custom_self.kwargs)
        # }, period=1)

        kwargs['camera'] = Camera()

        self.game.sql_data.player = 'Ben'
        self.game.sql_data.add_npc_count(len(self.game.entity_manager.get_list()) - 1)
        self.game.sql_data.friends_count(len(kwargs['player'].friends_ids))
        self.game.sql_data.main_enemy = 'Vilgaxx'

        return kwargs

    def play_scene_2(self, kwargs):
        """
        Fight between Ben 10 and prisoners. Save Myaxx
        """
        self.handle_event(kwargs)
        if 'win' in self.play_data:
            return self.END
        
        self.old_render_map()
        start_time = pygame.time.get_ticks()
        # self.render_map(kwargs)
        self.game.entity_manager.render(self.game.screen)
        time_since_enter = pygame.time.get_ticks() - start_time
        message = 'Milliseconds since enter: ' + str(time_since_enter)
        logging.info(message)
        
        # kwargs['vilgax'].go_to(kwargs['player'])
        # kwargs['vilgax'].attack(kwargs['player'])

        # if kwargs['player'].id not in self.game.entity_manager.get_id_list():
        #     self.play_data.update({"win": False})
        #     return self.END

        # if kwargs['player'].is_near(kwargs['myaxx']):
        #     self.play_data.update({'win': True})
        #     return self.END
        # for npc in kwargs['npcs']:
        #     npc.go_to(kwargs['player'])
        #     npc.attack(kwargs['player'])
            # npc.random_move()
        # kwargs['camera'].update(kwargs['player'])

    def init_scene_3(self):
        # kwargs
        pass

    def play_scene_3(self, kwargs):
        """
        Flying to Azmuth's planet
        """
        # self.handle_event(kwargs)
        # pygame.display.flip()
        pygame.time.wait(5000)
        sys.exit()

    def init_scene_4(self):
        pass

    def play_scene_4(self, kwargs):
        """
        Fighting with Vilgax
        """
        self.handle_event(kwargs)

    def init_scene_5(self):
        pass

    def play_scene_5(self, kwargs):
        """
        Urge Azmuth to keep omnitrix in Ben's hand.  
        """
        self.handle_event(kwargs)

    def play_current(self):
        global PAUSE_GAME
        if not PAUSE_GAME:
            if not self.play_data:
                initialization_function = self.init_funcs[self._index]
                self.play_data = initialization_function()

            stage = self.stages[self._index]
            if stage(kwargs=self.play_data) == self.END:
                if self._index + 1 < len(self.stages):
                    self._index += 1
                    initialization_function = self.init_funcs[self._index]
                    self.play_data.update(initialization_function())
                else:
                    # finish adventure
                    print("Finish")
        else:
            self.handle_event('pause')
            font = pygame.font.Font(None, 50)
            text = font.render('To continue press P', True, (100, 255, 100))
            self.game.screen.blit(text, (640, 500))

    def render_map(self, kwargs):
        for layer in kwargs['map'].layers:
            for x, y, image in layer.tiles():
                file_name = split(image[0])[-1]
                asset_name = file_name.split('.')[0]
                tile = Tile(x, y, (600, 100), image=getattr(self.game.ga, asset_name), tile_size=128)
                tile.render_isometric_tile(self.game.screen)
                self.dirty_rects.append((tile.iso_x, tile.iso_y, *tile.texture.get_rect()[2:]))
    
    def old_render_map(self):
        for row in range(0, 5):
            for col in range(0, 5):
                # tile = Tile(row, col, border_offset=self.game.border_offset,
                #                 image=scale(self.game.ga.wall_5_marine, (256, 256)), tile_size=256)
                tile = Tile(row, col, border_offset=self.game.border_offset,
                                image=self.game.ga.wall_5_marine, tile_size=128)
                # tile = Tile(row, col, border_offset=self.game.border_offset,
                #                 image=scale(self.game.ga.wall_5_marine, (64, 64)), tile_size=64)
                tile.render_isometric_tile(self.game.screen)

    def handle_event(self, kwargs):
        global PAUSE_GAME
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEOEXPOSE:  # handles window minimising/maximising
                self.game.screen.blit(scale(
                    self.game.screen, self.game.screen.get_size()), (0, 0))
                pygame.display.flip()
                # border_offset = self.game.screen.get_width() - TILE_SIZE[0] * MAP_WIDTH
            elif event.type == pygame.MOUSEMOTION:
                mouse_x_y = pygame.mouse.get_pos()
            elif event.type == pygame.KEYDOWN:
                if kwargs != 'pause':
                    btns_pressed = tuple(pygame.key.get_pressed())[79:83]
                    if 'player' in kwargs:
                        kwargs['player'].move(btns_pressed)

                    if event.key == pygame.K_SPACE:
                        kwargs['player'].attack()
                if event.key == pygame.K_p:
                    PAUSE_GAME = not PAUSE_GAME
            elif event.type == self.game.TICK_EVENT_ID:
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
            self.tasks = []
        self.id = -1
            
        
