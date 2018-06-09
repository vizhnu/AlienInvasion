class Settings:
    """"stores all the settings of Alien Invasion"""

    def __init__(self):
    #------------------------------------------
    #all static game settings are stored here
    #------------------------------------------
        # screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bgcolor = (99, 186, 96)

        # ship settings

        self.ship_limit = 3

        #bullet settings

        self.bullet_height = 15
        self.bullet_width = 3
        self.bullet_color = (120,56,0)
        self.allowed_bullets = 1


        self.speedup_scale = 1.08

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 2
        #alien settings
        self.alien_speed_factor = .5
        self.fleet_drop_speed = 17
        self.fleet_direction = 1

        #score settings
        self.score = 0

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        # alien settings
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_direction *= self.speedup_scale