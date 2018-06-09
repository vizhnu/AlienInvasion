import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import pygame.font

def check_keydown_events(event, ai_settings, screen, ship, aliens, stats, bullets):
    # checks keypresses
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        start_game(ai_settings, stats, bullets, aliens, ship)


def check_keyup_events(event, ship):
    # check key releases
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, ship, bullets, aliens, stats, play_button):
    for event in pygame.event.get():  # listen for event
        if event.type == pygame.QUIT:  # window closed
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, aliens, stats, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, bullets, aliens, ship, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, play_button, bullets, aliens, ship, mouse_x, mouse_y):
    """starts a new game if player clicks the play button"""
    button_clicked = play_button.rect.collidepoint(mouse_x,
                                                   mouse_y)  # if play button is clicked butto_clicked has a value
    if button_clicked and not stats.game_active:  # to ensure that button is clicked after game has stopped
        # otherwise play button can be pressed even when it is invisible during gameplay
        start_game(ai_settings, stats, bullets, aliens, ship)


def start_game(ai_settings, stats, bullets, aliens, ship):
    stats.reset_stats()
    stats.game_active = True

    bullets.empty()
    aliens.empty()

    ship.center_ship()

    ai_settings.initialize_dynamic_settings()

    # hide curser
    pygame.mouse.set_visible(False)


def update_screen(ai_settings, stats, screen, ship, bullets, aliens, play_button):
    screen.fill(ai_settings.bgcolor)
    ship.blitme()
    aliens.draw(screen)
    # draw all bullets in bullets.sprites()
    for bullet in bullets.sprites():
        bullet.draw_bullet()

        # draw the button after everything else for it to be above everything
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()  # draws the most recent screen


def update_bullets(ai_settings, screen, ship, bullets, aliens):
    bullets.update()  # decreases y co-ord of bullet
    # removes bullets which disappear(if bottom of bullets==0)
    for bullet in bullets.copy():  # uses a copy of the original bullets list
        if bullet.rect.bottom == 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, bullets, aliens)


def check_bullet_alien_collisions(ai_settings, screen, ship, bullets, aliens):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # update score
    if (len(collisions) != 0):
        ai_settings.score += 1

    # repopulates aliens and removes extra bullets
    if len(aliens) == 0:
        create_fleet(ai_settings, screen, ship, aliens)
        ai_settings.increase_speed()
        bullets.empty()


def fire_bullet(ai_settings, screen, ship, bullets):
    # creates a new bullet and adds it to bullets group if the number of bullets inscreen is less than avb
    # TODO: make this work ....(after firing bullets in bursts bullets stops firing)
    if len(bullets) < ai_settings.allowed_bullets:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


# creating alien fleets

def get_num_of_aliens(ai_settings, alien_width):
    """returns the number of aliens that can be fitted in a row"""
    available_space = ai_settings.screen_width - 2 * alien_width
    number_of_aliens = int(available_space / (alien_width))
    return number_of_aliens - 2  # i removed 2 aliens because it was getting too crowded


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # creates a single alien
    alien = Alien(ai_settings, screen)

    alien_width = alien.rect.width
    alien_height = alien.rect.height

    spacing = 32  # found using trial and error
    alien.x = alien_width + 2 * spacing * alien_number
    alien.rect.y = alien_height + 2 * spacing * row_number

    alien.rect.x = alien.x
    aliens.add(alien)


def get_number_of_rows(ai_settings, ship_height, alien_height):
    available_height = ai_settings.screen_height - 3 * alien_height - ship_height
    no_of_rows = int(available_height / (100))
    return no_of_rows


def create_fleet(ai_settings, screen, ship, aliens):
    """creates a fleet of aliens"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_of_aliens = get_num_of_aliens(ai_settings, alien_width)
    no_of_rows = get_number_of_rows(ai_settings, ship.rect.height, alien.rect.height)

    # creates a fleet of aliens
    for row_number in range(no_of_rows):
        # creates a single row of aliens
        for alien_number in range(number_of_aliens):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


# moving aliens

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):  # checks if any one of the alien in aliens has hit the ship sprite
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    check_alien_hit_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """Checks whtehter any one of the aliens in the aliens in the fleet touches the edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


# Game Ending Conditions

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Aliens hit the ship"""
    if stats.ships_left > 0:
        # decrments number of ships left
        stats.ships_left -= 1

        # empty aliens and bullets
        bullets.empty()
        aliens.empty()

        # creates a fleet and centers the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # pause
        sleep(.5)
    else:
        stats.game_active = False
        aliens.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        pygame.mouse.set_visible(True)


def check_alien_hit_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break
