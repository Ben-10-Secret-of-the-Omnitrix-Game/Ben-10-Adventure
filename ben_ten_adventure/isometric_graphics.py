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


class Tile:

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
        cart_x = self.x * self.tile_size[0]
        cart_y = self.y * self.tile_size[1]
        self.iso_x, self.iso_y = self.cartesian_to_isometric(
        cart_x + self.border_offset / 2, cart_y - self.border_offset / 4)
        # logging.info(f"Original ({self.x}, {self.y}); Decart ({cart_x}, {cart_y}); Isometric ({self.iso_x}, {self.iso_y}); Padded ({cart_x + self.border_offset}, {cart_y - self.border_offset / 2})")
        screen.blit(self.texture, (self.iso_x, self.iso_y))

    
    def get_cell_center(self, x, y):
        # TODO add documentation. Simplify code, increase readability !!!
        cart_x = (x + 1) * self.tile_size[0] + self.border_offset
        cart_y = (y - 2) * self.tile_size[1] + self.border_offset
        cntr_x = cart_x + self.tile_size[0] // 2
        cntr_y = cart_y + self.tile_size[1] // 2
        return self.cartesian_to_isometric(cart_x, cntr_y)
    
    def cartesian_to_isometric(self, cart_x, cart_y):
        isometric_x = (cart_x - cart_y)
        isometric_y = (cart_x + cart_y) / 2
        return isometric_x, isometric_y
