"""
UI system for QGamen_DanmakuShooting
"""

import pygame

class UI:
    """User interface class for displaying game information."""
    
    def __init__(self, game_area_width, ui_area_width, screen_height):
        """Initialize the UI."""
        self.game_area_width = game_area_width
        self.ui_area_width = ui_area_width
        self.screen_height = screen_height
        self.ui_x = game_area_width + 20  # Start of UI area with padding
        
        # Initialize fonts
        pygame.font.init()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.YELLOW = (255, 255, 0)
    
    def draw(self, screen, score, lives):
        """Draw the UI elements."""
        y_offset = 50
        
        # Score
        score_text = self.font_large.render("SCORE", True, self.WHITE)
        screen.blit(score_text, (self.ui_x, y_offset))
        y_offset += 50
        
        score_value = self.font_medium.render(f"{score:08d}", True, self.YELLOW)
        screen.blit(score_value, (self.ui_x, y_offset))
        y_offset += 100
        
        # Lives
        lives_text = self.font_large.render("LIVES", True, self.WHITE)
        screen.blit(lives_text, (self.ui_x, y_offset))
        y_offset += 50
        
        # Draw life icons
        for i in range(lives):
            life_x = self.ui_x + i * 40
            life_y = y_offset
            # Draw small triangles representing lives
            points = [
                (life_x + 15, life_y),      # Top
                (life_x, life_y + 20),      # Bottom left
                (life_x + 30, life_y + 20)  # Bottom right
            ]
            pygame.draw.polygon(screen, self.GREEN, points)
        
        y_offset += 100
        
        # Controls
        controls_text = self.font_medium.render("CONTROLS", True, self.WHITE)
        screen.blit(controls_text, (self.ui_x, y_offset))
        y_offset += 40
        
        control_lines = [
            "Arrow Keys: Move",
            "WASD: Move",
            "Space: Shoot",
            "ESC: Menu"
        ]
        
        for line in control_lines:
            control_text = self.font_small.render(line, True, self.WHITE)
            screen.blit(control_text, (self.ui_x, y_offset))
            y_offset += 30
        
        y_offset += 50
        
        # Game info
        info_text = self.font_medium.render("GAME INFO", True, self.WHITE)
        screen.blit(info_text, (self.ui_x, y_offset))
        y_offset += 40
        
        info_lines = [
            "Destroy enemies",
            "for 100 points",
            "",
            "Avoid bullets!",
            "3 second invulnerable",
            "time after hit"
        ]
        
        for line in info_lines:
            if line:  # Skip empty lines
                info_line = self.font_small.render(line, True, self.WHITE)
                screen.blit(info_line, (self.ui_x, y_offset))
            y_offset += 25
