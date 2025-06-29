"""
Player class for QGamen_DanmakuShooting
"""

import pygame
import math

class Player:
    """Player character class."""
    
    def __init__(self, x, y):
        """Initialize the player."""
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.speed = 5
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        
        # Shooting
        self.shoot_cooldown = 0
        self.shoot_delay = 5  # frames between shots
        
        # Special attack
        self.special_cooldown = 0
        self.special_delay = 30  # frames between special attacks
        
        # Invulnerability after being hit
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 180  # 3 seconds at 60 FPS
        self.blink_timer = 0
        
        # Colors
        self.color = (0, 255, 0)  # Green
        self.invulnerable_color = (0, 128, 0)  # Darker green
        
    def update(self, keys):
        """Update player state."""
        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        
        # Keep player within game area (left 2/3 of screen)
        game_area_width = 1280 * 2 // 3  # 修正: 新しい画面サイズに対応
        self.x = max(self.width // 2, min(self.x, game_area_width - self.width // 2))
        self.y = max(self.height // 2, min(self.y, 720 - self.height // 2))  # 修正: 新しい画面サイズに対応
        
        # Update rect
        self.rect.centerx = self.x
        self.rect.centery = self.y
        
        # Update shooting cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # Update special attack cooldown
        if self.special_cooldown > 0:
            self.special_cooldown -= 1
        
        # Update invulnerability
        if self.invulnerable:
            self.invulnerable_timer -= 1
            self.blink_timer += 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
    
    def shoot(self):
        """Create a bullet if shooting is allowed."""
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = self.shoot_delay
            return PlayerBullet(self.x, self.y - self.height // 2)
        return None
    
    def special_attack(self):
        """Trigger bomb special attack."""
        if self.special_cooldown <= 0:
            self.special_cooldown = self.special_delay
            # Return bomb position (player's current position)
            return {'x': self.x, 'y': self.y, 'radius': 200}
        return None
    
    def hit(self):
        """Handle player being hit."""
        # Reset position to center
        game_area_width = 1280 * 2 // 3  # 修正: 新しい画面サイズに対応
        self.x = game_area_width // 2
        self.y = 720 - 100  # 修正: 新しい画面サイズに対応
        
        # Start invulnerability
        self.invulnerable = True
        self.invulnerable_timer = self.invulnerable_duration
        self.blink_timer = 0
    
    def draw(self, screen):
        """Draw the player."""
        # Blinking effect during invulnerability
        if self.invulnerable and (self.blink_timer // 10) % 2 == 0:
            # Don't draw (blinking effect)
            return
        
        # Choose color based on invulnerability
        color = self.invulnerable_color if self.invulnerable else self.color
        
        # Draw player as a triangle pointing up
        points = [
            (self.x, self.y - self.height // 2),  # Top
            (self.x - self.width // 2, self.y + self.height // 2),  # Bottom left
            (self.x + self.width // 2, self.y + self.height // 2)   # Bottom right
        ]
        pygame.draw.polygon(screen, color, points)
        
        # Draw a small circle in the center for precise hitbox visualization
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 2)

class PlayerBullet:
    """Player bullet class."""
    
    def __init__(self, x, y):
        """Initialize the bullet."""
        self.x = x
        self.y = y
        self.width = int(4 * 1.5)  # 修正: 弾のサイズを1.5倍に
        self.height = int(8 * 1.5)  # 修正: 弾のサイズを1.5倍に
        self.speed = 10
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        self.color = (255, 255, 0)  # Yellow
    
    def update(self):
        """Update bullet position."""
        self.y -= self.speed
        self.rect.centery = self.y
    
    def is_off_screen(self):
        """Check if bullet is off screen."""
        return self.y < 0
    
    def draw(self, screen):
        """Draw the bullet."""
        pygame.draw.rect(screen, self.color, self.rect)
