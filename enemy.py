import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):
    """A class to represent a single enemy in the fleet."""

    def __init__(self, ai_settings, screen):
        """Initialise the enemy and set its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the enemy image and set its rect attribute.
        self.image = pygame.image.load('resources/enemy.png')
        self.rect = self.image.get_rect()

        # Start each new enemy near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store enemy's exact position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if enemy is at the edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the enemy right or left."""
        self.x += (self.ai_settings.enemy_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        """Draw the enemy at its current location."""
        self.screen.blit(self.image, self.rect)
