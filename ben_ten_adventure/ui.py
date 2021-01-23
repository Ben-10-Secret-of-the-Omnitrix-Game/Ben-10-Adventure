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
        return self.animation.update(state)
    
    def draw(self, screen):
        screen.blit(self.animation.current(), self.rect)
    
    
            