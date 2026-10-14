from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED
from constants import LINE_WIDTH
import pygame

class Player(CircleShape):
    x: float
    y: float
    rotation: float

    def __init__(self, x, y, radius, rotation = 0):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = rotation

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt * -1)
        if keys[pygame.K_d]:
            self.rotate(dt)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
