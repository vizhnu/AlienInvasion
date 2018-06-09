import pygame.font

class Button():
    """class to create a button"""

    def __init__(self,ai_settings, screen, msg):

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 200, 50
        self.button_color = (141, 66, 181)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None,48)

        # build the button's rect object and centre it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #calling funtion to dislay the msg
        self.display_msg(msg)

    def display_msg(self, msg):
        """turns text msg into a rendered image and displys it on the button at the cneter of the screen"""

        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):

        self.screen.fill(self.button_color, self.rect) #draws empty button
        self.screen.blit(self.msg_image,self.msg_image_rect) # draws message

