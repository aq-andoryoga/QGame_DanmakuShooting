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
                # Draw particle with glow effect
                # Outer glow
                glow_color = tuple(max(0, c - 100) for c in particle['color'])
                glow_size = int(particle['size'] * 1.5)
                if glow_size > 0:
                    pygame.draw.circle(screen, glow_color, 
                                     (int(particle['x']), int(particle['y'])), 
                                     glow_size)
                
                # Main particle
                pygame.draw.circle(screen, particle['color'], 
                                 (int(particle['x']), int(particle['y'])), 
                                 int(particle['size']))
                
                # Bright core
                core_color = tuple(min(255, c + 50) for c in particle['color'])
                core_size = max(1, int(particle['size'] * 0.5))
                pygame.draw.circle(screen, core_color, 
                                 (int(particle['x']), int(particle['y'])), 
                                 core_size)

class BombExplosion:
    """Large bomb explosion effect for special attacks."""
    
    def __init__(self, x, y, max_radius=200):
        """Initialize the bomb explosion."""
        self.x = x
        self.y = y
        self.max_radius = max_radius
        self.current_radius = 0
        self.lifetime = 60  # frames (1 second at 60 FPS)
        self.timer = 0
        self.particles = []
        self.shockwave_rings = []
        
        # Create initial particles
        for _ in range(50):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 12)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            color = random.choice([
                (255, 255, 255),  # White
                (255, 255, 100),  # Light yellow
                (255, 200, 100),  # Light orange
                (255, 150, 150),  # Light red
                (150, 150, 255)   # Light blue
            ])
            self.particles.append({
                'x': x,
                'y': y,
                'dx': dx,
                'dy': dy,
                'color': color,
                'size': random.randint(3, 8),
                'life': random.randint(30, 60)
            })
        
        # Create shockwave rings
        for i in range(3):
            self.shockwave_rings.append({
                'radius': 0,
                'max_radius': max_radius + i * 50,
                'start_time': i * 10,
                'alpha': 255
            })
    
    def update(self):
        """Update the bomb explosion."""
        self.timer += 1
        
        # Update main explosion radius
        progress = min(self.timer / 20.0, 1.0)  # Expand over 20 frames
        self.current_radius = self.max_radius * progress
        
        # Update particles
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['dx'] *= 0.98  # Slow down
            particle['dy'] *= 0.98
            particle['size'] = max(1, particle['size'] - 0.1)
            particle['life'] -= 1
            
            if particle['life'] <= 0 or particle['size'] <= 1:
                self.particles.remove(particle)
        
        # Update shockwave rings
        for ring in self.shockwave_rings:
            if self.timer >= ring['start_time']:
                ring_progress = min((self.timer - ring['start_time']) / 30.0, 1.0)
                ring['radius'] = ring['max_radius'] * ring_progress
                ring['alpha'] = max(0, 255 * (1.0 - ring_progress))
    
    def get_damage_radius(self):
        """Get the current damage radius."""
        return self.current_radius
    
    def is_finished(self):
        """Check if explosion is finished."""
        return self.timer >= self.lifetime
    
    def draw(self, screen):
        """Draw the bomb explosion."""
        # Draw shockwave rings
        for ring in self.shockwave_rings:
            if ring['radius'] > 0 and ring['alpha'] > 0:
                # Create a surface for alpha blending
                ring_surface = pygame.Surface((ring['radius'] * 2, ring['radius'] * 2), pygame.SRCALPHA)
                color_with_alpha = (255, 255, 255, int(ring['alpha']))
                pygame.draw.circle(ring_surface, color_with_alpha, 
                                 (int(ring['radius']), int(ring['radius'])), 
                                 int(ring['radius']), 3)
                screen.blit(ring_surface, (self.x - ring['radius'], self.y - ring['radius']))
        
        # Draw main explosion circle
        if self.current_radius > 0:
            # Outer glow
            glow_alpha = max(0, 100 * (1.0 - self.timer / self.lifetime))
            if glow_alpha > 0:
                glow_surface = pygame.Surface((self.current_radius * 2, self.current_radius * 2), pygame.SRCALPHA)
                glow_color = (255, 255, 200, int(glow_alpha))
                pygame.draw.circle(glow_surface, glow_color,
                                 (int(self.current_radius), int(self.current_radius)),
                                 int(self.current_radius))
                screen.blit(glow_surface, (self.x - self.current_radius, self.y - self.current_radius))
            
            # Inner bright circle
            inner_alpha = max(0, 200 * (1.0 - self.timer / 30.0))
            if inner_alpha > 0:
                inner_radius = self.current_radius * 0.6
                inner_surface = pygame.Surface((inner_radius * 2, inner_radius * 2), pygame.SRCALPHA)
                inner_color = (255, 255, 255, int(inner_alpha))
                pygame.draw.circle(inner_surface, inner_color,
                                 (int(inner_radius), int(inner_radius)),
                                 int(inner_radius))
                screen.blit(inner_surface, (self.x - inner_radius, self.y - inner_radius))
        
        # Draw particles
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
        self.bomb_explosions = []
    
    def add_explosion(self, x, y):
        """Add an explosion effect."""
        self.explosions.append(Explosion(x, y))
    
    def add_bomb_explosion(self, x, y, radius=200):
        """Add a bomb explosion effect."""
        self.bomb_explosions.append(BombExplosion(x, y, radius))
    
    def get_active_bomb_explosions(self):
        """Get currently active bomb explosions for damage calculation."""
        return [bomb for bomb in self.bomb_explosions if not bomb.is_finished()]
    
    def update(self):
        """Update all effects."""
        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.is_finished():
                self.explosions.remove(explosion)
        
        # Update bomb explosions
        for bomb in self.bomb_explosions[:]:
            bomb.update()
            if bomb.is_finished():
                self.bomb_explosions.remove(bomb)
    
    def draw(self, screen):
        """Draw all effects."""
        for explosion in self.explosions:
            explosion.draw(screen)
        
        for bomb in self.bomb_explosions:
            bomb.draw(screen)
