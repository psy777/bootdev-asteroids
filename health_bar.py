from player import Player
from bar import Bar
from constants import LINE_WIDTH
import pygame

class HealthBar(Bar):
    def __init__(self, player: Player, x: float, y: float, length: float, max_health: int):
        super().__init__(x, y, length, max_health, max_health)
        self.player = player
        self.length = 80

    def draw(self, screen: pygame.Surface):
        # 1. Get current health
        health = self.player.health
        ratio = max(0, min(1, health / self.player.max_health))

        # 2. Compute the visual fill length
        fill_width = ratio * self.length

        # 3. Position the bar centered above the player
        bar_x = self.player.position.x - self.length / 2
        bar_y = self.player.position.y + 30
        bar_height = 8

        # 4. Color based on health percentage
        if ratio > 0.5:
            color = (50, 205, 50)  # green
        elif ratio > 0.25:
            color = (238, 207, 50)  # yellow/orange
        else:
            color = (211, 47, 47)  # red

        # 5. Draw the background (empty bar)
        pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, self.length, bar_height))

        # 6. Draw the foreground (filled portion)
        pygame.draw.rect(screen, color, (bar_x, bar_y, fill_width, bar_height))

        # 7. Optional: add a border
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, self.length, bar_height), 1)

    def update(self):
        pass
