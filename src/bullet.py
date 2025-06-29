"""
Bullet manager for QGamen_DanmakuShooting
"""

import pygame

class BulletManager:
    """Manages all bullets in the game."""
    
    def __init__(self):
        """Initialize the bullet manager."""
        self.player_bullets = []
        self.enemy_bullets = []
        self.game_area_width = 1920 * 2 // 3
        self.screen_height = 1080
    
    def add_player_bullet(self, bullet):
        """Add a player bullet."""
        if bullet:
            self.player_bullets.append(bullet)
    
    def add_enemy_bullet(self, bullet):
        """Add an enemy bullet."""
        if bullet:
            self.enemy_bullets.append(bullet)
    
    def update(self):
        """Update all bullets."""
        # Update player bullets
        for bullet in self.player_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.player_bullets.remove(bullet)
        
        # Update enemy bullets
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.is_off_screen(self.game_area_width, self.screen_height):
                self.enemy_bullets.remove(bullet)
    
    def draw(self, screen):
        """Draw all bullets."""
        for bullet in self.player_bullets:
            bullet.draw(screen)
        
        for bullet in self.enemy_bullets:
            bullet.draw(screen)
    
    def clear_all(self):
        """Clear all bullets."""
        self.player_bullets.clear()
        self.enemy_bullets.clear()
