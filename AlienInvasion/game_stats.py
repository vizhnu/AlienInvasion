class GameStats():
    """Game statistix"""

    def __init__(self, ai_settings):

        self.ai_settings = ai_settings
        self.reset_stats() # calls reset_stats() to initialise all stats


    def reset_stats(self):
        """resets game statistics"""

        self.ships_left = self.ai_settings.ship_limit
        self.game_active = False