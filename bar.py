import pygame

class Bar(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, length: float, value, max_value):
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()
        self.x = x
        self.y = y
        self.length = length
        self.value = value
        self.max_value = max_value

    def draw(self, screen: pygame.Surface):
        pass
        # must override

    def update(self):
        pass
        # must override
