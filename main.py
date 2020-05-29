import sys
import pygame
from settings import Settings
from battleship import Ship
from enemy import Enemy
import functions as func
from pygame.sprite import Group


def run_game():
    # Initialise game and create a game object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invaders")

    # Make a ship, a group of bullets and a group of enemies.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    enemies = Group()

    # Create a fleet of enemies.
    func.create_fleet(ai_settings, screen, enemies)

    # Start main loop for the game.
    while True:

        # Watch for keyboard and mouse events.
        func.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        func.update_bullets(bullets)
        func.update_screen(ai_settings, screen, ship, enemies, bullets)


run_game()
