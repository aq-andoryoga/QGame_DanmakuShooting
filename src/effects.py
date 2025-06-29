"""
Visual effects for QGamen_DanmakuShooting
"""

import pygame
import random
import math

class Explosion:
    """Explosion effect when enemies are destroyed."""
    
    def __init__(self, x, y):
        """Initialize the explosion."""
        self.x = x
        self.y = y
        self.particles = []
        self.lifetime = 30  # frames
        self.timer = 0
        
        # Create particles
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            color = random.choice([
                (255, 255, 0),   # Yellow
                (255, 200, 0),   # Orange
                (255, 100, 0),   # Red-orange
                (255, 255, 255)  # White
            ])
            self.particles.append({
                'x': x,
                'y': y,
                'dx': dx,
                'dy': dy,
                'color': color,
                'size': random.randint(2, 5)
            })
    
    def update(self):
        """Update the explosion."""
        self.timer += 1
        
        # Update particles
        for particle in self.particles:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['dx'] *= 0.95  # Slow down
            particle['dy'] *= 0.95
            particle['size'] = max(1, particle['size'] - 0.1)
    
    def is_finished(self):
        """Check if explosion is finished."""
        return self.timer >= self.lifetime
    
    def draw(self, screen):
        """Draw the explosion."""
        for particle in self.particles:
            if particle['size'] > 0:
                pygame.draw.circle(screen, particle['color'], 
                                 (int(particle['x']), int(particle['y'])), 
                                 int(particle['size']))

class EffectManager:
    """Manages all visual effects."""
    
    def __init__(self):
        """Initialize the effect manager."""
        self.explosions = []
    
    def add_explosion(self, x, y):
        """Add an explosion effect."""
        self.explosions.append(Explosion(x, y))
    
    def update(self):
        """Update all effects."""
        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.is_finished():
                self.explosions.remove(explosion)
    
    def draw(self, screen):
        """Draw all effects."""
        for explosion in self.explosions:
            explosion.draw(screen)
