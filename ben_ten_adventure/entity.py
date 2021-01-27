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

    """
    def __init__(self, x, y, skin, speed=3):
        # pygame.sprite.Sprite.__init__(self)
        super().__init__()
        """
        x and y - entity current position
        skin - image of entity. Instance of pygame.Surface
        """
        self.x = x
        self.y = y
        self.skin = skin
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
        return (abs(self.x - entity.x) * 2 < 50) and (abs(self.y - entity.y) * 2 < 50)


class Player(BaseEntity):
    """
    In singleplayer:
        Player is main adventurer. Trying to pass the game till the end
    In multiplayer:
        There are a lot of Players surronding you and bumbling around.

    """

    def __init__(self, name, image=None, hp=200, x=0, y=0, speed=1):
        super().__init__(x, y, '', speed)
        """
        x, y - coords
        image is a list of Tiles
        """
        self.image = image
        if image:
            self.texture = image[self.rotation]
        self.name = name
        self.x = x
        self.y = y
        self.width, self.height = self.texture.get_size()
        self._render = RenderPlayer(self)
        self.hp = hp
        self.is_killed = False

    def move(self, keys_states, speed=None):
        if not self.is_killed:
            if speed is None:
                speed = self.speed
            try:
                direction = self._direction_map[keys_states]
                self.x = self.x + (direction[0]['dx'] * speed)
                self.y = self.y + (direction[0]['dy'] * speed)
                self.rotation = direction[1] - 1
                if not self.is_killed:
                    self.texture = self.image[self.rotation]
            except KeyError:
                pass
        print('pl', self.cartesian_to_isometric(self.x, self.y))

    def render(self, screen=None, border_offset=[500, 100]):
        self._render.render_isometric_player(screen, border_offset)

    def is_attacked(self):
        self._render.is_attacked()
        
    def get_rect(self):
        return self.texture.get_rect()
    


class NPC(BaseEntity):
    """
    NPC -   all "zombie" like entities. 
    E.g. "players"(not exactly) that's attacking Player(main adventurer, see above).
    How to know is it NPC?
        * no one control it with keyboard, mouse, any other stuff.
        * has primitive actions, generally it's stupid AI or hardcoded actions.
    """

    def __init__(self, skin, image=None, hp=100, x=0, y=0, speed=1):
        super().__init__(x, y, '', speed)
        self.weapon = None
        self.skin = skin
        self.image = image
        if image:
            self.texture = image[self.rotation]
        self.x = x
        self.y = y
        self.width, self.height = self.texture.get_size()
        self._render = RenderNPC(self)
        self.hp = hp
        self.attack_pause = 40

        """if there is no weapon, NPC will try to kill player without it"""
        self.damage = 20

        self.dest_complete = True
        self.dest_x = 0
        self.dest_y = 0

    def render(self, screen=None, border_offset=[500, 100]):
        self._render.render_isometric_npc(screen, border_offset)

    def update(self):
        self.x += self.speed
        self.y += self.speed

    def set_weapon(self, weapon):
        self.weapon = weapon

    def go_to(self, player):
        if self.attack_pause < 40:
            self.attack_pause += 1
        if self.speed > abs(self.x - player.x):
            self.x += self.x - player.x
        elif self.x != player.x:
            if self.x > player.x:
                self.x -= self.speed
            else:
                self.x += self.speed
        if self.speed > abs(self.y - player.y):
            self.y += self.y - player.y
        elif self.y != player.y:
            if self.y > player.y:
                self.y -= self.speed
            else:
                self.y += self.speed

    def attack(self, player):
        if self.weapon == None:
            damage = self.damage
            radius = 10
        else:
            damage = self.weapon.damage
            radius = self.weapon.radius
        if self.attack_pause == 40 and player.hp > 0:
            if ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5 <= radius:
                player.hp -= damage
                player.is_attacked()
                if player.hp <= 0:
                    player.is_killed = True
                self.attack_pause = 0
                
    def get_rect(self):
        return self.texture.get_rect()

    def random_move(self, tile_size=128, map_width=10, map_height=10, border_offset=[500, 100]):
        """randomly calculating a point on the map
            and going to it"""

        if self.attack_pause < 40:
            self.attack_pause += 1

        rot_x = 0
        rot_y = 0

        if self.dest_complete:
            self.dest_x = randint(0, map_width * tile_size // 2)
            self.dest_y = randint(0, map_height * tile_size // 2)
            self.dest_complete = False

        if (self.x, self.y) == (self.dest_x, self.dest_y):
            self.dest_complete = True
            print(1)
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

        """changing texture rotate"""

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

        self.texture = self.image[self.rotation]