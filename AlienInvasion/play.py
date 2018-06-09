"""Alien invasion game in PyGame"""

import game_functions as gf
import pygame

from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button


def run_game():
    pygame.init()

    ai_settings = Settings()
    stats = GameStats(ai_settings)

    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))  # makes a drawable window of size 1200*807
    pygame.display.set_caption("Alien Invation")
    play_button = Button(ai_settings, screen, "Play")

    # create a ship and Groups of bullets and aliens
    ship = Ship(screen, ai_settings)
    bullets = Group()
    aliens = Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Game loop
    while True:
        gf.check_events(ai_settings, screen, ship, bullets,aliens, stats, play_button)  # listens for pygame events
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, bullets, aliens)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings,stats, screen, ship, bullets, aliens, play_button) # draws the content to screen

run_game()
