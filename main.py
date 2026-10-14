from locale import D_T_FMT # wtf is this
from asteroidfield import AsteroidField
from asteroid import Asteroid
from constants import SCREEN_HEIGHT
from constants import SCREEN_WIDTH
from constants import PLAYER_RADIUS
from player import Player
import pygame
from logger import log_state


def main():
    pygame.init()
    print("Starting Asteroids")
    print(f"Screen width: { SCREEN_WIDTH }")
    print(f"Screen height: { SCREEN_HEIGHT }")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Player.containers = (updatable, drawable)

    asteroidField = AsteroidField()
    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2, radius = PLAYER_RADIUS)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0


    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")

        for thing in drawable:
            thing.draw(screen)

        for thing in updatable:
            thing.update(dt)

        pygame.display.flip()
        dt = clock.tick(60) / 1000



if __name__ == "__main__":
    main()
