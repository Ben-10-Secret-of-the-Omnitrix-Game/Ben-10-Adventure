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

    def __init__(self, x, y, image=None, tile_size=(48, 48), wall_height=48):
        """
        color - tuple of (r, g, b) or (r, g, b, a)
        x and y are all cartesian coordinates 
        """
        assert isinstance(image, pygame.Surface), image
        self.x = x
        self.y = y 
        self.texture = image
        self.border_offset = -250
        self.tile_size = tile_size
        self.wall_height = wall_height

        

    def render_isometric_tile(self, screen):
        screen: pygame.Surface
        cart_x = self.x * self.tile_size[0]
        cart_y = self.y * self.tile_size[1]
        iso_x, iso_y = self.cartesian_to_isometric(cart_x, cart_y)
        # logging.info(f"Original ({self.x}, {self.y}); Decart ({cart_x}, {cart_y}); Isometric ({iso_x}, {iso_y})")
        # iso_x *= self.tile_size[0] 
        # iso_y *= self.tile_size[1] 
        # print(iso_x, iso_y)
        screen.blit(self.texture, (iso_x + 700, iso_y - 500))


    def cartesian_to_isometric(self, cart_x, cart_y):
        # isometric_x = (cart_x * self.texture.get_width()) - (cart_y * self.texture.get_width())
        # isometric_y = (cart_y * self.texture.get_height()) - (cart_x * self.texture.get_height())
        isometric_x = (cart_x - cart_y)
        isometric_y = (cart_x + cart_y) / 2
        return isometric_x, isometric_y