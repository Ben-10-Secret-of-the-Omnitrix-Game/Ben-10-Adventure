import pygame
from .animation import ButtonAnimation

class ButtonSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__()
        self.animation = ButtonAnimation(images)
        
        self.image = self.animation.current() # returns Surface
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    
    def animate(self, state):
        self.animation.update(state)
        return self
    
    def draw(self, screen):
        # rect = self.animation.current().get_rect()
        # rect.x = self.rect.x
        # rect.y = self.rect.y
        # screen.fill((0, 0, 0, 0), rect)
        screen.blit(self.animation.current(), self.rect)
        
    def check_click(self, position):
        return self.rect.collidepoint(position)
    
    
            