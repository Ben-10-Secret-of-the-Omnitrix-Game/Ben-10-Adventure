"""

I don't know exacly what should I include here
Defenetly here should be stuff to render
Have a look into demo_isometric_level
Functions like:
    render_isometric_tile
    render_isometric_tilemap
    cartesian_to_isometric
Certainly will be here

"""
import logging
import pygame
from random import choice

class BasicIsometric:
    
    def cartesian_to_isometric(self, cart_x, cart_y):
        isometric_x = (cart_x - cart_y)
        isometric_y = (cart_x + cart_y) / 2
        return isometric_x, isometric_y
    
    def isometric_to_cartesian(self, iso_x, iso_y):
        pass


class Tile(BasicIsometric):

    def __init__(self, x, y, border_offset, image=None, tile_size=(48, 48)):
        """
        border_offset - x only padding
        x and y are all cartesian coordinates 
        """
        assert isinstance(image, pygame.Surface), image
        self.x = x
        self.y = y
        self.texture = image
        self.border_offset = border_offset
        self.tile_size = (64, 64)
        
        self.iso_x = x
        self.iso_y = y

    def render_isometric_tile(self, screen):
        screen: pygame.Surface
        # TODO make self.tile_size Named Tuple for better code reading
        cart_x = self.x * self.tile_size[0]
        cart_y = self.y * self.tile_size[1]
        # offset = self.tile_size[0] // 32
        self.iso_x, self.iso_y = self.cartesian_to_isometric(
        cart_x, cart_y)
        # logging.info(f"24 Original ({self.x}, {self.y}); Decart ({cart_x}, {cart_y}); Isometric ({self.iso_x}, {self.iso_y}); Tile Size: {self.tile_size}")
        # logging.info(f"Original ({self.x}, {self.y}); Decart ({cart_x}, {cart_y}); Isometric ({self.iso_x}, {self.iso_y}); Padded ({cart_x + self.border_offset}, {cart_y - self.border_offset / 2})")
        screen.blit(self.texture, (self.iso_x + 500, self.iso_y + 100))
    
    
class RenderPlayer:
    def __init__(self, player):
        self.player = player
        self.screen = None

    def player_place(self, x, y):
        return x, y - self.player.height + 20

    def render_isometric_player(self):
        font = pygame.font.Font(None, 40)
        if not self.player.is_killed:
            self.screen.blit(self.player.texture,
                        self.player_place(*self.player.cartesian_to_isometric(self.player.x, self.player.y)))
            text = font.render('Health: ' + str(self.player.hp), True, (100, 255, 100))
        else:
            text = font.render('Wasted', True, (255, 100, 100))
        self.screen.blit(text, (650, 20))

    def is_attacked(self):
        duration = 0
        changes = [-3, -2, -1, 0, 1, 2, 3]
        x = self.player.x
        y = self.player.y
        while duration != 5:
            self.player.x += choice(changes)
            self.player.y += choice(changes)
            self.render_isometric_player()
            pygame.display.flip()
            pygame.time.wait(10)
            duration += 1
        self.player.x = x
        self.player.y = y


class RenderNPC:
    def __init__(self, npc):
        self.npc = npc

    def npc_place(self, x, y):
        return x, y - self.npc.height + 20

    def render_isometric_npc(self, screen):
        screen.blit(self.npc.texture,
                    self.npc_place(*self.npc.cartesian_to_isometric(self.npc.x, self.npc.y)))
