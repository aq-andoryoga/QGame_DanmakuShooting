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
        
        # Movement boundaries (will be set by game)
        self.game_area_width = 1280 * 2 // 3  # Default value
        self.screen_height = 720  # Default value
        
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
        
    def set_boundaries(self, game_area_width, screen_height):
        """Set movement boundaries for the player."""
        self.game_area_width = game_area_width
        self.screen_height = screen_height
    
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
        
        # Keep player within game area
        self.x = max(self.width // 2, min(self.x, self.game_area_width - self.width // 2))
        self.y = max(self.height // 2, min(self.y, self.screen_height - self.height // 2))
        
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
        
        # Spaceship colors
        if self.invulnerable:
            hull_color = (255, 200, 200)  # Reddish when invulnerable
            engine_color = (255, 100, 100)
            cockpit_color = (255, 150, 150)
        else:
            hull_color = (200, 220, 255)  # Light blue-white
            engine_color = (100, 150, 255)  # Blue engine glow
            cockpit_color = (150, 200, 255)  # Lighter blue
        
        # Draw spaceship body (main hull)
        hull_points = [
            (self.x, self.y - 15),      # Nose
            (self.x - 8, self.y + 5),   # Left wing
            (self.x - 5, self.y + 10),  # Left engine mount
            (self.x + 5, self.y + 10),  # Right engine mount
            (self.x + 8, self.y + 5)    # Right wing
        ]
        pygame.draw.polygon(screen, hull_color, hull_points)
        
        # Draw engine glow
        pygame.draw.circle(screen, engine_color, (int(self.x - 5), int(self.y + 12)), 3)
        pygame.draw.circle(screen, engine_color, (int(self.x + 5), int(self.y + 12)), 3)
        
        # Draw bright engine core
        bright_engine = tuple(min(255, c + 50) for c in engine_color)
        pygame.draw.circle(screen, bright_engine, (int(self.x - 5), int(self.y + 12)), 1)
        pygame.draw.circle(screen, bright_engine, (int(self.x + 5), int(self.y + 12)), 1)
        
        # Draw cockpit
        pygame.draw.circle(screen, cockpit_color, (int(self.x), int(self.y - 5)), 4)
        
        # Draw wing details
        wing_detail_color = tuple(max(0, c - 20) for c in hull_color)
        pygame.draw.line(screen, wing_detail_color, (self.x - 6, self.y + 2), (self.x - 4, self.y + 8), 2)
        pygame.draw.line(screen, wing_detail_color, (self.x + 6, self.y + 2), (self.x + 4, self.y + 8), 2)
        
        # Draw precise hitbox center (small dot)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 1)

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
        # Player laser beam
        # Draw outer glow
        glow_rect = pygame.Rect(self.rect.x - 1, self.rect.y - 1, self.rect.width + 2, self.rect.height + 2)
        pygame.draw.rect(screen, (50, 100, 150), glow_rect)  # Blue glow
        
        # Draw main beam
        pygame.draw.rect(screen, (100, 200, 255), self.rect)  # Blue laser
        
        # Draw bright core
        if self.rect.width > 2 and self.rect.height > 2:
            core_rect = pygame.Rect(self.rect.x + 1, self.rect.y, self.rect.width - 2, self.rect.height)
            pygame.draw.rect(screen, (200, 230, 255), core_rect)  # Bright blue core
