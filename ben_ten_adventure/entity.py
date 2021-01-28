import pygame
from random import randint
from .graphics import RenderPlayer, RenderNPC
from .weapon import BaseWeapon


class BaseEntity(pygame.sprite.Sprite):
    """
    What is Entity?
    Entity is everything that implies life creature or in simple words everything that's alive

    It's a base class of Entity

    I need my own entity, what should I do?
        1. define class named by this rules:
            Your class name end with "Entity" (case sensetive)
        2. inherit your class from BaseEntity whenever your entity is!
        3. Extend functionality

    id is unique - for PLayer it's name

    """
    def __init__(self, x, y, id, speed=3):
        # pygame.sprite.Sprite.__init__(self)
        super().__init__()
        """
        x and y - entity current position
        skin - image of entity. Instance of pygame.Surface
        """
        self.x = x
        self.y = y
        self.id = id
        self.rotation = 0
        self._direction_map = {
            (1, 0, 0, 0): [{'dx': 0, 'dy': -1}, 2],
            (0, 1, 0, 0): [{'dx': 0, 'dy': 1}, 4],
            (0, 0, 1, 0): [{'dx': 1, 'dy': 0}, 1],
            (0, 0, 0, 1): [{'dx': -1, 'dy': 0}, 3],
            (1, 0, 1, 0): [{'dx': 1, 'dy': -1}, 1],
            (0, 1, 0, 1): [{'dx': -1, 'dy': 1}, 4],
            (0, 1, 1, 0): [{'dx': 1, 'dy': 1}, 1],
            (1, 0, 0, 1): [{'dx': -1, 'dy': -1}, 3]
        }
        self.speed = speed

        from .manager import ALL_ENTITIES
        ALL_ENTITIES.add_entity(self)

    def __str__(self):
        return f'{self.__class__.__name__} {self.id}'

    def __repr__(self):
        return self.__str__()

    def _move(self, keys_states, speed=None):
        if speed is None:
            speed = self.speed
        try:
            direction = self._direction_map[keys_states]
            self.x = self.x + (direction[0]['dx'] * speed)
            self.y = self.y + (direction[0]['dy'] * speed)
            self.rotation = direction[1] - 1
        except KeyError:
            pass

    def cartesian_to_isometric(self, cart_x, cart_y):
        isometric_x = (cart_x - cart_y)
        isometric_y = (cart_x + cart_y) / 2
        return isometric_x, isometric_y

    def render(self):
        pass
    
    def is_near(self, entity):
        radius = 50
        return ((self.x - entity.x) ** 2 + (self.y - entity.y) ** 2) ** 0.5 < radius


class Player(BaseEntity):
    """
    In singleplayer:
        Player is main adventurer. Trying to pass the game till the end
    In multiplayer:
        There are a lot of Players surronding you and bumbling around.

    """

    def __init__(self, name, image=None, hp=200, x=0, y=0, speed=1):
        super().__init__(x, y, name, speed)
        """
        x, y - coords
        image is a list of Tiles
        """
        self.image = image
        if image:
            self.texture = image[self.rotation]
        self.id = name
        self.x = x
        self.y = y
        self.width, self.height = self.texture.get_size()
        self._render = RenderPlayer(self)
        self.hp = hp

        self.friends = [self.id]
        self.friends_ids = []

        self.weapon = None
        self.damage = 20
        self.attack_pause = 10
        self.current_tick = self.attack_pause

    def move(self, keys_states, speed=None):
        from .manager import ALL_ENTITIES
        if speed is None:
            speed = self.speed
        try:
            direction = self._direction_map[keys_states]
            self.x = self.x + (direction[0]['dx'] * speed)
            self.y = self.y + (direction[0]['dy'] * speed)
            if ALL_ENTITIES.is_collision(self):
                self.x = self.x - (direction[0]['dx'] * speed)
                self.y = self.y - (direction[0]['dy'] * speed)
            self.rotation = direction[1] - 1
            self.texture = self.image[self.rotation]
        except KeyError:
            pass

    def render(self, screen=None, border_offset=[500, 100]):
        if self.current_tick < self.attack_pause:
            self.current_tick += 1
        self._render.render_isometric_player(screen, border_offset)

    def is_attacked(self):
        self._render.is_attacked()
        if self.hp <= 0:
            from .manager import ALL_ENTITIES
            ALL_ENTITIES.remove(self)

    def get_rect(self):
        return self.texture.get_rect()

    def set_friends(self, *args):
        for friend in args:
            self.friends.append(friend)
            self.friends_ids.append(friend.id)

    def set_weapon(self, weapon):
        self.weapon = weapon

    def attack(self):
        from .manager import ALL_ENTITIES

        if self.weapon is None:
            damage = self.damage
            radius = 40
        else:
            damage = self.weapon.damage
            radius = self.weapon.radius
        if self.current_tick == self.attack_pause:
            for npc in ALL_ENTITIES.get_list():
                if npc.id not in self.friends:
                    if ((self.x - npc.x) ** 2 + (self.y - npc.y) ** 2) ** 0.5 <= radius and npc.hp > 0:
                        npc.hp -= damage
                        npc.is_attacked()
                        self.current_tick = 0
                        break

    

class NPC(BaseEntity):
    """
    NPC -   all "zombie" like entities. 
    E.g. "players"(not exactly) that's attacking Player(main adventurer, see above).
    How to know is it NPC?
        * no one control it with keyboard, mouse, any other stuff.
        * has primitive actions, generally it's stupid AI or hardcoded actions.

    id is made for comparing different NPCs and preventing their collision
    id is unique, usually it's a Number(1, 3, 10, NPC2) or a Name (f.e. Vilgax)
    """

    def __init__(self, id, image=None, hp=100, x=0, y=0, speed=1):
        super().__init__(x, y, id, speed)
        self.weapon = None
        self.id = id
        self.image = image
        if image:
            self.texture = image[self.rotation]
        self.x = x
        self.y = y
        self.width, self.height = self.texture.get_size()
        self._render = RenderNPC(self)
        self.hp = hp
        self.attack_pause = 40
        self.current_tick = self.attack_pause

        """if there is no weapon, NPC will try to kill player without it"""
        self.damage = 20

        self.dest_complete = True
        self.dest_x = 0
        self.dest_y = 0

    def render(self, screen=None, border_offset=[500, 100]):
        if self.current_tick < self.attack_pause:
            self.current_tick += 1
        self._render.render_isometric_npc(screen, border_offset)

    def update(self):
        self.x += self.speed
        self.y += self.speed

    def set_weapon(self, weapon):
        self.weapon = weapon

    def go_to(self, player):
        from .manager import ALL_ENTITIES

        rot_x, rot_y = 0, 0

        if self.speed > abs(self.x - player.x):
            self.x = player.x
        elif self.x != player.x:
            if self.x > player.x:
                self.x -= self.speed
                rot_x = -1
            else:
                self.x += self.speed
                rot_x = 1
        if self.speed > abs(self.y - player.y):
            self.y = player.y
        elif self.y != player.y:
            if self.y > player.y:
                self.y -= self.speed
                rot_y = -1
            else:
                self.y += self.speed
                rot_y = 1
        if ALL_ENTITIES.is_collision(self):
            self.x -= self.speed * rot_x
            self.y -= self.speed * rot_y
        else:
            """changing texture rotation"""

            if rot_x == rot_y == 1:
                self.rotation = 0
            elif rot_x == rot_y == -1:
                self.rotation = 2
            elif rot_x == 1 and rot_y == -1:
                self.rotation = 1
            elif rot_x == -1 and rot_y == 1:
                self.rotation = 3
            elif rot_x == -1 and rot_y == 0:
                self.rotation = 2
            elif rot_x == 1 and rot_y == 0:
                self.rotation = 0
            elif rot_y == 1 and rot_x == 0:
                self.rotation = 3
            else:
                self.rotation = 1

            if self.image and len(self.image) >= self.rotation + 1:
                self.texture = self.image[self.rotation]

    def is_attacked(self):
        self._render.is_attacked()
        if self.hp <= 0:
            from .manager import ALL_ENTITIES
            ALL_ENTITIES.remove(self)
            print(ALL_ENTITIES.get_list())

    def attack(self, player):
        if self.weapon == None:
            damage = self.damage
            radius = 40
        else:
            damage = self.weapon.damage
            radius = self.weapon.radius
        if self.current_tick == self.attack_pause and player.hp > 0:
            if ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5 <= radius:
                player.hp -= damage
                player.is_attacked()
                self.current_tick = 0
                
    def get_rect(self):
        return self.texture.get_rect()

    def random_move(self, tile_size=128, map_width=10, map_height=10, border_offset=[500, 100]):
        """randomly calculating a point on the map
            and going to it"""

        from .manager import ALL_ENTITIES

        rot_x = 0
        rot_y = 0

        if self.dest_complete:
            self.dest_x = randint(0, map_width * tile_size // 2)
            self.dest_y = randint(0, map_height * tile_size // 2)
            self.dest_complete = False

        if (self.x, self.y) == (self.dest_x, self.dest_y):
            self.dest_complete = True
        else:
            if self.speed > abs(self.x - self.dest_x):
                self.x = self.dest_x
            elif self.x != self.dest_x:
                if self.x > self.dest_x:
                    self.x -= self.speed
                    rot_x = -1
                else:
                    self.x += self.speed
                    rot_x = 1
            if self.speed > abs(self.y - self.dest_y):
                self.y = self.dest_y
            elif self.y != self.dest_y:
                if self.y > self.dest_y:
                    self.y -= self.speed
                    rot_y = -1
                else:
                    self.y += self.speed
                    rot_y = 1
        if ALL_ENTITIES.is_collision(self):
            self.x -= self.speed * rot_x
            self.y -= self.speed * rot_y

            self.dest_x = randint(0, map_width * tile_size // 2)
            self.dest_y = randint(0, map_height * tile_size // 2)
        else:
            """changing texture rotation"""

            if rot_x == rot_y == 1:
                self.rotation = 0
            elif rot_x == rot_y == -1:
                self.rotation = 2
            elif rot_x == 1 and rot_y == -1:
                self.rotation = 1
            elif rot_x == -1 and rot_y == 1:
                self.rotation = 3
            elif rot_x == -1 and rot_y == 0:
                self.rotation = 2
            elif rot_x == 1 and rot_y == 0:
                self.rotation = 0
            elif rot_y == 1 and rot_x == 0:
                self.rotation = 3
            else:
                self.rotation = 1

            if self.image and len(self.image) >= self.rotation + 1:
                self.texture = self.image[self.rotation]