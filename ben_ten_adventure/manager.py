import pygame
import cv2
import numpy
import pytmx
import sys

from .utils import Movie, DEFAULT_RESOURCES_PATH, Camera
from .scene import Scene
from .graphics import Tile, RenderEntities
from .entity import Player, NPC
from .weapon import BaseWeapon

from os.path import join, split
from pygame.transform import scale
from random import randint

# Task related imports
from .schedulers import RepeatingTask, Task
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
        self.ga = object
        self.screen = object
        self.task_manager = object
        # self.adventure = object
        self.config = object
        self.border_offset = int


class SecretOfTheOmnitrix(AdventureScene):
    def __init__(self, game: Game):
        self.game = game
        self.stages = [
            self.play_scene_1,
            self.play_scene_2,
            self.play_scene_3,
            self.play_scene_4,
            self.play_scene_5]
        self._index = 0
        self.init_funcs = [
            self.init_scene_1,
            self.init_scene_2,
            self.init_scene_2,
            self.init_scene_3,
            self.init_scene_4,
            self.init_scene_5]

        self.play_data = {}

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
        kwargs['npcs'] = [NPC(str(i + 1), npc_images,
                              x=randint(0, MAP_WIDTH * TILE_SIZE // 2),
                              y=randint(0, MAP_HEIGHT * TILE_SIZE // 2),
                              speed=randint(1, 3)) for i in range(5)]
        ben_images = [self.game.ga.ben10_1_128_128, self.game.ga.ben10_2_128_128,
                      self.game.ga.ben10_3_128_128, self.game.ga.ben10_4_128_128]
        kwargs['player'] = Player('Ben', ben_images, x=250, y=250, speed=15)
        kwargs['myaxx'] = NPC('Myaxx', image=[self.game.ga.Myaxx_ov_render], hp=50, x=600, y=500, speed=5)
        kwargs['player'].set_friends(kwargs['myaxx'])
        kwargs['vilgax'] = NPC('Vilgax', image=[self.game.ga.Alien_V_128_128], hp=250, x=700, y=600, speed=5)
        kwargs['player'].set_friends(kwargs['myaxx'])

        kwargs['atom_fn_bomb'] = BaseWeapon(180, 1000, 50)
        kwargs['player'].set_weapon(kwargs['atom_fn_bomb'])

        kwargs['camera'] = Camera()
        return kwargs

    def play_scene_2(self, kwargs):
        """
        Fight between Ben 10 and prisoners. Save Myaxx
        """

        self.render_map(kwargs)
        self.handle_event(kwargs)
        self.game.entity_manager.render(self.game.screen)
        kwargs['vilgax'].go_to(kwargs['player'])
        kwargs['vilgax'].attack(kwargs['player'])

        if kwargs['player'].id not in self.game.entity_manager.get_id_list():
            self.play_data.update({"win": False})
            return self.END

        if kwargs['player'].is_near(kwargs['myaxx']):
            self.play_data.update({'win': True})
            return self.END
        for npc in kwargs['npcs']:
            npc.go_to(kwargs['player'])
            npc.attack(kwargs['player'])
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
        if kwargs['win']:
            self.game.screen.blit(self.game.ga.win, self.game.border_offset)
        else:
            self.game.screen.blit(self.game.ga.game_over, self.game.border_offset)
        pygame.display.flip()
        pygame.time.wait(3000)
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

    def handle_event(self, kwargs):
        global PAUSE_GAME
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEOEXPOSE:  # handles window minimising/maximising
                # screen.fill((0, 0, 0))
                self.game.screen.blit(scale(
                    self.game.screen, self.game.screen.get_size()), (0, 0))
                pygame.display.update()
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
        self.queue.put((next_run, task))

    
    def tick(self):
        self.current_tick += 1
        if self.queue.empty():
            return
        task = self.queue.get()[1]
        
        # delete if is canceled
        if task.is_canceled:
            del self.tasks[task.id]
            task.on_cancel()
            
        if task.is_repeating:
            next_run = self.current_tick + task.period
            self.queue.put((next_run, task))
            task.on_run(self.current_tick)
        elif task.is_delayed:
            task.is_canceled = True
            task.on_run(self.current_tick)
        elif task.is_delayed_repeating:
            next_run = self.current_tick + task.period
            self.queue.put((next_run, task))
            task.on_run(self.current_tick)
    
    def shutdown(self):
        if not self.queue.is_empty():
            self.queue.join()
        if self.tasks:
            for task in self.tasks:
                task.on_cancel()
            self.tasks = []
        self.id = -1
            
        