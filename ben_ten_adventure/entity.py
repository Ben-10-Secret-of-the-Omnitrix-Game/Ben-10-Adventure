import pygame

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
    def __init__(self, x, y, skin, speed=1):
        # pygame.sprite.Sprite.__init__(self)
        self.super().__init__(self)
        """
        x and y - entity current position
        skin - image of entity. Instance of pygame.Surface
        """
        self.x = x
        self.y = y
        self.skin = skin
        self._direction_map = {
            (0, 0, 0, 0): {'dx': 0, 'dy': 0},
            (1, 0, 0, 0): {'dx': 0, 'dy': 1},
            (0, 1, 0, 0): {'dx': 0, 'dy': -1},
            (0, 0, 1, 0): {'dx': 1, 'dy': 0},
            (0, 0, 0, 1): {'dx': -1, 'dy': 0},
            (1, 0, 1, 0): {'dx': 1, 'dy': 1},
            (1, 0, 0, 1): {'dx': -1, 'dy': 1},
            (0, 1, 1, 0): {'dx': 1, 'dy': -1},
            (0, 0, 1, 1): {'dx': -1, 'dy': -1},
        }
        self.speed = speed
    
    def _move(self, keys_states, speed=None):
        if speed is None:
            speed = self.speed
        direction = self._direction_map[keys_states]
        self.x = self.x + (direction['dx'] * speed)
        self.y = self.y + (direction['dy'] * speed)


class Player(BaseEntity):
    """
    In singleplayer:
        Player is main adventurer. Trying to pass the game till the end
    In multiplayer:
        There are a lot of Players surronding you and bumbling around.

    """
    def __init__(self):
        pass


class NPC(BaseEntity):
    """
    NPC -   all "zombie" like entities. 
    E.g. "players"(not exacly) that's attacking Player(main adventurer, see above). 
    How to know is it NPC?
        * Nonone control it with keyboard, mouse, any other stuff.
        * has primitive actions, generally it's stupid AI or hardcoded actions.
    """
    pass
