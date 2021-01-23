import pygame
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
        self.render = RenderPlayer(self)
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

    def render_isometric_player(self, screen):
        self.render.render_isometric_player(screen)


class NPC(BaseEntity):
    """
    NPC -   all "zombie" like entities. 
    E.g. "players"(not exacly) that's attacking Player(main adventurer, see above). 
    How to know is it NPC?
        * Nonone control it with keyboard, mouse, any other stuff.
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
        self.render = RenderNPC(self)
        self.hp = hp
        self.attack_pause = 20

        """if there is no weapon, NPC will try to kill player without it"""
        self.damage = 20

    def render_isometric_npc(self, screen):
        self.render.render_isometric_npc(screen)

    def update(self):
        self.x += self.speed
        self.y += self.speed

    def set_weapon(self, weapon):
        self.weapon = weapon

    def go_to(self, player):
        if self.attack_pause < 20:
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
            radius = 1
        else:
            damage = self.weapon.damage
            radius = self.weapon.radius
        if self.attack_pause == 20 and player.hp > 0:
            if ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5 <= radius:
                player.hp -= damage
                if player.hp <= 0:
                    player.is_killed = True
                print(player.hp)
                self.attack_pause = 0