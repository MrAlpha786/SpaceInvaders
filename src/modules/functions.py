import sys
from time import sleep
import pygame
from modules.bullets import Bullet
from modules.enemy import Enemy


def get_number_enemies_x(ai_settings, enemy_width):
    """Determine the number of enemies that fit in a row."""
    available_sapce_x = ai_settings.screen_width - 2 * enemy_width
    number_enemies_x = int(available_sapce_x / (2 * enemy_width))
    return number_enemies_x


def get_number_rows(ai_settings, ship_height, enemy_height):
    """Determine the number of rows of enemies that fit on the screen."""
    available_sapce_y = (ai_settings.screen_height -
                         (3 * enemy_height) - ship_height)
    number_rows = int(available_sapce_y / (2 * enemy_height))
    return number_rows


def create_enemy(ai_settings, screen, enemies, enemy_number, row_number):
    """Create an enemy and place it in the row."""
    enemy = Enemy(ai_settings, screen)
    enemy_width = enemy.rect.width
    enemy.x = enemy_width + 2 * enemy_width * enemy_number
    enemy.rect.x = enemy.x
    enemy.rect.y = enemy.rect.height + 2 * enemy.rect.height * row_number
    enemies.add(enemy)


def create_fleet(ai_settings, screen, ship, enemies):
    """Create a full fleet of enemies."""
    # Create an enemy and find the number of enemies in a row.
    enemy = Enemy(ai_settings, screen)
    number_enemies_x = get_number_enemies_x(ai_settings, enemy.rect.width)
    number_rows = get_number_rows(
        ai_settings, ship.rect.height, enemy.rect.height)

    # Create the first row of enemies.
    for row_number in range(number_rows):
        for enemy_number in range(number_enemies_x):
            create_enemy(ai_settings, screen, enemies,
                         enemy_number, row_number)


def change_fleet_direction(ai_settings, enemies):
    """Drop the entire fleet and change the fleet's direction"""
    for enemy in enemies.sprites():
        enemy.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, enemies):
    """Respond appropriately if any enemy has reached an edge"""
    for enemy in enemies.sprites():
        if enemy.check_edges():
            change_fleet_direction(ai_settings, enemies)
            break


def ship_hit(ai_settings, stats, sb, screen, ship, enemies, bullets):
    """Respond to ship bieng hit by enemy."""
    if stats.ships_left > 0:
        # Decrement ship_left.
        stats.ships_left -= 1

        # Empty the list of enemies and bullets.
        enemies.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, enemies)
        ship.center_ship()

        # Pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_enemies_bottom(ai_settings, stats, sb, screen, ship, enemies, bullets):
    """Check if any enemy have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for enemy in enemies.sprites():
        if enemy.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, sb, screen, ship, enemies, bullets)
            break


def update_enemies(ai_settings, stats, sb, screen, ship, enemies, bullets):
    """Check if the fleet is at an edge and then update the position of all enemies in the fleet."""
    check_fleet_edges(ai_settings, enemies)
    enemies.update()

    # Look for enemy-ship collisions.
    if pygame.sprite.spritecollideany(ship, enemies):
        ship_hit(ai_settings, stats, sb, screen, ship, enemies, bullets)

    # Look for enemies hitting the bottom of the screen.
    check_enemies_bottom(ai_settings, stats, sb,
                         screen, ship, enemies, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keydown_events(event, ai_settings, screen, stats, sb, ship, enemies, bullets):
    """Respond to keypresses."""
    if stats.game_active:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            ship.moving_left = True

        elif event.key == pygame.K_SPACE:
            fire_bullet(ai_settings, screen, ship, bullets)

    if event.key == pygame.K_q:
        sys.exit()

    elif event.key == pygame.K_ESCAPE:
        # Game Pause
        if stats.game_active:
            stats.game_active = False
        elif stats.ships_left == 0:
            activate_game(ai_settings, screen, stats,
                          sb, ship, enemies, bullets)
        else:
            stats.game_active = True


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, enemies, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings,
                                 screen, stats, sb, ship, enemies, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, enemies, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button,
                      ship, enemies, bullets, mouse_x, mouse_y):
    """Start a new game when player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        activate_game(ai_settings, screen, stats, sb, ship, enemies, bullets)


def activate_game(ai_settings, screen, stats, sb, ship, enemies, bullets):
    """Activate Game."""
    # Reset the game settings.
    ai_settings.initialize_dynamic_settings()

    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)

    # Rest the game statistics.
    stats.reset_stats()
    stats.game_active = True

    # Reset the scoreboard images.
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()

    # Empty the list of enemies and bullets.
    enemies.empty()
    bullets.empty()

    # Create a new fleet and center the ship.
    create_fleet(ai_settings, screen, ship, enemies)
    ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, enemies, ex, bullets, play_button):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    enemies.draw(screen)

    # Draw the score information.
    sb.show_score()

    if ex.explode:
        ex.blit()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make most recently drawn screen visible.
    pygame.display.flip()


def check_bullet_enemy_collisions(ai_settings, screen, stats, sb, ship, enemies, ex, bullets):
    """ Respond to bullet-enemy collisions."""
    # Remove any bullet and enemy that have collided.
    collisions = pygame.sprite.groupcollide(bullets, enemies, True, True)

    if collisions:
        for enemies in collisions.values():
            stats.score += ai_settings.enemy_points * len(enemies)
            animate_explosion(ex, enemies[-1])
            sb.prep_score()
        check_high_score(stats, sb)
        ex.sound.play()

    if len(enemies) == 0:
        # If the fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, enemies)


def animate_explosion(ex, enemy):
    for i in range(9):
        ex.explosion_rect[i].center = enemy.rect.center

    ex.explode = True

def update_bullets(ai_settings, screen, stats, sb, ship, enemies, ex, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet position.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_enemy_collisions(
        ai_settings, screen, stats, sb, ship, enemies, ex, bullets)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
