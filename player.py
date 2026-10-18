from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_SPEED
from constants import PLAYER_SHOOT_SPEED, PLAYER_TURN_SPEED
from constants import LINE_WIDTH, PLAYER_SHOOT_COOLDOWN_SECONDS
from shot import Shot
import pygame
import math

class Player(CircleShape):
    x: float
    y: float
    rotation: float
    cooldown: float

    def __init__(self, x, y, radius, rotation = 0, cooldown = 0.0):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = rotation
        self.cooldown = cooldown
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.last_mouse_move = 0

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

        self.cooldown -= dt # cooldown for shots

        # key controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(dt * -1)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(dt * -1)
        if keys[pygame.K_SPACE]:
            if self.cooldown > 0:
                pass
            else:
                self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
                self.shoot()

        # mouse controls
        self.rotate_with_mouse()

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def rotate_with_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.position.x
        dy = mouse_y - self.position.y
        angle = math.degrees(math.atan2(dy, dx)) - 90
        self.rotation = angle

        if mouse_x != self.last_mouse_x or mouse_y != self.last_mouse_y:
            self.last_mouse_move = pygame.time.get_ticks()
            self.last_mouse_x, self.last_mouse_y = mouse_x, mouse_y

    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        vector = pygame.Vector2(0, 1)
        rotated_vector = vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SHOOT_SPEED
        shot.velocity += rotated_with_speed_vector
