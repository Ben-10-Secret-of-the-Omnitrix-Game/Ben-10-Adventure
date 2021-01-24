import logging

from pygame import Surface

class Animation:
    DEFAULT = 0
    def __init__(self, images):
        self.images = images
        self.state = self.DEFAULT
        self._states_count = len(self.images)

    def _update(self, state):
        if state >= self._states_count:
            # TODO add check for debug
            raise ValueError("Your state is greater than count of images")
        self.state = state
        return True
    

class ButtonAnimation(Animation):
    # button states
    PRESSED = 1
    
    def __init__(self, images):
        super().__init__(images)
    
    def update(self, state):
        if not self._update(state):
            return False
        return self.images[self.state]
    
    def toggle(self):
        self.state ^= 1
        return self.images[self.state]
    
    def current(self) -> Surface:
        return self.images[self.state]
    
    