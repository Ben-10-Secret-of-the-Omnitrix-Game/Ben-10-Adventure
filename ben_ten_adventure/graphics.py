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
        self.tile_size = tile_size

        self.iso_x = x
        self.iso_y = y

    def render_isometric_tile(self, screen):
        screen: pygame.Surface
        # TODO make self.tile_size Named Tuple for better code reading
        cart_x = self.x * self.tile_size / 2
        cart_y = self.y * self.tile_size / 2
        self.iso_x, self.iso_y = self.cartesian_to_isometric(
            cart_x, cart_y)
        screen.blit(self.texture, (self.iso_x + self.border_offset[0], self.iso_y + self.border_offset[1]))


class RenderPlayer:
    def __init__(self, player):
        self.player = player
        self.screen = None

    def player_place(self, x, y):
        return x, y - self.player.height + 20

    def render_isometric_player(self, screen=None, border_offset=[500, 100]):
        if screen is None:
            screen = self.screen
        else:
            self.screen = screen

        font = pygame.font.Font(None, 40)
        if screen:
            iso_x, iso_y = self.player.cartesian_to_isometric(self.player.x, self.player.y)
            screen.blit(self.player.texture,
                        self.player_place(border_offset[0] + iso_x, border_offset[1] + iso_y))
            text = font.render('Health: ' + str(self.player.hp), True, (100, 255, 100))
            screen.blit(text, (1200, 200))

    def is_attacked(self):
        duration = 0
        changes = [-3, -2, -1, 0, 1, 2, 3]
        x = self.player.x
        y = self.player.y
        while duration != 5:
            self.player.x += choice(changes)
            self.player.y += choice(changes)
            self.render_isometric_player()
            duration += 1
        self.player.x = x
        self.player.y = y
        self.screen = None


class RenderNPC:
    def __init__(self, npc):
        self.npc = npc
        self.screen = None

    def npc_place(self, x, y):
        return x, y - self.npc.height + 20

    def render_isometric_npc(self, screen=None, border_offset=[500, 100]):
        if screen is None:
            screen = self.screen
        else:
            self.screen = screen

        if screen:
            iso_x, iso_y = self.npc.cartesian_to_isometric(self.npc.x, self.npc.y)
            screen.blit(self.npc.texture,
                        self.npc_place(border_offset[0] + iso_x, border_offset[1] + iso_y))

    def is_attacked(self):
        duration = 0
        changes = [-3, -2, -1, 0, 1, 2, 3]
        x = self.npc.x
        y = self.npc.y
        while duration != 5:
            self.npc.x += choice(changes)
            self.npc.y += choice(changes)
            self.render_isometric_npc()
            duration += 1
        self.npc.x = x
        self.npc.y = y
        self.screen = None


class RenderEntities:
    """To render all entities right, we've got to compare everything
        That's why we put all entities together for rendering"""

    def render(self, entities, screen=None, border_offset=[500, 100]):
        entities = sorted(entities, key=lambda x: x.x + x.y)
        for ent in entities:
            ent.render(screen, border_offset)

class Camera:
    def __init__(self, map_field):
        self.map = map_field
    
    def render_focus(self):
        pass