"""
UI system for QGamen_DanmakuShooting
"""

import pygame
from font_manager import font_manager

class UI:
    """User interface class for displaying game information."""
    
    def __init__(self, game_area_width, ui_area_width, screen_height):
        """Initialize the UI."""
        self.game_area_width = game_area_width
        self.ui_area_width = ui_area_width
        self.screen_height = screen_height
        self.ui_x = game_area_width + 20  # Start of UI area with padding
        
        # Use font manager for Japanese support
        self.font_manager = font_manager
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.YELLOW = (255, 255, 0)
        self.BLUE = (0, 100, 255)
        self.MAGENTA = (255, 100, 255)
    
    def draw(self, screen, score, lives, special_attacks):
        """Draw the UI elements."""
        # Draw semi-transparent UI background panel (narrower)
        ui_panel = pygame.Surface((160, screen.get_height()))
        ui_panel.set_alpha(100)
        ui_panel.fill((0, 0, 30))  # Dark blue
        screen.blit(ui_panel, (screen.get_width() - 160, 0))
        
        # Draw panel border
        pygame.draw.line(screen, (100, 150, 255), 
                        (screen.get_width() - 160, 0), 
                        (screen.get_width() - 160, screen.get_height()), 2)
        
        # Adjust UI position for narrower panel
        ui_x = screen.get_width() - 150
        y_offset = 20
        
        # Score with glow effect (smaller font)
        score_text = self.font_manager.render_text("スコア", 32, (200, 230, 255))
        # Draw subtle glow
        glow_text = self.font_manager.render_text("スコア", 32, (100, 150, 200))
        screen.blit(glow_text, (ui_x + 1, y_offset + 1))
        screen.blit(score_text, (ui_x, y_offset))
        y_offset += 35
        
        score_value = self.font_manager.render_text(f"{score:08d}", 24, (255, 255, 150))
        screen.blit(score_value, (ui_x, y_offset))
        y_offset += 50
        
        # Lives with spaceship icons (smaller font)
        lives_text = self.font_manager.render_text("ライフ", 32, (200, 230, 255))
        glow_text = self.font_manager.render_text("ライフ", 32, (100, 150, 200))
        screen.blit(glow_text, (ui_x + 1, y_offset + 1))
        screen.blit(lives_text, (ui_x, y_offset))
        y_offset += 35
        
        # Draw mini spaceships for lives (smaller icons)
        for i in range(lives):
            life_x = ui_x + i * 25
            life_y = y_offset
            # Draw mini spaceship for each life (smaller)
            pygame.draw.polygon(screen, (100, 200, 255), [
                (life_x + 8, life_y),       # Nose
                (life_x + 2, life_y + 8),   # Left wing
                (life_x + 14, life_y + 8)   # Right wing
            ])
            # Mini engines
            pygame.draw.circle(screen, (50, 150, 255), (life_x + 5, life_y + 10), 1)
            pygame.draw.circle(screen, (50, 150, 255), (life_x + 11, life_y + 10), 1)
        
        y_offset += 50
        
        # Special Attacks with energy theme (smaller font)
        special_text = self.font_manager.render_text("爆弾", 32, (200, 230, 255))
        glow_text = self.font_manager.render_text("爆弾", 32, (100, 150, 200))
        screen.blit(glow_text, (ui_x + 1, y_offset + 1))
        screen.blit(special_text, (ui_x, y_offset))
        y_offset += 35
        
        special_count = self.font_manager.render_text(f"残り: {special_attacks}/2個", 24, (255, 150, 255))
        screen.blit(special_count, (ui_x, y_offset))
        y_offset += 25
        
        # Draw energy bomb icons (smaller)
        for i in range(min(special_attacks, 2)):  # Show max 2 icons
            icon_x = ui_x + i * 30
            icon_y = y_offset
            
            # Draw energy bomb (glowing orb) - smaller
            # Outer glow
            pygame.draw.circle(screen, (100, 50, 150), (icon_x + 8, icon_y + 8), 10)
            # Main orb
            pygame.draw.circle(screen, (255, 100, 255), (icon_x + 8, icon_y + 8), 8)
            # Inner core
            pygame.draw.circle(screen, (255, 200, 255), (icon_x + 8, icon_y + 8), 4)
            # Energy spark
            pygame.draw.circle(screen, (255, 255, 255), (icon_x + 8, icon_y + 8), 2)
        
        y_offset += 60
        
        # Game info section
        info_text = self.font_manager.render_text("操作方法", 28, (200, 230, 255))
        glow_text = self.font_manager.render_text("操作方法", 28, (100, 150, 200))
        screen.blit(glow_text, (ui_x + 1, y_offset + 1))
        screen.blit(info_text, (ui_x, y_offset))
        y_offset += 35
        
        # Control instructions
        info_lines = [
            "WASD: 移動",
            "Space: 射撃",
            "X: 爆弾",
            "",
            "ゲームのコツ:",
            "敵を倒してスコア",
            "アイテムを回収",
            "弾を避けよう！",
            "被弾後3秒無敵",
            "爆弾は1ライフ2個",
            "被弾で爆弾回復"
        ]
        
        for line in info_lines:
            if line:  # Skip empty lines
                info_line = self.font_manager.render_text(line, 20, self.WHITE)
                screen.blit(info_line, (ui_x, y_offset))
            y_offset += 22
