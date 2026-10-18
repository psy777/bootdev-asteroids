from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_SPEED, PLAYER_START_LEVEL
from constants import PLAYER_SHOOT_SPEED, PLAYER_TURN_SPEED, BASE_LEVEL_UP_XP
from constants import LINE_WIDTH, PLAYER_SHOOT_COOLDOWN_SECONDS
from shot import Shot
import pygame
import math
import sys

class Player(CircleShape):
    x: float
    y: float
    rotation: float
    cooldown: float
    auto_shooting: bool
    level: int

    def __init__(self,
            x, y,
            radius,
            rotation = 0,
            cooldown = 0.0,
            auto_shooting = False,
            level:int = PLAYER_START_LEVEL
            ):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = rotation
        self.cooldown = cooldown
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.last_mouse_move = 0
        self.auto_shooting = auto_shooting
        self.level = level
        self.health = level * 50 + 450
        self.max_health = level * 50 + 450
        self.xp = 0
        self.needed_xp = BASE_LEVEL_UP_XP # required xp to reach next level
        self.next_level_xp = BASE_LEVEL_UP_XP # total xp required for the next level

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
        if keys[pygame.K_SPACE]: # hold to shoot
            if self.cooldown > 0:
                pass
            else:
                self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
                self.shoot()
        if keys[pygame.K_c]: # toggle automatic shooting
            self.toggle_shooting()

        # if shooting toggle is on
        if self.auto_shooting:
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

    def toggle_shooting(self):
        if self.auto_shooting == True:
            self.auto_shooting = False
        else:
            self.auto_shooting = True

    def take_damage(self, other, dt):
        if other.radius <= 20:
            self.health -= 50
        elif other.radius > 20 and other.radius <= 40:
            self.health -= 100
        else:
            self.health -= 200

        if self.health <= 0:
            print("Game Over!")
            sys.exit()

        # collision normal from asteroid to player
        normal = (self.position - other.position).normalize()
        # push player away
        self.velocity += normal * 800
        self.position += self.velocity * dt
        # push asteroid away (slightly less for variety)
        other.velocity -= normal * 100

    def level_up(self, extra: int = 0):
        self.level += 1
        self.xp = extra
        self.next_level_xp = BASE_LEVEL_UP_XP * (self.level * 1.5)
        self.needed_xp = self.next_level_xp - extra

    def gain_xp(self):
        self.xp += 20
        if self.xp >= self.needed_xp:
            extra = self.xp - self.needed_xp
            self.level_up(extra = extra)
