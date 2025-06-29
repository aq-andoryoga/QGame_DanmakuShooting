"""
Main Game class for QGamen_DanmakuShooting
"""

import pygame
import sys
import json
import os
import math
import threading
from player import Player
from enemy import EnemyManager
from bullet import BulletManager
from ui import UI
from effects import EffectManager
from ranking import RankingManager
from items import ItemManager
from audio_manager import audio_manager
from audio_generator import AudioGenerator, check_audio_files_exist
from space_background import SpaceBackground

class GameState:
    """Game state enumeration."""
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    RANKING = 3
    NAME_INPUT = 4
    AUDIO_GENERATION = 5  # New state for audio generation

class Game:
    """Main game class that handles the game loop and state management."""
    
    def __init__(self):
        """Initialize the game."""
        # Screen settings - 修正: 画面サイズを小さく
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.GAME_AREA_WIDTH = int(self.SCREEN_WIDTH * 2 / 3)  # Left 2/3 for game
        self.UI_AREA_WIDTH = self.SCREEN_WIDTH - self.GAME_AREA_WIDTH  # Right 1/3 for UI
        self.FPS = 60
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("QGame - スペースサバイバル")
        
        # Initialize clock
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
        self.state = GameState.MENU
        self.previous_state = None
        
        # Game objects
        self.player = None
        self.enemy_manager = None
        self.bullet_manager = None
        self.effect_manager = None
        self.item_manager = None
        self.ui = None
        self.ranking_manager = RankingManager()
        self.audio_manager = audio_manager
        self.space_background = SpaceBackground(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        # Game variables
        self.score = 0
        self.lives = 3
        self.special_attacks = 2  # 1ライフあたり2個まで
        self.max_special_per_life = 2  # 1ライフあたりの最大爆弾数
        self.game_over_timer = 0
        self.game_time = 0  # ゲーム経過時間
        
        # Audio generation variables
        self.audio_generation_progress = 0
        self.audio_generation_total = 0
        self.audio_generation_message = ""
        self.audio_generation_complete = False
        self.audio_generator = None
        
        # Initialize fonts with Japanese support
        from font_manager import font_manager
        self.font_manager = font_manager
        self.font_large = self.font_manager.get_font(72)
        self.font_medium = self.font_manager.get_font(48)
        self.font_small = self.font_manager.get_font(36)
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (128, 128, 128)
        self.YELLOW = (255, 255, 0)
        
        # Check if audio files exist, if not, generate them
        self._check_and_generate_audio_files()
        
    def init_game(self):
        """Initialize game objects for a new game."""
        self.player = Player(self.GAME_AREA_WIDTH // 2, self.SCREEN_HEIGHT - 100)
        self.player.set_boundaries(self.GAME_AREA_WIDTH, self.SCREEN_HEIGHT)
        
        self.enemy_manager = EnemyManager(self.GAME_AREA_WIDTH, self.SCREEN_HEIGHT)
        self.bullet_manager = BulletManager()
        self.effect_manager = EffectManager()
        self.item_manager = ItemManager()
        self.ui = UI(self.GAME_AREA_WIDTH, self.UI_AREA_WIDTH, self.SCREEN_HEIGHT)
        self.score = 0
        self.lives = 3
        self.special_attacks = 2  # 1ライフあたり2個まで
        self.game_time = 0
        
    def _check_and_generate_audio_files(self):
        """Check if audio files exist and generate them if needed."""
        files_exist, missing_files = check_audio_files_exist()
        
        if not files_exist:
            print(f"⚠️ Missing audio files: {len(missing_files)} files")
            print("🎵 Starting audio file generation...")
            self.change_state(GameState.AUDIO_GENERATION)
            self._start_audio_generation()
        else:
            print("✅ All audio files found")
            # Start menu BGM
            self.audio_manager.play_bgm('menu')
    
    def _start_audio_generation(self):
        """Start audio file generation in a separate thread."""
        self.audio_generator = AudioGenerator(callback=self._audio_generation_callback)
        
        # Start generation in a separate thread to avoid blocking the UI
        generation_thread = threading.Thread(target=self._generate_audio_files_thread)
        generation_thread.daemon = True
        generation_thread.start()
    
    def _audio_generation_callback(self, message, current, total):
        """Callback function for audio generation progress."""
        self.audio_generation_message = message
        self.audio_generation_progress = current
        self.audio_generation_total = total
        
        if current >= total:
            self.audio_generation_complete = True
    
    def _generate_audio_files_thread(self):
        """Generate audio files in a separate thread."""
        try:
            success = self.audio_generator.generate_all_audio()
            if success:
                self.audio_generation_complete = True
                print("✅ Audio file generation completed successfully")
            else:
                print("❌ Audio file generation failed")
        except Exception as e:
            print(f"❌ Audio file generation error: {e}")
            self.audio_generation_complete = True
        
    def change_state(self, new_state):
        """Change game state and update BGM accordingly."""
        if self.state != new_state:
            self.previous_state = self.state
            self.state = new_state
            
            # Change BGM based on new state
            if new_state == GameState.MENU:
                self.audio_manager.play_bgm('menu')
            elif new_state == GameState.PLAYING:
                self.audio_manager.play_bgm('game')
            elif new_state == GameState.GAME_OVER:
                self.audio_manager.play_bgm('game_over', loops=0)  # Play once
            elif new_state == GameState.RANKING:
                self.audio_manager.play_bgm('ranking')
            elif new_state == GameState.NAME_INPUT:
                self.audio_manager.play_bgm('ranking')  # Same as ranking
            elif new_state == GameState.AUDIO_GENERATION:
                # No BGM during audio generation
                self.audio_manager.stop_bgm()
        
    def handle_events(self):
        """Handle all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.change_state(GameState.MENU)
                    else:
                        self.running = False
                elif self.state == GameState.MENU:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.audio_manager.play_sfx('menu_select')
                        self.init_game()
                        self.change_state(GameState.PLAYING)
                    elif event.key == pygame.K_r:
                        self.audio_manager.play_sfx('menu_select')
                        self.change_state(GameState.RANKING)
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.audio_manager.play_sfx('menu_select')
                        if self.ranking_manager.is_high_score(self.score):
                            self.change_state(GameState.NAME_INPUT)
                        else:
                            self.change_state(GameState.MENU)
                elif self.state == GameState.RANKING:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        self.audio_manager.play_sfx('menu_select')
                        self.change_state(GameState.MENU)
                elif self.state == GameState.NAME_INPUT:
                    self.ranking_manager.handle_name_input(event, self.score)
                    if self.ranking_manager.name_input_complete:
                        self.audio_manager.play_sfx('menu_select')
                        self.change_state(GameState.MENU)
                elif self.state == GameState.AUDIO_GENERATION:
                    if event.key == pygame.K_RETURN and self.audio_generation_complete:
                        self.audio_manager.play_sfx('menu_select')
                        # Reload audio manager to use the new files
                        self.audio_manager = audio_manager
                        self.audio_manager.play_bgm('menu')
                        self.change_state(GameState.MENU)
    
    def update(self):
        """Update game logic."""
        dt = self.clock.get_time() / 1000.0  # Delta time in seconds
        
        # Update space background
        self.space_background.update(dt)
        
        if self.state == GameState.PLAYING:
            self.game_time += 1
            
            # Update player
            keys = pygame.key.get_pressed()
            self.player.update(keys)
            
            # Update enemies
            self.enemy_manager.update(self.game_time)
            
            # Update bullets
            self.bullet_manager.update()
            
            # Update effects
            self.effect_manager.update()
            
            # Update items
            self.item_manager.update()
            
            # Handle player shooting
            if keys[pygame.K_SPACE]:
                player_bullet = self.player.shoot()
                if player_bullet:
                    self.bullet_manager.add_player_bullet(player_bullet)
                    # Play shooting sound effect
                    self.audio_manager.play_sfx('shoot')
            
            # Handle special attack - 修正: 爆弾型必殺技
            if keys[pygame.K_x] and self.special_attacks > 0:
                bomb_data = self.player.special_attack()
                if bomb_data:
                    # Create bomb explosion
                    self.effect_manager.add_bomb_explosion(bomb_data['x'], bomb_data['y'], bomb_data['radius'])
                    self.special_attacks -= 1
                    # Play bomb sound effect
                    self.audio_manager.play_sfx('bomb')
                    
                    # Debug: 爆弾使用をコンソールに出力
                    print(f"爆弾使用！残り: {self.special_attacks}/2")
                    # Play bomb sound effect
                    self.audio_manager.play_sfx('bomb')
            
            # Enemy shooting
            enemy_bullets = self.enemy_manager.get_bullets()
            for bullet in enemy_bullets:
                self.bullet_manager.add_enemy_bullet(bullet)
            
            # Collision detection
            self.check_collisions()
            
            # Check game over
            if self.lives <= 0:
                self.change_state(GameState.GAME_OVER)
                self.game_over_timer = pygame.time.get_ticks()
        
        elif self.state == GameState.GAME_OVER:
            # Auto transition after 3 seconds if not high score
            if pygame.time.get_ticks() - self.game_over_timer > 3000:
                if not self.ranking_manager.is_high_score(self.score):
                    self.change_state(GameState.MENU)
        
        elif self.state == GameState.AUDIO_GENERATION:
            # Check if audio generation is complete
            if self.audio_generation_complete and not hasattr(self, '_audio_completion_handled'):
                self._audio_completion_handled = True
                print("🎵 Audio generation completed, ready to continue")
    
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
                    # Play explosion sound effect
                    self.audio_manager.play_sfx('explosion')
                    
                    # 修正: アイテムドロップ追加
                    item_count = enemy.get_item_drop_count()
                    for _ in range(item_count):
                        self.item_manager.add_score_item(enemy.x, enemy.y)
                    break
        
        # Bomb explosions vs enemies and bullets
        active_bombs = self.effect_manager.get_active_bomb_explosions()
        for bomb in active_bombs:
            bomb_radius = bomb.get_damage_radius()
            
            # Bomb vs enemies
            for enemy in self.enemy_manager.enemies[:]:
                distance = math.sqrt((enemy.x - bomb.x)**2 + (enemy.y - bomb.y)**2)
                if distance <= bomb_radius:
                    self.enemy_manager.enemies.remove(enemy)
                    self.effect_manager.add_explosion(enemy.x, enemy.y)
                    self.score += 100
                    # Play explosion sound effect
                    self.audio_manager.play_sfx('explosion')
                    
                    # アイテムドロップ
                    item_count = enemy.get_item_drop_count()
                    for _ in range(item_count):
                        self.item_manager.add_score_item(enemy.x, enemy.y)
            
            # Bomb vs enemy bullets
            for bullet in self.bullet_manager.enemy_bullets[:]:
                distance = math.sqrt((bullet.x - bomb.x)**2 + (bullet.y - bomb.y)**2)
                if distance <= bomb_radius:
                    self.bullet_manager.enemy_bullets.remove(bullet)
        
        # Enemy bullets vs player
        if not self.player.invulnerable:
            for bullet in self.bullet_manager.enemy_bullets[:]:
                if bullet.rect.colliderect(self.player.rect):
                    # Player hit
                    self.bullet_manager.enemy_bullets.remove(bullet)
                    self.lives -= 1
                    self.player.hit()
                    # Play player hit sound effect
                    self.audio_manager.play_sfx('player_hit')
                    
                    # 被弾時に爆弾を2個にリセット
                    self.special_attacks = self.max_special_per_life
                    
                    # Debug: 被弾時の爆弾リセットをコンソールに出力
                    print(f"被弾！爆弾リセット: {self.special_attacks}/2, 残りライフ: {self.lives}")
                    break
        
        # Player vs score items
        for item in self.item_manager.score_items[:]:
            if item.rect.colliderect(self.player.rect):
                self.item_manager.score_items.remove(item)
                self.score += 10
                # Play item collection sound effect
                self.audio_manager.play_sfx('item')
    
    def draw_menu(self):
        """Draw the main menu."""
        # Draw space background
        self.space_background.draw(self.screen)
        
        # Draw semi-transparent overlay for better text readability
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Title
        title = self.font_manager.render_text("QGame - スペースサバイバル", 48, self.WHITE)
        title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Menu options
        start_text = self.font_manager.render_text("Enterキーでゲーム開始", 32, self.WHITE)
        start_rect = start_text.get_rect(center=(self.SCREEN_WIDTH // 2, 300))
        self.screen.blit(start_text, start_rect)
        
        ranking_text = self.font_manager.render_text("Rキーでランキング表示", 32, self.WHITE)
        ranking_rect = ranking_text.get_rect(center=(self.SCREEN_WIDTH // 2, 350))
        self.screen.blit(ranking_text, ranking_rect)
        
        quit_text = self.font_manager.render_text("ESCキーで終了", 32, self.WHITE)
        quit_rect = quit_text.get_rect(center=(self.SCREEN_WIDTH // 2, 400))
        self.screen.blit(quit_text, quit_rect)
    
    def draw_game(self):
        """Draw the game screen."""
        # Fill screen with black first
        self.screen.fill((0, 0, 0))
        
        # Create clipping rectangle for game area
        game_rect = pygame.Rect(0, 0, self.GAME_AREA_WIDTH, self.SCREEN_HEIGHT)
        
        # Set clipping area for game objects
        self.screen.set_clip(game_rect)
        
        # Draw space background (clipped to game area)
        # Create a temporary surface for the game area background
        game_bg_surface = pygame.Surface((self.GAME_AREA_WIDTH, self.SCREEN_HEIGHT))
        game_bg_surface.fill((0, 0, 0))  # Black background
        
        # Draw stars only in game area
        for star in self.space_background.stars:
            if star.x < self.GAME_AREA_WIDTH:  # Only draw stars in game area
                star.draw(game_bg_surface)
        
        # Draw nebulae in game area
        for nebula in self.space_background.nebulae:
            if nebula.x < self.GAME_AREA_WIDTH:
                nebula.draw(game_bg_surface)
        
        # Draw planets in game area
        for planet in self.space_background.planets:
            if planet.x < self.GAME_AREA_WIDTH:
                planet.draw(game_bg_surface)
        
        self.screen.blit(game_bg_surface, (0, 0))
        
        # Draw game objects (clipped to game area)
        self.player.draw(self.screen)
        self.enemy_manager.draw(self.screen)
        self.bullet_manager.draw(self.screen)
        self.effect_manager.draw(self.screen)
        self.item_manager.draw(self.screen)
        
        # Remove clipping
        self.screen.set_clip(None)
        
        # Draw game area border
        pygame.draw.line(self.screen, (100, 150, 255), 
                        (self.GAME_AREA_WIDTH, 0), 
                        (self.GAME_AREA_WIDTH, self.SCREEN_HEIGHT), 3)
        
        # Draw UI area background
        ui_rect = pygame.Rect(self.GAME_AREA_WIDTH, 0, self.UI_AREA_WIDTH, self.SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, (10, 10, 30), ui_rect)
        
        # Draw UI
        self.ui.draw(self.screen, self.score, self.lives, self.special_attacks)
    
    def draw_game_over(self):
        """Draw the game over screen."""
        # Draw space background
        self.space_background.draw(self.screen)
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.font_manager.render_text("ゲームオーバー", 48, self.RED)
        game_over_rect = game_over_text.get_rect(center=(self.SCREEN_WIDTH // 2, 200))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Score
        score_text = self.font_manager.render_text(f"最終スコア: {self.score}", 32, self.WHITE)
        score_rect = score_text.get_rect(center=(self.SCREEN_WIDTH // 2, 280))
        self.screen.blit(score_text, score_rect)
        
        # Continue instruction
        if self.ranking_manager.is_high_score(self.score):
            continue_text = self.font_manager.render_text("Enterキーで名前を入力", 28, self.WHITE)
        else:
            continue_text = self.font_manager.render_text("Enterキーで続行", 28, self.WHITE)
        continue_rect = continue_text.get_rect(center=(self.SCREEN_WIDTH // 2, 350))
        self.screen.blit(continue_text, continue_rect)
    
    def draw_ranking(self):
        """Draw the ranking screen."""
        # Draw space background
        self.space_background.draw(self.screen)
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        overlay.set_alpha(120)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Title
        title = self.font_manager.render_text("ハイスコア", 48, self.WHITE)
        title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Rankings
        rankings = self.ranking_manager.get_rankings()
        for i, (name, score) in enumerate(rankings):
            rank_text = self.font_manager.render_text(f"{i+1:2d}位. {name:<10} {score:>6d}点", 32, self.WHITE)
            rank_rect = rank_text.get_rect(center=(self.SCREEN_WIDTH // 2, 150 + i * 35))
            self.screen.blit(rank_text, rank_rect)
        
        # Back instruction
        back_text = self.font_manager.render_text("EnterまたはESCキーで戻る", 28, self.WHITE)
        back_rect = back_text.get_rect(center=(self.SCREEN_WIDTH // 2, 550))
        self.screen.blit(back_text, back_rect)
    
    def draw_name_input(self):
        """Draw the name input screen."""
        # Draw space background
        self.space_background.draw(self.screen)
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        overlay.set_alpha(120)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Title
        title = self.font_manager.render_text("新記録達成！", 48, self.GREEN)
        title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Score
        score_text = self.font_manager.render_text(f"スコア: {self.score}点", 32, self.WHITE)
        score_rect = score_text.get_rect(center=(self.SCREEN_WIDTH // 2, 220))
        self.screen.blit(score_text, score_rect)
        
        # Name input
        name_prompt = self.font_manager.render_text("名前を入力してください:", 32, self.WHITE)
        name_prompt_rect = name_prompt.get_rect(center=(self.SCREEN_WIDTH // 2, 300))
        self.screen.blit(name_prompt, name_prompt_rect)
        
        name_text = self.font_manager.render_text(self.ranking_manager.current_name + "_", 36, self.WHITE)
        name_rect = name_text.get_rect(center=(self.SCREEN_WIDTH // 2, 350))
        self.screen.blit(name_text, name_rect)
        
        # Instructions
        instruction = self.font_manager.render_text("Enterキーで決定", 28, self.WHITE)
        instruction_rect = instruction.get_rect(center=(self.SCREEN_WIDTH // 2, 420))
        self.screen.blit(instruction, instruction_rect)
    
    def draw_audio_generation(self):
        """Draw the audio generation screen."""
        # Draw space background
        self.space_background.draw(self.screen)
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Title
        title = self.font_manager.render_text("初回セットアップ", 48, self.WHITE)
        title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Message
        if self.audio_generation_message:
            message = self.font_manager.render_text(self.audio_generation_message, 28, self.WHITE)
            message_rect = message.get_rect(center=(self.SCREEN_WIDTH // 2, 250))
            self.screen.blit(message, message_rect)
        
        # Progress bar
        if self.audio_generation_total > 0:
            progress_width = 400
            progress_height = 30
            progress_x = (self.SCREEN_WIDTH - progress_width) // 2
            progress_y = 320
            
            # Background
            pygame.draw.rect(self.screen, self.GRAY, 
                           (progress_x, progress_y, progress_width, progress_height))
            
            # Progress fill
            if self.audio_generation_progress > 0:
                fill_width = int((self.audio_generation_progress / self.audio_generation_total) * progress_width)
                pygame.draw.rect(self.screen, self.GREEN, 
                               (progress_x, progress_y, fill_width, progress_height))
            
            # Progress text
            progress_text = f"{self.audio_generation_progress}/{self.audio_generation_total}"
            progress_label = self.font_manager.render_text(progress_text, 24, self.WHITE)
            progress_label_rect = progress_label.get_rect(center=(self.SCREEN_WIDTH // 2, progress_y + progress_height + 30))
            self.screen.blit(progress_label, progress_label_rect)
        
        # Instructions
        if self.audio_generation_complete:
            complete_text = self.font_manager.render_text("完了！Enterキーで続行", 28, self.GREEN)
            complete_rect = complete_text.get_rect(center=(self.SCREEN_WIDTH // 2, 450))
            self.screen.blit(complete_text, complete_rect)
        else:
            wait_text = self.font_manager.render_text("音声ファイルを生成しています...", 20, self.YELLOW)
            wait_rect = wait_text.get_rect(center=(self.SCREEN_WIDTH // 2, 450))
            self.screen.blit(wait_text, wait_rect)
    
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
        elif self.state == GameState.AUDIO_GENERATION:
            self.draw_audio_generation()
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
