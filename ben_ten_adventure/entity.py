import pygame
from .graphics import RenderPlayer


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

    def __init__(self, name, image=None, x=0, y=0, speed=1):
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

    def move(self, keys_states, speed=None):
        if speed is None:
            speed = self.speed
        try:
            direction = self._direction_map[keys_states]
            self.x = self.x + (direction[0]['dx'] * speed)
            self.y = self.y + (direction[0]['dy'] * speed)
            self.rotation = direction[1] - 1
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
    pass
