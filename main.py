import sys
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import ScoreBoard
from button import Button
from battleship import Ship
from enemy import Enemy
import functions as func
from pygame.sprite import Group


def run_game():
    # Initialise game and create a game object.
    pygame.init()
    ai_settings = Settings()
    #screen_width, screen_height=pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders")
    icon = pygame.image.load('resources/battleship24.png')
    pygame.display.set_icon(icon)

    # Make a play button.
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = ScoreBoard(ai_settings, screen, stats)

    # Make a ship, a group of bullets and a group of enemies.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    enemies = Group()

    # Create a fleet of enemies.
    func.create_fleet(ai_settings, screen, ship, enemies)

    # Start main loop for the game.
    while True:

        # Watch for keyboard and mouse events.
        func.check_events(ai_settings, screen, stats,
                          play_button, ship, enemies, bullets)

        if stats.game_active:
            ship.update()
            func.update_bullets(ai_settings, screen, stats,
                                sb, ship, enemies, bullets)
            func.update_enemies(ai_settings, stats, screen,
                                ship, enemies, bullets)

        func.update_screen(ai_settings, screen, stats, sb, ship,
                           enemies, bullets, play_button)


run_game()
