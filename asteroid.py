from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from circleshape import CircleShape
from logger import log_event
import random
import pygame

class Asteroid(CircleShape):

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(
            screen,
            "white",
            self.position,
            self.radius,
            LINE_WIDTH
        )

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            result = random.uniform(20, 50)
            newvec = self.velocity.rotate(result)
            newoppvec = self.velocity.rotate(result * -1)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            new_ast_1 = Asteroid(self.position.x, self.position.y, radius = new_radius)
            new_ast_1.velocity = newvec
            new_ast_1.velocity *= 1.2
            new_ast_2 = Asteroid(self.position.x, self.position.y, radius = new_radius)
            new_ast_2.velocity = newoppvec
            new_ast_2.velocity *= 1.2
