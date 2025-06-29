"""
Enemy classes for QGamen_DanmakuShooting
"""

import pygame
import math
import random

class Enemy:
    """Base enemy class."""
    
    def __init__(self, x, y):
        """Initialize the enemy."""
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = 2
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        self.color = (255, 0, 0)  # Red
        
        # Shooting
        self.shoot_timer = 0
        self.shoot_interval = 60  # frames between shots
        self.bullet_pattern = 0
        
    def update(self):
        """Update enemy state."""
        self.y += self.speed
        self.rect.centery = self.y
        
        # Update shooting timer
        self.shoot_timer += 1
    
    def get_bullets(self):
        """Get bullets to shoot this frame."""
        bullets = []
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            bullets = self.create_bullet_pattern()
        return bullets
    
    def create_bullet_pattern(self):
        """Create bullet pattern (to be overridden by subclasses)."""
        return []
    
    def is_off_screen(self, screen_height):
        """Check if enemy is off screen."""
        return self.y > screen_height + self.height
    
    def draw(self, screen):
        """Draw the enemy."""
        pygame.draw.rect(screen, self.color, self.rect)

class RadialEnemy(Enemy):
    """Enemy that shoots bullets in a radial pattern."""
    
    def __init__(self, x, y):
        """Initialize the radial enemy."""
        super().__init__(x, y)
        self.color = (255, 100, 100)  # Light red
        self.bullet_count = 8
        self.angle_offset = 0
    
    def create_bullet_pattern(self):
        """Create radial bullet pattern."""
        bullets = []
        angle_step = 360 / self.bullet_count
        
        for i in range(self.bullet_count):
            angle = math.radians(i * angle_step + self.angle_offset)
            dx = math.cos(angle)
            dy = math.sin(angle)
            bullets.append(EnemyBullet(self.x, self.y, dx * 3, dy * 3))
        
        self.angle_offset += 10  # Rotate pattern
        return bullets

class CircularEnemy(Enemy):
    """Enemy that shoots bullets in a circular wave pattern."""
    
    def __init__(self, x, y):
        """Initialize the circular enemy."""
        super().__init__(x, y)
        self.color = (255, 150, 150)  # Lighter red
        self.bullet_count = 12
        self.wave_timer = 0
    
    def create_bullet_pattern(self):
        """Create circular wave bullet pattern."""
        bullets = []
        angle_step = 360 / self.bullet_count
        
        for i in range(self.bullet_count):
            angle = math.radians(i * angle_step + self.wave_timer * 2)
            dx = math.cos(angle)
            dy = math.sin(angle)
            speed = 2 + math.sin(self.wave_timer * 0.1) * 1
            bullets.append(EnemyBullet(self.x, self.y, dx * speed, dy * speed))
        
        self.wave_timer += 1
        return bullets

class SpiralEnemy(Enemy):
    """Enemy that shoots bullets in a spiral pattern."""
    
    def __init__(self, x, y):
        """Initialize the spiral enemy."""
        super().__init__(x, y)
        self.color = (200, 100, 255)  # Purple
        self.spiral_angle = 0
        self.shoot_interval = 10  # Shoot more frequently
    
    def create_bullet_pattern(self):
        """Create spiral bullet pattern."""
        bullets = []
        
        # Create 3 bullets in a spiral
        for i in range(3):
            angle = math.radians(self.spiral_angle + i * 120)
            dx = math.cos(angle)
            dy = math.sin(angle)
            bullets.append(EnemyBullet(self.x, self.y, dx * 4, dy * 4))
        
        self.spiral_angle += 15  # Rotate spiral
        return bullets

class EnemyManager:
    """Manages all enemies."""
    
    def __init__(self, game_area_width, screen_height):
        """Initialize the enemy manager."""
        self.game_area_width = game_area_width
        self.screen_height = screen_height
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_interval = 120  # frames between spawns
        self.enemy_types = [RadialEnemy, CircularEnemy, SpiralEnemy]
    
    def update(self):
        """Update all enemies."""
        # Update existing enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.is_off_screen(self.screen_height):
                self.enemies.remove(enemy)
        
        # Spawn new enemies
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.spawn_enemy()
    
    def spawn_enemy(self):
        """Spawn a new enemy."""
        enemy_type = random.choice(self.enemy_types)
        x = random.randint(50, self.game_area_width - 50)
        y = -50
        enemy = enemy_type(x, y)
        self.enemies.append(enemy)
    
    def get_bullets(self):
        """Get all bullets from all enemies."""
        bullets = []
        for enemy in self.enemies:
            bullets.extend(enemy.get_bullets())
        return bullets
    
    def draw(self, screen):
        """Draw all enemies."""
        for enemy in self.enemies:
            enemy.draw(screen)

class EnemyBullet:
    """Enemy bullet class."""
    
    def __init__(self, x, y, dx, dy):
        """Initialize the bullet."""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = 6
        self.height = 6
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        self.color = (255, 100, 100)  # Light red
    
    def update(self):
        """Update bullet position."""
        self.x += self.dx
        self.y += self.dy
        self.rect.centerx = self.x
        self.rect.centery = self.y
    
    def is_off_screen(self, game_area_width, screen_height):
        """Check if bullet is off screen."""
        return (self.x < 0 or self.x > game_area_width or 
                self.y < 0 or self.y > screen_height)
    
    def draw(self, screen):
        """Draw the bullet."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.width // 2)
