from constants import SCREEN_HEIGHT
from constants import held_keys
from constants import SCREEN_WIDTH
from constants import PLAYER_RADIUS
from player import Player
from bar import Bar
from health_bar import HealthBar
from level_bar import LevelBar
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from logger import log_event
import pygame
import sys
from logger import log_state


def main():
    pygame.init()
    print("Starting Asteroids")
    print(f"Screen width: { SCREEN_WIDTH }")
    print(f"Screen height: { SCREEN_HEIGHT }")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Shot.containers = (updatable, drawable, shots)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Player.containers = (updatable, drawable)
    HealthBar.containers = (drawable,)
    LevelBar.containers = (drawable, updatable)

    asteroidField = AsteroidField()
    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2, radius = PLAYER_RADIUS, level = 1)
    player_health_bar = HealthBar(
        player = player,
        x = player.position.x,
        y = player.position.y,
        length = 30.0,
        max_health = player.max_health)
    level_bar = LevelBar(player = player, x = (SCREEN_WIDTH - 350.0) / 2, y = SCREEN_HEIGHT / 20, length = 350.0, max_value = 100)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0


    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                held_keys.add(event.scancode)
            elif event.type == pygame.KEYUP:
                held_keys.discard(event.scancode)
        screen.fill("black")

        for thing in drawable:
            thing.draw(screen)

        for thing in updatable:
            thing.update(dt)

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    asteroid.split()
                    shot.kill()
                    player.gain_xp()
                    log_event("asteroid_shot")

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                player.take_damage(asteroid, dt)

        pygame.display.flip()
        dt = clock.tick(60) / 1000



if __name__ == "__main__":
    main()
