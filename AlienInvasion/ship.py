import pygame


class Ship():
    #  defines the space ship

    def __init__(self, screen, ai_settings):
        self.screen = screen

        self.image = pygame.image.load('images/small_ship.bmp')  # loads the image
        self.rect = self.image.get_rect()  # sets ship.rect's value as image's rect value
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings

        # position the ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)

        # movement flags
        self.moving_right = False
        self.moving_left = False


    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right :
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left :
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center

    def center_ship(self):
        self.center = self.screen_rect.centerx
