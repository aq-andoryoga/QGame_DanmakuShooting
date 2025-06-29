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
        y_offset = 30
        
        # Score
        score_text = self.font_manager.render_text("スコア", 48, self.WHITE)
        screen.blit(score_text, (self.ui_x, y_offset))
        y_offset += 40
        
        score_value = self.font_manager.render_text(f"{score:08d}", 36, self.YELLOW)
        screen.blit(score_value, (self.ui_x, y_offset))
        y_offset += 70
        
        # Lives
        lives_text = self.font_manager.render_text("ライフ", 48, self.WHITE)
        screen.blit(lives_text, (self.ui_x, y_offset))
        y_offset += 40
        
        # Draw life icons
        for i in range(lives):
            life_x = self.ui_x + i * 35
            life_y = y_offset
            # Draw small triangles representing lives
            points = [
                (life_x + 12, life_y),      # Top
                (life_x, life_y + 16),      # Bottom left
                (life_x + 24, life_y + 16)  # Bottom right
            ]
            pygame.draw.polygon(screen, self.GREEN, points)
        
        y_offset += 70
        
        # Special Attacks
        special_text = self.font_manager.render_text("爆弾", 48, self.WHITE)
        screen.blit(special_text, (self.ui_x, y_offset))
        y_offset += 40
        
        special_count = self.font_manager.render_text(f"残り: {special_attacks}個", 36, self.MAGENTA)
        screen.blit(special_count, (self.ui_x, y_offset))
        y_offset += 30
        
        # Draw bomb icons
        for i in range(min(special_attacks, 6)):  # Show max 6 icons
            icon_x = self.ui_x + (i % 3) * 25
            icon_y = y_offset + (i // 3) * 25
            # Draw bomb icon (circle with fuse)
            pygame.draw.circle(screen, self.MAGENTA, (icon_x + 8, icon_y + 8), 8)
            pygame.draw.circle(screen, self.WHITE, (icon_x + 8, icon_y + 8), 6)
            # Draw fuse
            pygame.draw.line(screen, self.YELLOW, (icon_x + 12, icon_y + 4), (icon_x + 16, icon_y), 2)
        
        y_offset += 80
        
        # Controls
        controls_text = self.font_manager.render_text("操作方法", 36, self.WHITE)
        screen.blit(controls_text, (self.ui_x, y_offset))
        y_offset += 35
        
        control_lines = [
            "矢印キー: 移動",
            "WASD: 移動", 
            "スペース: 射撃",
            "Xキー: 爆弾",
            "ESC: メニュー"
        ]
        
        for line in control_lines:
            control_text = self.font_manager.render_text(line, 24, self.WHITE)
            screen.blit(control_text, (self.ui_x, y_offset))
            y_offset += 25
        
        y_offset += 30
        
        # Game info
        info_text = self.font_manager.render_text("ゲーム情報", 36, self.WHITE)
        screen.blit(info_text, (self.ui_x, y_offset))
        y_offset += 35
        
        info_lines = [
            "敵を倒して100点",
            "アイテムで10点",
            "",
            "弾を避けよう！",
            "被弾後3秒無敵",
            "爆弾で一掃！"
        ]
        
        for line in info_lines:
            if line:  # Skip empty lines
                info_line = self.font_manager.render_text(line, 24, self.WHITE)
                screen.blit(info_line, (self.ui_x, y_offset))
            y_offset += 22
