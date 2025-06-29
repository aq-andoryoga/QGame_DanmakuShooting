"""
Item system for QGamen_DanmakuShooting
"""

import pygame
import random
import math

class ScoreItem:
    """Score item that gives points when collected."""
    
    def __init__(self, x, y):
        """Initialize the score item."""
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        
        # Movement
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(1, 3)
        self.gravity = 0.1
        
        # Visual
        self.color = (255, 255, 0)  # Yellow
        self.blink_timer = 0
        self.lifetime = 600  # 10 seconds at 60 FPS
        self.timer = 0
        
    def update(self):
        """Update item position and state."""
        # Apply movement
        self.x += self.dx
        self.y += self.dy
        self.dy += self.gravity
        
        # Update rect
        self.rect.centerx = self.x
        self.rect.centery = self.y
        
        # Update timers
        self.blink_timer += 1
        self.timer += 1
        
        # Slow down horizontal movement
        self.dx *= 0.98
    
    def is_expired(self, screen_height):
        """Check if item should be removed."""
        return self.timer >= self.lifetime or self.y > screen_height + 50
    
    def draw(self, screen):
        """Draw the score item."""
        # Blink faster as it approaches expiration
        if self.timer > self.lifetime * 0.8:
            if (self.blink_timer // 5) % 2 == 0:
                return  # Don't draw (blinking effect)
        
        # Draw as a small diamond
        points = [
            (self.x, self.y - self.height // 2),      # Top
            (self.x + self.width // 2, self.y),       # Right
            (self.x, self.y + self.height // 2),      # Bottom
            (self.x - self.width // 2, self.y)        # Left
        ]
        pygame.draw.polygon(screen, self.color, points)
        
        # Add a small white center
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 2)

class ItemManager:
    """Manages all items in the game."""
    
    def __init__(self):
        """Initialize the item manager."""
        self.score_items = []
        self.game_area_width = 1280 * 2 // 3
        self.screen_height = 720
    
    def add_score_item(self, x, y):
        """Add a score item at the specified position."""
        # Add some randomness to the position
        item_x = x + random.uniform(-20, 20)
        item_y = y + random.uniform(-10, 10)
        self.score_items.append(ScoreItem(item_x, item_y))
    
    def update(self):
        """Update all items."""
        # Update score items
        for item in self.score_items[:]:
            item.update()
            if item.is_expired(self.screen_height):
                self.score_items.remove(item)
    
    def draw(self, screen):
        """Draw all items."""
        for item in self.score_items:
            item.draw(screen)
    
    def clear_all(self):
        """Clear all items."""
        self.score_items.clear()
