"""
Enemy classes for QGamen_DanmakuShooting
"""

import pygame
import math
import random

class EnemyStrength:
    """Enemy strength levels."""
    WEAK = 0
    NORMAL = 1
    STRONG = 2

class Enemy:
    """Base enemy class."""
    
    def __init__(self, x, y, strength=EnemyStrength.NORMAL):
        """Initialize the enemy."""
        self.x = x
        self.y = y
        self.strength = strength
        
        # Size and speed based on strength
        if strength == EnemyStrength.WEAK:
            self.width = 25
            self.height = 25
            self.speed = 3
            self.hp = 1
        elif strength == EnemyStrength.NORMAL:
            self.width = 30
            self.height = 30
            self.speed = 2
            self.hp = 1
        else:  # STRONG
            self.width = 40
            self.height = 40
            self.speed = 1.5
            self.hp = 2
        
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
    
    def get_item_drop_count(self):
        """Get number of items to drop when destroyed."""
        if self.strength == EnemyStrength.WEAK:
            return random.randint(1, 2)
        elif self.strength == EnemyStrength.NORMAL:
            return random.randint(2, 4)
        else:  # STRONG
            return random.randint(4, 7)
    
    def is_off_screen(self, screen_height):
        """Check if enemy is off screen."""
        return self.y > screen_height + self.height
    
    def draw(self, screen):
        """Draw the enemy."""
        # Color based on strength
        if self.strength == EnemyStrength.WEAK:
            hull_color = (255, 150, 150)  # Light red
            engine_color = (200, 100, 100)
        elif self.strength == EnemyStrength.NORMAL:
            hull_color = (255, 100, 100)  # Red
            engine_color = (200, 50, 50)
        else:  # STRONG
            hull_color = (200, 50, 50)    # Dark red
            engine_color = (150, 25, 25)
        
        # Draw enemy spaceship (inverted triangle)
        center_x = self.rect.centerx
        center_y = self.rect.centery
        
        # Main hull
        hull_points = [
            (center_x, center_y + 10),      # Bottom point
            (center_x - 8, center_y - 8),   # Top left
            (center_x + 8, center_y - 8)    # Top right
        ]
        pygame.draw.polygon(screen, hull_color, hull_points)
        
        # Engine glow at the back (top)
        pygame.draw.circle(screen, engine_color, (center_x - 4, center_y - 10), 2)
        pygame.draw.circle(screen, engine_color, (center_x + 4, center_y - 10), 2)
        
        # Cockpit/core
        cockpit_color = tuple(min(255, c + 30) for c in hull_color)
        pygame.draw.circle(screen, cockpit_color, (center_x, center_y), 3)
        
        # Strength indicator
        if self.strength == EnemyStrength.STRONG:
            # Draw energy shield effect
            shield_color = (255, 255, 100, 100)  # Yellow with alpha
            shield_surface = pygame.Surface((self.rect.width + 6, self.rect.height + 6), pygame.SRCALPHA)
            pygame.draw.rect(shield_surface, shield_color, shield_surface.get_rect(), 2)
            screen.blit(shield_surface, (self.rect.x - 3, self.rect.y - 3))

class RadialEnemy(Enemy):
    """Enemy that shoots bullets in a radial pattern."""
    
    def __init__(self, x, y, strength=EnemyStrength.NORMAL):
        """Initialize the radial enemy."""
        super().__init__(x, y, strength)
        
        # Bullet count based on strength
        if strength == EnemyStrength.WEAK:
            self.bullet_count = 6
            self.shoot_interval = 80
        elif strength == EnemyStrength.NORMAL:
            self.bullet_count = 8
            self.shoot_interval = 60
        else:  # STRONG
            self.bullet_count = 12
            self.shoot_interval = 40
        
        self.angle_offset = 0
    
    def create_bullet_pattern(self):
        """Create radial bullet pattern."""
        bullets = []
        angle_step = 360 / self.bullet_count
        
        for i in range(self.bullet_count):
            angle = math.radians(i * angle_step + self.angle_offset)
            dx = math.cos(angle)
            dy = math.sin(angle)
            speed = 2 + self.strength * 0.5
            bullets.append(EnemyBullet(self.x, self.y, dx * speed, dy * speed))
        
        self.angle_offset += 10  # Rotate pattern
        return bullets

class CircularEnemy(Enemy):
    """Enemy that shoots bullets in a circular wave pattern."""
    
    def __init__(self, x, y, strength=EnemyStrength.NORMAL):
        """Initialize the circular enemy."""
        super().__init__(x, y, strength)
        
        # Bullet count based on strength
        if strength == EnemyStrength.WEAK:
            self.bullet_count = 8
            self.shoot_interval = 90
        elif strength == EnemyStrength.NORMAL:
            self.bullet_count = 12
            self.shoot_interval = 60
        else:  # STRONG
            self.bullet_count = 16
            self.shoot_interval = 45
        
        self.wave_timer = 0
    
    def create_bullet_pattern(self):
        """Create circular wave bullet pattern."""
        bullets = []
        angle_step = 360 / self.bullet_count
        
        for i in range(self.bullet_count):
            angle = math.radians(i * angle_step + self.wave_timer * 2)
            dx = math.cos(angle)
            dy = math.sin(angle)
            speed = 2 + math.sin(self.wave_timer * 0.1) * 1 + self.strength * 0.3
            bullets.append(EnemyBullet(self.x, self.y, dx * speed, dy * speed))
        
        self.wave_timer += 1
        return bullets

class SpiralEnemy(Enemy):
    """Enemy that shoots bullets in a spiral pattern."""
    
    def __init__(self, x, y, strength=EnemyStrength.NORMAL):
        """Initialize the spiral enemy."""
        super().__init__(x, y, strength)
        
        # Shooting frequency based on strength
        if strength == EnemyStrength.WEAK:
            self.shoot_interval = 15
            self.spiral_arms = 2
        elif strength == EnemyStrength.NORMAL:
            self.shoot_interval = 10
            self.spiral_arms = 3
        else:  # STRONG
            self.shoot_interval = 8
            self.spiral_arms = 4
        
        self.spiral_angle = 0
    
    def create_bullet_pattern(self):
        """Create spiral bullet pattern."""
        bullets = []
        
        # Create bullets in spiral arms
        for i in range(self.spiral_arms):
            angle = math.radians(self.spiral_angle + i * (360 / self.spiral_arms))
            dx = math.cos(angle)
            dy = math.sin(angle)
            speed = 3 + self.strength * 0.5
            bullets.append(EnemyBullet(self.x, self.y, dx * speed, dy * speed))
        
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
    
    def update(self, game_time):
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
            self.spawn_enemy(game_time)
    
    def spawn_enemy(self, game_time):
        """Spawn a new enemy with strength based on game time."""
        enemy_type = random.choice(self.enemy_types)
        x = random.randint(50, self.game_area_width - 50)
        y = -50
        
        # Determine strength based on game time
        time_factor = game_time / 3600  # Convert frames to minutes (60fps * 60s)
        
        # Probability weights change over time
        weak_prob = max(0.5 - time_factor * 0.1, 0.1)
        normal_prob = max(0.4 - time_factor * 0.05, 0.3)
        strong_prob = min(0.1 + time_factor * 0.15, 0.6)
        
        # Normalize probabilities
        total = weak_prob + normal_prob + strong_prob
        weak_prob /= total
        normal_prob /= total
        strong_prob /= total
        
        rand = random.random()
        if rand < weak_prob:
            strength = EnemyStrength.WEAK
        elif rand < weak_prob + normal_prob:
            strength = EnemyStrength.NORMAL
        else:
            strength = EnemyStrength.STRONG
        
        enemy = enemy_type(x, y, strength)
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
        self.width = int(6 * 1.5)  # 修正: 弾のサイズを1.5倍に
        self.height = int(6 * 1.5)  # 修正: 弾のサイズを1.5倍に
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
        # Enemy plasma bolt
        # Draw outer glow
        glow_radius = self.width // 2 + 2
        glow_color = tuple(max(0, c - 100) for c in self.color)
        pygame.draw.circle(screen, glow_color, (int(self.x), int(self.y)), glow_radius)
        
        # Draw main bolt
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.width // 2)
        
        # Draw bright center
        bright_color = tuple(min(255, c + 50) for c in self.color)
        center_radius = max(1, self.width // 4)
        pygame.draw.circle(screen, bright_color, (int(self.x), int(self.y)), center_radius)
