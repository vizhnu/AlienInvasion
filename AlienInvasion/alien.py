import pygame
from pygame.sprite import Sprite
import time

class Alien(Sprite):
    """a class to represent a single alien"""

    def __init__(self, ai_settings, screen):
        super().__init__()  # initialises the Sprite super class
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/alien.bmp')
        self.rect=self.image.get_rect()

        #starts the alien at the top of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #stores the exact position of the alien in float value
        self.x = float(self.rect.x)

    def blitme(self):

        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x


    def check_edges(self):
        """Returns true if one alien touches the edge"""
        screen_rect = self.screen.get_rect()
        if  self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
