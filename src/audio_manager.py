"""
Audio manager for QGamen_DanmakuShooting
Handles BGM and sound effects using audio files
"""

import pygame
import os
import random

class AudioManager:
    """Manages all audio including BGM and sound effects."""
    
    def __init__(self):
        """Initialize the audio manager."""
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.audio_enabled = True
            print("✅ Audio system initialized")
        except pygame.error as e:
            print(f"⚠️ Audio initialization failed: {e}")
            self.audio_enabled = False
        
        self.current_bgm = None
        self.current_bgm_name = None
        self.bgm_volume = 0.7
        self.sfx_volume = 0.8
        
        # Audio file paths
        self.assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'audio')
        self.bgm_dir = os.path.join(self.assets_dir, 'bgm')
        self.sfx_dir = os.path.join(self.assets_dir, 'sfx')
        
        # BGM tracks
        self.bgm_files = {
            'menu': 'menu_bgm.wav',
            'game': 'game_bgm.wav',
            'game_over': 'game_over_bgm.wav',
            'ranking': 'ranking_bgm.wav'
        }
        
        # Sound effect files
        self.sfx_files = {
            'shoot': 'shoot.wav',
            'explosion': 'explosion.wav',
            'bomb': 'bomb.wav',
            'item': 'item_collect.wav',
            'player_hit': 'player_hit.wav',
            'enemy_spawn': 'enemy_spawn.wav',
            'menu_select': 'menu_select.wav',
            'menu_move': 'menu_move.wav'
        }
        
        # Loaded sound effects cache
        self.sfx_cache = {}
        
        # Load sound effects
        self._load_sound_effects()
        
        # Check for audio files
        self._check_audio_files()
    
    def _check_audio_files(self):
        """Check if audio files exist."""
        if not os.path.exists(self.assets_dir):
            print("⚠️ Audio assets directory not found")
            print(f"Expected: {self.assets_dir}")
            print("Run 'python generate_audio_files.py' to create audio files")
            return
        
        # Check BGM files
        missing_bgm = []
        for name, filename in self.bgm_files.items():
            filepath = os.path.join(self.bgm_dir, filename)
            if not os.path.exists(filepath):
                missing_bgm.append(filename)
        
        # Check SFX files
        missing_sfx = []
        for name, filename in self.sfx_files.items():
            filepath = os.path.join(self.sfx_dir, filename)
            if not os.path.exists(filepath):
                missing_sfx.append(filename)
        
        if missing_bgm or missing_sfx:
            print("⚠️ Some audio files are missing:")
            if missing_bgm:
                print(f"  BGM: {', '.join(missing_bgm)}")
            if missing_sfx:
                print(f"  SFX: {', '.join(missing_sfx)}")
            print("Run 'python generate_audio_files.py' to create missing files")
        else:
            print("✅ All audio files found")
    
    def _load_sound_effects(self):
        """Load sound effects into cache."""
        if not self.audio_enabled:
            return
        
        for sfx_name, filename in self.sfx_files.items():
            filepath = os.path.join(self.sfx_dir, filename)
            try:
                if os.path.exists(filepath):
                    sound = pygame.mixer.Sound(filepath)
                    sound.set_volume(self.sfx_volume)
                    self.sfx_cache[sfx_name] = sound
                    print(f"✅ Loaded SFX: {sfx_name}")
                else:
                    print(f"⚠️ SFX file not found: {filename}")
            except Exception as e:
                print(f"⚠️ Failed to load SFX {sfx_name}: {e}")
    
    def play_bgm(self, track_name, loops=-1):
        """Play background music."""
        if not self.audio_enabled:
            return
        
        # Don't restart the same BGM
        if self.current_bgm_name == track_name and pygame.mixer.music.get_busy():
            return
        
        try:
            if track_name in self.bgm_files:
                filepath = os.path.join(self.bgm_dir, self.bgm_files[track_name])
                
                if os.path.exists(filepath):
                    # Stop current BGM
                    pygame.mixer.music.stop()
                    
                    # Load and play new BGM
                    pygame.mixer.music.load(filepath)
                    pygame.mixer.music.set_volume(self.bgm_volume)
                    pygame.mixer.music.play(loops=loops)
                    
                    self.current_bgm_name = track_name
                    print(f"🎵 Playing BGM: {track_name}")
                else:
                    print(f"⚠️ BGM file not found: {self.bgm_files[track_name]}")
            else:
                print(f"⚠️ BGM track not found: {track_name}")
        except Exception as e:
            print(f"⚠️ Failed to play BGM {track_name}: {e}")
    
    def stop_bgm(self):
        """Stop background music."""
        if not self.audio_enabled:
            return
        
        try:
            pygame.mixer.music.stop()
            self.current_bgm_name = None
            print("🔇 BGM stopped")
        except Exception as e:
            print(f"⚠️ Failed to stop BGM: {e}")
    
    def set_bgm_volume(self, volume):
        """Set BGM volume (0.0 to 1.0)."""
        self.bgm_volume = max(0.0, min(1.0, volume))
        
        try:
            pygame.mixer.music.set_volume(self.bgm_volume)
        except Exception as e:
            print(f"⚠️ Failed to set BGM volume: {e}")
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))
        
        # Update volume for all cached sound effects
        for sound in self.sfx_cache.values():
            sound.set_volume(self.sfx_volume)
    
    def play_sfx(self, sfx_name):
        """Play sound effect."""
        if not self.audio_enabled:
            return
        
        try:
            if sfx_name in self.sfx_cache:
                self.sfx_cache[sfx_name].play()
            else:
                print(f"⚠️ SFX not found: {sfx_name}")
        except Exception as e:
            print(f"⚠️ Failed to play SFX {sfx_name}: {e}")
    
    def play_sfx_with_variation(self, sfx_name, pitch_variation=0.1):
        """Play sound effect with pitch variation."""
        if not self.audio_enabled:
            return
        
        try:
            if sfx_name in self.sfx_cache:
                # Create a copy of the sound for pitch variation
                sound = self.sfx_cache[sfx_name]
                
                # Play with slight pitch variation (if supported)
                sound.play()
                
                # Note: pygame doesn't support real-time pitch shifting
                # This is a placeholder for potential future enhancement
            else:
                print(f"⚠️ SFX not found: {sfx_name}")
        except Exception as e:
            print(f"⚠️ Failed to play SFX {sfx_name}: {e}")
    
    def is_bgm_playing(self):
        """Check if BGM is currently playing."""
        if not self.audio_enabled:
            return False
        
        try:
            return pygame.mixer.music.get_busy()
        except:
            return False
    
    def get_bgm_position(self):
        """Get current BGM position (if supported)."""
        if not self.audio_enabled:
            return 0
        
        try:
            return pygame.mixer.music.get_pos()
        except:
            return 0
    
    def fade_out_bgm(self, fade_time_ms=1000):
        """Fade out current BGM."""
        if not self.audio_enabled:
            return
        
        try:
            pygame.mixer.music.fadeout(fade_time_ms)
            print(f"🔉 BGM fading out over {fade_time_ms}ms")
        except Exception as e:
            print(f"⚠️ Failed to fade out BGM: {e}")
    
    def pause_bgm(self):
        """Pause current BGM."""
        if not self.audio_enabled:
            return
        
        try:
            pygame.mixer.music.pause()
            print("⏸️ BGM paused")
        except Exception as e:
            print(f"⚠️ Failed to pause BGM: {e}")
    
    def resume_bgm(self):
        """Resume paused BGM."""
        if not self.audio_enabled:
            return
        
        try:
            pygame.mixer.music.unpause()
            print("▶️ BGM resumed")
        except Exception as e:
            print(f"⚠️ Failed to resume BGM: {e}")

# Global audio manager instance
audio_manager = AudioManager()
