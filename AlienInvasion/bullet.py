from pygame.sprite import Sprite

import pygame


class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship):
        super().__init__()
        self.screen = screen

        # create a bullet at (0,0) and then assign it correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)  # creates a rectangle with pygame.Rect
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # stores the distance of the bullet from bottom i.e y cordinate
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """updates the position of the bullet by decreasing the y co-ord"""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
