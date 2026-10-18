from bar import Bar
from player import Player
import pygame

class LevelBar(Bar):
    def __init__(
        self,
        player: Player,
        x: float,
        y: float,
        length: float,
        value: int = 0,
        max_value: int = 100
    ):
        super().__init__(x, y ,length, value, max_value)
        self.player = player
        self.max_value = max_value

    def draw(self, screen: pygame.Surface):
        # 1. Calculate fill ratio
        ratio = max(0, min(1, self.value / self.max_value))
        fill_width = ratio * self.length

        # 2. Dimensions
        bar_height = 12
        bar_x = self.x
        bar_y = self.y

        # 3. Background (empty bar)
        pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, self.length, bar_height))

        # 4. Filled portion (XP progress)
        xp_color = (100, 149, 237)  # cornflower blue for XP
        pygame.draw.rect(screen, xp_color, (bar_x, bar_y, fill_width, bar_height))

        # 5. Border
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, self.length, bar_height), 1)

        # 6. Level text in the center
        level_text = f"Level {self.player.level}"
        font = pygame.font.Font(None, 16)
        text = font.render(level_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(bar_x + self.length / 2, bar_y + bar_height / 2))
        screen.blit(text, text_rect)

    def update(self, dt):
        self.value = self.player.xp
        self.max_value = self.player.next_level_xp
