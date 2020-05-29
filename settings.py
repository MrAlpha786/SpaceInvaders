class Settings:
    """A class to store all settings for Alien Invaders."""

    def __init__(self):
        """Initialise the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 76, 153)

        self.ship_speed_factor = 0.8

        # Bullet settings
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 51, 51
        self.bullet_allowed = 3
