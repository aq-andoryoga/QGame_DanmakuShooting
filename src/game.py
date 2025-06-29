"""
Main Game class for QGamen_DanmakuShooting
"""

import pygame
import sys
import json
import os
from player import Player
from enemy import EnemyManager
from bullet import BulletManager
from ui import UI
from effects import EffectManager
from ranking import RankingManager

class GameState:
    """Game state enumeration."""
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    RANKING = 3
    NAME_INPUT = 4

class Game:
    """Main game class that handles the game loop and state management."""
    
    def __init__(self):
        """Initialize the game."""
        # Screen settings
        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080
        self.GAME_AREA_WIDTH = int(self.SCREEN_WIDTH * 2 / 3)  # Left 2/3 for game
        self.UI_AREA_WIDTH = self.SCREEN_WIDTH - self.GAME_AREA_WIDTH  # Right 1/3 for UI
        self.FPS = 60
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("QGamen - Danmaku Shooting")
        
        # Initialize clock
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
        self.state = GameState.MENU
        
        # Game objects
        self.player = None
        self.enemy_manager = None
        self.bullet_manager = None
        self.effect_manager = None
        self.ui = None
        self.ranking_manager = RankingManager()
        
        # Game variables
        self.score = 0
        self.lives = 3
        self.game_over_timer = 0
        
        # Initialize fonts
        pygame.font.init()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (128, 128, 128)
        
    def init_game(self):
        """Initialize game objects for a new game."""
        self.player = Player(self.GAME_AREA_WIDTH // 2, self.SCREEN_HEIGHT - 100)
        self.enemy_manager = EnemyManager(self.GAME_AREA_WIDTH, self.SCREEN_HEIGHT)
        self.bullet_manager = BulletManager()
        self.effect_manager = EffectManager()
        self.ui = UI(self.GAME_AREA_WIDTH, self.UI_AREA_WIDTH, self.SCREEN_HEIGHT)
        self.score = 0
        self.lives = 3
        
    def handle_events(self):
        """Handle all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.MENU
                    else:
                        self.running = False
                elif self.state == GameState.MENU:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.init_game()
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_r:
                        self.state = GameState.RANKING
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.ranking_manager.is_high_score(self.score):
                            self.state = GameState.NAME_INPUT
                        else:
                            self.state = GameState.MENU
                elif self.state == GameState.RANKING:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                elif self.state == GameState.NAME_INPUT:
                    self.ranking_manager.handle_name_input(event, self.score)
                    if self.ranking_manager.name_input_complete:
                        self.state = GameState.MENU
    
    def update(self):
        """Update game logic."""
        if self.state == GameState.PLAYING:
            # Update player
            keys = pygame.key.get_pressed()
            self.player.update(keys)
            
            # Update enemies
            self.enemy_manager.update()
            
            # Update bullets
            self.bullet_manager.update()
            
            # Update effects
            self.effect_manager.update()
            
            # Handle player shooting
            if keys[pygame.K_SPACE]:
                player_bullet = self.player.shoot()
                if player_bullet:
                    self.bullet_manager.add_player_bullet(player_bullet)
            
            # Enemy shooting
            enemy_bullets = self.enemy_manager.get_bullets()
            for bullet in enemy_bullets:
                self.bullet_manager.add_enemy_bullet(bullet)
            
            # Collision detection
            self.check_collisions()
            
            # Check game over
            if self.lives <= 0:
                self.state = GameState.GAME_OVER
                self.game_over_timer = pygame.time.get_ticks()
        
        elif self.state == GameState.GAME_OVER:
            # Auto transition after 3 seconds if not high score
            if pygame.time.get_ticks() - self.game_over_timer > 3000:
                if not self.ranking_manager.is_high_score(self.score):
                    self.state = GameState.MENU
    
    def check_collisions(self):
        """Check all collision detections."""
        # Player bullets vs enemies
        for bullet in self.bullet_manager.player_bullets[:]:
            for enemy in self.enemy_manager.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    # Enemy hit
                    self.bullet_manager.player_bullets.remove(bullet)
                    self.enemy_manager.enemies.remove(enemy)
                    self.effect_manager.add_explosion(enemy.x, enemy.y)
                    self.score += 100
                    break
        
        # Enemy bullets vs player
        if not self.player.invulnerable:
            for bullet in self.bullet_manager.enemy_bullets[:]:
                if bullet.rect.colliderect(self.player.rect):
                    # Player hit
                    self.bullet_manager.enemy_bullets.remove(bullet)
                    self.lives -= 1
                    self.player.hit()
                    break
    
    def draw_menu(self):
        """Draw the main menu."""
        self.screen.fill(self.BLACK)
        
        # Title
        title = self.font_large.render("QGamen - Danmaku Shooting", True, self.WHITE)
        title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)
        
        # Menu options
        start_text = self.font_medium.render("Press ENTER to Start", True, self.WHITE)
        start_rect = start_text.get_rect(center=(self.SCREEN_WIDTH // 2, 400))
        self.screen.blit(start_text, start_rect)
        
        ranking_text = self.font_medium.render("Press R for Rankings", True, self.WHITE)
        ranking_rect = ranking_text.get_rect(center=(self.SCREEN_WIDTH // 2, 500))
        self.screen.blit(ranking_text, ranking_rect)
        
        quit_text = self.font_medium.render("Press ESC to Quit", True, self.WHITE)
        quit_rect = quit_text.get_rect(center=(self.SCREEN_WIDTH // 2, 600))
        self.screen.blit(quit_text, quit_rect)
    
    def draw_game(self):
        """Draw the game screen."""
        self.screen.fill(self.BLACK)
        
        # Draw game area border
        pygame.draw.line(self.screen, self.WHITE, 
                        (self.GAME_AREA_WIDTH, 0), 
                        (self.GAME_AREA_WIDTH, self.SCREEN_HEIGHT), 2)
        
        # Draw game objects
        self.player.draw(self.screen)
        self.enemy_manager.draw(self.screen)
        self.bullet_manager.draw(self.screen)
        self.effect_manager.draw(self.screen)
        
        # Draw UI
        self.ui.draw(self.screen, self.score, self.lives)
    
    def draw_game_over(self):
        """Draw the game over screen."""
        self.screen.fill(self.BLACK)
        
        # Game Over text
        game_over_text = self.font_large.render("GAME OVER", True, self.RED)
        game_over_rect = game_over_text.get_rect(center=(self.SCREEN_WIDTH // 2, 300))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Score
        score_text = self.font_medium.render(f"Final Score: {self.score}", True, self.WHITE)
        score_rect = score_text.get_rect(center=(self.SCREEN_WIDTH // 2, 400))
        self.screen.blit(score_text, score_rect)
        
        # Continue instruction
        if self.ranking_manager.is_high_score(self.score):
            continue_text = self.font_small.render("Press ENTER to enter your name", True, self.WHITE)
        else:
            continue_text = self.font_small.render("Press ENTER to continue", True, self.WHITE)
        continue_rect = continue_text.get_rect(center=(self.SCREEN_WIDTH // 2, 500))
        self.screen.blit(continue_text, continue_rect)
    
    def draw_ranking(self):
        """Draw the ranking screen."""
        self.screen.fill(self.BLACK)
        
        # Title
        title = self.font_large.render("HIGH SCORES", True, self.WHITE)
        title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Rankings
        rankings = self.ranking_manager.get_rankings()
        for i, (name, score) in enumerate(rankings):
            rank_text = self.font_medium.render(f"{i+1:2d}. {name:<10} {score:>6d}", True, self.WHITE)
            rank_rect = rank_text.get_rect(center=(self.SCREEN_WIDTH // 2, 200 + i * 50))
            self.screen.blit(rank_text, rank_rect)
        
        # Back instruction
        back_text = self.font_small.render("Press ENTER or ESC to return", True, self.WHITE)
        back_rect = back_text.get_rect(center=(self.SCREEN_WIDTH // 2, 800))
        self.screen.blit(back_text, back_rect)
    
    def draw_name_input(self):
        """Draw the name input screen."""
        self.screen.fill(self.BLACK)
        
        # Title
        title = self.font_large.render("NEW HIGH SCORE!", True, self.GREEN)
        title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)
        
        # Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, self.WHITE)
        score_rect = score_text.get_rect(center=(self.SCREEN_WIDTH // 2, 300))
        self.screen.blit(score_text, score_rect)
        
        # Name input
        name_prompt = self.font_medium.render("Enter your name:", True, self.WHITE)
        name_prompt_rect = name_prompt.get_rect(center=(self.SCREEN_WIDTH // 2, 400))
        self.screen.blit(name_prompt, name_prompt_rect)
        
        name_text = self.font_medium.render(self.ranking_manager.current_name + "_", True, self.WHITE)
        name_rect = name_text.get_rect(center=(self.SCREEN_WIDTH // 2, 450))
        self.screen.blit(name_text, name_rect)
        
        # Instructions
        instruction = self.font_small.render("Press ENTER when done", True, self.WHITE)
        instruction_rect = instruction.get_rect(center=(self.SCREEN_WIDTH // 2, 550))
        self.screen.blit(instruction, instruction_rect)
    
    def draw(self):
        """Draw everything to the screen."""
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.state == GameState.RANKING:
            self.draw_ranking()
        elif self.state == GameState.NAME_INPUT:
            self.draw_name_input()
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
