class Settings:
    """A class to store all settings for Alien Invaders."""

    def __init__(self):
        """Initialise the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 76, 153)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 51, 51
        self.bullet_allowed = 3

        # Enemy settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up.
        self.speedup_scale = 1.1
        # How quickly the enemy point value increase.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 0.8
        self.bullet_speed_factor = 3
        self.enemy_speed_factor = 0.5

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.enemy_points = 50

    def increae_speed(self):
        """Increase speed settings enemy point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.enemy_speed_factor *= self.speedup_scale

        self.enemy_points = int(self.enemy_points * self.score_scale)
