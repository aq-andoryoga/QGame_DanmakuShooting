"""
Space background system for QGamen_DanmakuShooting
Creates dynamic space backgrounds with stars, nebulae, and planets
"""

import pygame
import random
import math

class Star:
    """Individual star in the background."""
    
    def __init__(self, x, y, size, brightness, speed):
        """Initialize a star."""
        self.x = x
        self.y = y
        self.size = size
        self.brightness = brightness
        self.speed = speed
        self.twinkle_phase = random.uniform(0, 2 * math.pi)
        self.twinkle_speed = random.uniform(0.02, 0.05)
    
    def update(self, dt):
        """Update star position and twinkling."""
        # Move star downward (parallax scrolling)
        self.y += self.speed * dt
        
        # Update twinkling
        self.twinkle_phase += self.twinkle_speed * dt
    
    def draw(self, screen):
        """Draw the star."""
        # Calculate twinkling brightness
        twinkle_factor = 0.7 + 0.3 * math.sin(self.twinkle_phase)
        current_brightness = int(self.brightness * twinkle_factor)
        
        # Star color (white to blue-white)
        color = (current_brightness, current_brightness, min(255, current_brightness + 20))
        
        # Draw star
        if self.size <= 1:
            screen.set_at((int(self.x), int(self.y)), color)
        else:
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))

class Nebula:
    """Nebula cloud in the background."""
    
    def __init__(self, x, y, width, height, color, speed):
        """Initialize a nebula."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.alpha = random.randint(20, 60)
        self.pulse_phase = random.uniform(0, 2 * math.pi)
        self.pulse_speed = random.uniform(0.01, 0.03)
    
    def update(self, dt):
        """Update nebula position and pulsing."""
        self.y += self.speed * dt
        self.pulse_phase += self.pulse_speed * dt
    
    def draw(self, screen):
        """Draw the nebula."""
        # Create pulsing effect
        pulse_factor = 0.8 + 0.2 * math.sin(self.pulse_phase)
        current_alpha = int(self.alpha * pulse_factor)
        
        # Create nebula surface
        nebula_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Draw gradient circles for nebula effect
        center_x = self.width // 2
        center_y = self.height // 2
        max_radius = min(self.width, self.height) // 2
        
        for i in range(max_radius, 0, -2):
            alpha = int(current_alpha * (1 - i / max_radius) * 0.5)
            color_with_alpha = (*self.color, alpha)
            
            # Create temporary surface for alpha blending
            temp_surface = pygame.Surface((i * 2, i * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, color_with_alpha, (i, i), i)
            
            nebula_surface.blit(temp_surface, (center_x - i, center_y - i), special_flags=pygame.BLEND_ALPHA_SDL2)
        
        # Blit nebula to screen
        screen.blit(nebula_surface, (int(self.x), int(self.y)), special_flags=pygame.BLEND_ADD)

class Planet:
    """Distant planet in the background."""
    
    def __init__(self, x, y, radius, color, speed):
        """Initialize a planet."""
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.rotation = 0
        self.rotation_speed = random.uniform(0.1, 0.3)
    
    def update(self, dt):
        """Update planet position and rotation."""
        self.y += self.speed * dt
        self.rotation += self.rotation_speed * dt
    
    def draw(self, screen):
        """Draw the planet."""
        # Main planet body
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Add some surface details (darker bands)
        for i in range(2, 4):
            band_y = int(self.y + math.sin(self.rotation + i) * self.radius * 0.3)
            if abs(band_y - self.y) < self.radius:
                band_width = int(math.sqrt(self.radius**2 - (band_y - self.y)**2) * 2)
                darker_color = tuple(max(0, c - 30) for c in self.color)
                
                band_rect = pygame.Rect(int(self.x - band_width // 2), band_y - 2, band_width, 4)
                pygame.draw.rect(screen, darker_color, band_rect)

class ShootingStar:
    """Shooting star effect."""
    
    def __init__(self, x, y, velocity_x, velocity_y, length, color):
        """Initialize a shooting star."""
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.length = length
        self.color = color
        self.life = 1.0
        self.fade_speed = random.uniform(0.5, 1.0)
    
    def update(self, dt):
        """Update shooting star position and life."""
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.life -= self.fade_speed * dt
    
    def draw(self, screen):
        """Draw the shooting star."""
        if self.life <= 0:
            return
        
        # Calculate trail positions
        trail_points = []
        for i in range(self.length):
            trail_x = self.x - (self.velocity_x * i * 0.01)
            trail_y = self.y - (self.velocity_y * i * 0.01)
            trail_points.append((trail_x, trail_y))
        
        # Draw trail with fading effect
        for i, (trail_x, trail_y) in enumerate(trail_points):
            alpha = int(255 * self.life * (1 - i / self.length))
            if alpha > 0:
                color_with_alpha = (*self.color, alpha)
                
                # Create small surface for alpha blending
                star_surface = pygame.Surface((3, 3), pygame.SRCALPHA)
                pygame.draw.circle(star_surface, color_with_alpha, (1, 1), 1)
                screen.blit(star_surface, (int(trail_x), int(trail_y)), special_flags=pygame.BLEND_ADD)

class SpaceBackground:
    """Main space background system."""
    
    def __init__(self, width, height):
        """Initialize the space background."""
        self.width = width
        self.height = height
        
        # Background elements
        self.stars = []
        self.nebulae = []
        self.planets = []
        self.shooting_stars = []
        
        # Timers
        self.shooting_star_timer = 0
        self.shooting_star_interval = random.uniform(3.0, 8.0)
        
        # Colors
        self.space_colors = {
            'deep_space': (5, 5, 15),
            'nebula_blue': (30, 50, 120),
            'nebula_purple': (80, 30, 120),
            'nebula_pink': (120, 30, 80),
            'nebula_green': (30, 120, 50),
            'planet_red': (150, 80, 60),
            'planet_blue': (60, 100, 150),
            'planet_green': (80, 150, 90),
            'planet_orange': (180, 120, 60),
            'star_white': (255, 255, 255),
            'star_blue': (200, 220, 255),
            'star_yellow': (255, 255, 200)
        }
        
        # Initialize background elements
        self._create_initial_stars()
        self._create_initial_nebulae()
        self._create_initial_planets()
    
    def _create_initial_stars(self):
        """Create initial star field."""
        # Small distant stars
        for _ in range(200):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            size = 1
            brightness = random.randint(100, 200)
            speed = random.uniform(10, 30)
            self.stars.append(Star(x, y, size, brightness, speed))
        
        # Medium stars
        for _ in range(50):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            size = 2
            brightness = random.randint(150, 255)
            speed = random.uniform(20, 50)
            self.stars.append(Star(x, y, size, brightness, speed))
        
        # Large bright stars
        for _ in range(20):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            size = 3
            brightness = 255
            speed = random.uniform(30, 70)
            self.stars.append(Star(x, y, size, brightness, speed))
    
    def _create_initial_nebulae(self):
        """Create initial nebulae."""
        for _ in range(3):
            x = random.uniform(-100, self.width + 100)
            y = random.uniform(-200, self.height)
            width = random.randint(200, 400)
            height = random.randint(150, 300)
            color_name = random.choice(['nebula_blue', 'nebula_purple', 'nebula_pink', 'nebula_green'])
            color = self.space_colors[color_name]
            speed = random.uniform(5, 15)
            self.nebulae.append(Nebula(x, y, width, height, color, speed))
    
    def _create_initial_planets(self):
        """Create initial planets."""
        for _ in range(2):
            x = random.uniform(50, self.width - 50)
            y = random.uniform(-300, self.height)
            radius = random.randint(30, 80)
            color_name = random.choice(['planet_red', 'planet_blue', 'planet_green', 'planet_orange'])
            color = self.space_colors[color_name]
            speed = random.uniform(8, 25)
            self.planets.append(Planet(x, y, radius, color, speed))
    
    def _spawn_new_elements(self, dt):
        """Spawn new background elements as needed."""
        # Spawn new stars
        if len(self.stars) < 270:
            if random.random() < 0.3:
                x = random.uniform(0, self.width)
                y = -10
                size = random.choice([1, 1, 1, 2, 2, 3])  # Weighted towards smaller stars
                brightness = random.randint(100, 255)
                speed = random.uniform(10, 70)
                self.stars.append(Star(x, y, size, brightness, speed))
        
        # Spawn new nebulae
        if len(self.nebulae) < 4:
            if random.random() < 0.01:
                x = random.uniform(-100, self.width + 100)
                y = -300
                width = random.randint(200, 400)
                height = random.randint(150, 300)
                color_name = random.choice(['nebula_blue', 'nebula_purple', 'nebula_pink', 'nebula_green'])
                color = self.space_colors[color_name]
                speed = random.uniform(5, 15)
                self.nebulae.append(Nebula(x, y, width, height, color, speed))
        
        # Spawn new planets
        if len(self.planets) < 3:
            if random.random() < 0.005:
                x = random.uniform(50, self.width - 50)
                y = -200
                radius = random.randint(30, 80)
                color_name = random.choice(['planet_red', 'planet_blue', 'planet_green', 'planet_orange'])
                color = self.space_colors[color_name]
                speed = random.uniform(8, 25)
                self.planets.append(Planet(x, y, radius, color, speed))
        
        # Spawn shooting stars
        self.shooting_star_timer += dt
        if self.shooting_star_timer >= self.shooting_star_interval:
            self.shooting_star_timer = 0
            self.shooting_star_interval = random.uniform(3.0, 8.0)
            
            # Create shooting star
            x = random.uniform(-50, self.width + 50)
            y = random.uniform(-50, self.height // 2)
            velocity_x = random.uniform(100, 300)
            velocity_y = random.uniform(150, 400)
            length = random.randint(10, 20)
            color = random.choice([self.space_colors['star_white'], 
                                 self.space_colors['star_blue'], 
                                 self.space_colors['star_yellow']])
            self.shooting_stars.append(ShootingStar(x, y, velocity_x, velocity_y, length, color))
    
    def _cleanup_elements(self):
        """Remove elements that have moved off screen."""
        # Remove off-screen stars
        self.stars = [star for star in self.stars if star.y < self.height + 50]
        
        # Remove off-screen nebulae
        self.nebulae = [nebula for nebula in self.nebulae if nebula.y < self.height + 200]
        
        # Remove off-screen planets
        self.planets = [planet for planet in self.planets if planet.y < self.height + 200]
        
        # Remove dead shooting stars
        self.shooting_stars = [star for star in self.shooting_stars 
                             if star.life > 0 and star.x < self.width + 100 and star.y < self.height + 100]
    
    def update(self, dt):
        """Update all background elements."""
        # Update all elements
        for star in self.stars:
            star.update(dt)
        
        for nebula in self.nebulae:
            nebula.update(dt)
        
        for planet in self.planets:
            planet.update(dt)
        
        for shooting_star in self.shooting_stars:
            shooting_star.update(dt)
        
        # Spawn new elements and cleanup
        self._spawn_new_elements(dt)
        self._cleanup_elements()
    
    def draw(self, screen):
        """Draw the space background."""
        # Fill with deep space color
        screen.fill(self.space_colors['deep_space'])
        
        # Draw nebulae first (background layer)
        for nebula in self.nebulae:
            nebula.draw(screen)
        
        # Draw planets
        for planet in self.planets:
            planet.draw(screen)
        
        # Draw stars
        for star in self.stars:
            star.draw(screen)
        
        # Draw shooting stars (foreground layer)
        for shooting_star in self.shooting_stars:
            shooting_star.draw(screen)
    
    def get_parallax_offset(self, layer_speed=1.0):
        """Get parallax scrolling offset for UI elements."""
        # This can be used to create parallax effects for UI elements
        return 0  # Placeholder for future parallax UI effects
