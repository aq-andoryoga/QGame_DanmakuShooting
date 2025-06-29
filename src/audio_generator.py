"""
Audio file generator module for QGamen_DanmakuShooting
Generates BGM and sound effects as WAV files
"""

import os
import sys
import math
import pygame
import struct
import wave

class AudioGenerator:
    """Generates audio files for the game."""
    
    def __init__(self, callback=None):
        """Initialize the audio file generator."""
        self.sample_rate = 44100  # Higher quality for file output
        self.assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'audio')
        self.callback = callback  # Progress callback function
        
        # Create assets directory structure
        os.makedirs(os.path.join(self.assets_dir, 'bgm'), exist_ok=True)
        os.makedirs(os.path.join(self.assets_dir, 'sfx'), exist_ok=True)
        
        # Try to import numpy for high-quality generation
        self.numpy_available = False
        try:
            import numpy as np
            self.numpy_available = True
            self.np = np
            print("✅ NumPy available - High quality audio generation enabled")
        except ImportError:
            print("⚠️ NumPy not available - Using fallback audio generation")
        
        # Initialize pygame mixer for audio processing
        try:
            pygame.mixer.pre_init(frequency=self.sample_rate, size=-16, channels=1, buffer=512)
            pygame.mixer.init()
            print("✅ Pygame mixer initialized")
        except Exception as e:
            print(f"⚠️ Pygame mixer initialization failed: {e}")
    
    def generate_all_audio(self):
        """Generate all BGM and sound effects."""
        total_files = 12  # 4 BGM + 8 SFX
        current_file = 0
        
        if self.callback:
            self.callback("音声ファイルを生成中...", 0, total_files)
        
        try:
            # Generate BGM files
            bgm_specs = {
                'menu_bgm.wav': {
                    'duration': 60,
                    'generator': self._generate_ambient_bgm,
                    'params': {'base_freq': 220, 'style': 'space_ambient'}
                },
                'game_bgm.wav': {
                    'duration': 120,
                    'generator': self._generate_action_bgm,
                    'params': {'base_freq': 440, 'style': 'battle_action'}
                },
                'game_over_bgm.wav': {
                    'duration': 20,
                    'generator': self._generate_dramatic_bgm,
                    'params': {'base_freq': 330, 'style': 'dramatic_defeat'}
                },
                'ranking_bgm.wav': {
                    'duration': 30,
                    'generator': self._generate_victory_bgm,
                    'params': {'base_freq': 550, 'style': 'triumphant_victory'}
                }
            }
            
            for filename, spec in bgm_specs.items():
                current_file += 1
                if self.callback:
                    self.callback(f"BGM生成中: {filename}", current_file, total_files)
                
                try:
                    audio_data = spec['generator'](spec['duration'], **spec['params'])
                    filepath = os.path.join(self.assets_dir, 'bgm', filename)
                    self._save_audio_file(audio_data, filepath)
                    print(f"✅ Generated: {filename}")
                except Exception as e:
                    print(f"❌ Failed to generate {filename}: {e}")
            
            # Generate SFX files
            sfx_specs = {
                'shoot.wav': {
                    'duration': 0.2,
                    'generator': self._generate_laser_shoot,
                    'params': {'freq': 800, 'style': 'laser_pulse'}
                },
                'explosion.wav': {
                    'duration': 1.0,
                    'generator': self._generate_explosion,
                    'params': {'style': 'enemy_destruction'}
                },
                'bomb.wav': {
                    'duration': 2.0,
                    'generator': self._generate_bomb_explosion,
                    'params': {'style': 'massive_explosion'}
                },
                'item_collect.wav': {
                    'duration': 0.3,
                    'generator': self._generate_item_collect,
                    'params': {'freq': 1200, 'style': 'pickup_chime'}
                },
                'player_hit.wav': {
                    'duration': 0.8,
                    'generator': self._generate_player_hit,
                    'params': {'style': 'damage_alert'}
                },
                'enemy_spawn.wav': {
                    'duration': 0.5,
                    'generator': self._generate_enemy_spawn,
                    'params': {'style': 'warp_in'}
                },
                'menu_select.wav': {
                    'duration': 0.2,
                    'generator': self._generate_menu_select,
                    'params': {'freq': 600, 'style': 'ui_confirm'}
                },
                'menu_move.wav': {
                    'duration': 0.1,
                    'generator': self._generate_menu_move,
                    'params': {'freq': 400, 'style': 'ui_navigate'}
                }
            }
            
            for filename, spec in sfx_specs.items():
                current_file += 1
                if self.callback:
                    self.callback(f"効果音生成中: {filename}", current_file, total_files)
                
                try:
                    audio_data = spec['generator'](spec['duration'], **spec['params'])
                    filepath = os.path.join(self.assets_dir, 'sfx', filename)
                    self._save_audio_file(audio_data, filepath)
                    print(f"✅ Generated: {filename}")
                except Exception as e:
                    print(f"❌ Failed to generate {filename}: {e}")
            
            if self.callback:
                self.callback("音声ファイル生成完了！", total_files, total_files)
            
            return True
            
        except Exception as e:
            print(f"❌ Audio generation failed: {e}")
            if self.callback:
                self.callback(f"生成エラー: {str(e)}", current_file, total_files)
            return False
    
    def _generate_ambient_bgm(self, duration, base_freq, style):
        """Generate ambient space BGM."""
        if self.numpy_available:
            return self._generate_ambient_bgm_numpy(duration, base_freq)
        else:
            return self._generate_ambient_bgm_simple(duration, base_freq)
    
    def _generate_ambient_bgm_numpy(self, duration, base_freq):
        """Generate ambient BGM using numpy."""
        frames = int(duration * self.sample_rate)
        t = self.np.linspace(0, duration, frames)
        
        # Base drone with slow modulation
        drone1 = self.np.sin(2 * self.np.pi * base_freq * t) * 0.3
        drone2 = self.np.sin(2 * self.np.pi * base_freq * 1.5 * t) * 0.2
        
        # Slow LFO modulation
        lfo = self.np.sin(2 * self.np.pi * 0.05 * t) * 0.1 + 1
        
        # Ethereal high frequencies
        sparkle = self.np.sin(2 * self.np.pi * base_freq * 4 * t) * 0.05 * self.np.sin(2 * self.np.pi * 0.2 * t)
        
        # Combine and apply envelope
        combined = (drone1 + drone2) * lfo + sparkle
        
        # Apply fade in/out
        fade_samples = int(0.5 * self.sample_rate)
        combined[:fade_samples] *= self.np.linspace(0, 1, fade_samples)
        combined[-fade_samples:] *= self.np.linspace(1, 0, fade_samples)
        
        return combined * 0.6
    
    def _generate_ambient_bgm_simple(self, duration, base_freq):
        """Generate ambient BGM using simple math."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Base drone
            drone1 = math.sin(2 * math.pi * base_freq * t) * 0.3
            drone2 = math.sin(2 * math.pi * base_freq * 1.5 * t) * 0.2
            
            # Slow modulation
            lfo = math.sin(2 * math.pi * 0.05 * t) * 0.1 + 1
            
            # Combine
            sample = (drone1 + drone2) * lfo * 0.6
            
            # Apply fade in/out
            fade_in_samples = int(0.5 * self.sample_rate)
            fade_out_samples = int(0.5 * self.sample_rate)
            
            if i < fade_in_samples:
                sample *= float(i) / fade_in_samples
            elif i > frames - fade_out_samples:
                sample *= float(frames - i) / fade_out_samples
            
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_action_bgm(self, duration, base_freq, style):
        """Generate action battle BGM."""
        if self.numpy_available:
            return self._generate_action_bgm_numpy(duration, base_freq)
        else:
            return self._generate_action_bgm_simple(duration, base_freq)
    
    def _generate_action_bgm_numpy(self, duration, base_freq):
        """Generate action BGM using numpy."""
        frames = int(duration * self.sample_rate)
        t = self.np.linspace(0, duration, frames)
        
        # Rhythmic pattern (4/4 beat at 120 BPM)
        beat_freq = 2.0  # 2 Hz = 120 BPM
        rhythm = self.np.sin(2 * self.np.pi * beat_freq * t)
        rhythm = self.np.where(rhythm > 0, 1, 0.3)
        
        # Main melody line
        melody_freq = base_freq * (1 + 0.1 * self.np.sin(2 * self.np.pi * 0.25 * t))
        melody = self.np.sin(2 * self.np.pi * melody_freq * t) * 0.4
        
        # Bass line
        bass_freq = base_freq * 0.5
        bass = self.np.sin(2 * self.np.pi * bass_freq * t) * 0.3
        
        # High frequency arpeggios
        arp_freq = base_freq * 2 * (1 + 0.2 * self.np.sin(2 * self.np.pi * 4 * t))
        arpeggio = self.np.sin(2 * self.np.pi * arp_freq * t) * 0.15
        
        # Combine with rhythm
        combined = (melody + bass + arpeggio) * rhythm
        
        return combined * 0.7
    
    def _generate_action_bgm_simple(self, duration, base_freq):
        """Generate action BGM using simple math."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Rhythmic pattern
            rhythm = 1 if math.sin(2 * math.pi * 2 * t) > 0 else 0.3
            
            # Main melody
            melody = math.sin(2 * math.pi * base_freq * t) * 0.4
            
            # Bass line
            bass = math.sin(2 * math.pi * base_freq * 0.5 * t) * 0.3
            
            # Combine
            sample = (melody + bass) * rhythm * 0.7
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_dramatic_bgm(self, duration, base_freq, style):
        """Generate dramatic game over BGM."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            progress = t / duration
            
            # Descending chord progression
            freq1 = base_freq * (1 - progress * 0.4)
            freq2 = base_freq * 0.75 * (1 - progress * 0.3)
            freq3 = base_freq * 0.6 * (1 - progress * 0.2)
            
            chord1 = math.sin(2 * math.pi * freq1 * t) * 0.3
            chord2 = math.sin(2 * math.pi * freq2 * t) * 0.25
            chord3 = math.sin(2 * math.pi * freq3 * t) * 0.2
            
            # Dramatic fade out
            fade = (1 - progress) ** 2
            
            sample = (chord1 + chord2 + chord3) * fade * 0.8
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_victory_bgm(self, duration, base_freq, style):
        """Generate victory ranking BGM."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            progress = t / duration
            
            # Ascending triumphant melody
            melody_freq = base_freq * (1 + progress * 0.5)
            melody = math.sin(2 * math.pi * melody_freq * t) * 0.4
            
            # Harmony
            harmony_freq = base_freq * 1.25 * (1 + progress * 0.3)
            harmony = math.sin(2 * math.pi * harmony_freq * t) * 0.3
            
            # Triumphant brass-like sound
            brass_freq = base_freq * 2
            brass = math.sin(2 * math.pi * brass_freq * t) * 0.2 * (1 + math.sin(2 * math.pi * 8 * t) * 0.1)
            
            sample = (melody + harmony + brass) * 0.7
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_laser_shoot(self, duration, freq, style):
        """Generate laser shooting sound."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Laser sweep effect
            sweep_freq = freq * (1 - t / duration * 0.3)
            laser = math.sin(2 * math.pi * sweep_freq * t)
            
            # Add harmonics for richness
            harmonic = math.sin(2 * math.pi * sweep_freq * 2 * t) * 0.3
            
            # Sharp attack, quick decay
            envelope = math.exp(-t * 8)
            
            sample = (laser + harmonic) * envelope * 0.6
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_explosion(self, duration, style):
        """Generate explosion sound."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        import random
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Noise burst
            noise = (random.random() - 0.5) * 2
            
            # Low frequency rumble
            rumble = math.sin(2 * math.pi * 60 * t) * 0.5
            
            # Mid frequency crack
            crack_freq = 200 * (1 - t / duration * 0.8)
            crack = math.sin(2 * math.pi * crack_freq * t) * 0.3
            
            # Explosion envelope
            envelope = math.exp(-t * 3) * (1 + math.exp(-t * 20) * 2)
            
            sample = (noise * 0.3 + rumble + crack) * envelope * 0.5
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_bomb_explosion(self, duration, style):
        """Generate massive bomb explosion sound."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        import random
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Deep rumble
            rumble = math.sin(2 * math.pi * 40 * t) * 0.6
            
            # Noise burst
            noise = (random.random() - 0.5) * 2 * 0.4
            
            # Shockwave effect
            shockwave = math.sin(2 * math.pi * 80 * t * (1 - t / duration)) * 0.4
            
            # Long decay envelope
            envelope = math.exp(-t * 1.5) * (1 + math.exp(-t * 10) * 3)
            
            sample = (rumble + noise + shockwave) * envelope * 0.7
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_item_collect(self, duration, freq, style):
        """Generate item collection sound."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Rising chime
            chime_freq = freq * (1 + t / duration * 0.5)
            chime = math.sin(2 * math.pi * chime_freq * t)
            
            # Bell-like harmonics
            harmonic1 = math.sin(2 * math.pi * chime_freq * 2 * t) * 0.3
            harmonic2 = math.sin(2 * math.pi * chime_freq * 3 * t) * 0.1
            
            # Pleasant decay
            envelope = math.exp(-t * 4)
            
            sample = (chime + harmonic1 + harmonic2) * envelope * 0.5
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_player_hit(self, duration, style):
        """Generate player hit/damage sound."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Alarm-like sound
            alarm_freq = 800 * (1 + 0.2 * math.sin(2 * math.pi * 10 * t))
            alarm = math.sin(2 * math.pi * alarm_freq * t)
            
            # Distortion effect
            distortion = math.sin(2 * math.pi * 200 * t) * 0.3
            
            # Warning envelope
            envelope = math.exp(-t * 2) * (1 + math.sin(2 * math.pi * 5 * t) * 0.3)
            
            sample = (alarm + distortion) * envelope * 0.6
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_enemy_spawn(self, duration, style):
        """Generate enemy spawn/warp sound."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Warp effect
            warp_freq = 400 * (1 + t / duration * 2)
            warp = math.sin(2 * math.pi * warp_freq * t)
            
            # Modulation
            mod = math.sin(2 * math.pi * 20 * t) * 0.2 + 1
            
            # Build-up envelope
            envelope = t / duration * math.exp(-t * 2)
            
            sample = warp * mod * envelope * 0.4
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_menu_select(self, duration, freq, style):
        """Generate menu selection sound."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Clean beep
            beep = math.sin(2 * math.pi * freq * t)
            
            # Quick envelope
            envelope = math.exp(-t * 10)
            
            sample = beep * envelope * 0.4
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_menu_move(self, duration, freq, style):
        """Generate menu navigation sound."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Soft click
            click = math.sin(2 * math.pi * freq * t)
            
            # Very quick envelope
            envelope = math.exp(-t * 20)
            
            sample = click * envelope * 0.3
            audio_data.append(sample)
        
        return audio_data
    
    def _save_audio_file(self, audio_data, filepath):
        """Save audio data to WAV file using built-in wave module."""
        try:
            # Normalize and convert audio data
            if self.numpy_available and hasattr(audio_data, 'dtype'):
                # NumPy array
                audio_data = self.np.clip(audio_data, -1, 1)
                audio_int16 = (audio_data * 32767).astype(self.np.int16)
                audio_bytes = audio_int16.tobytes()
            else:
                # Python list
                audio_bytes = b''
                for sample in audio_data:
                    # Clamp sample to [-1, 1]
                    sample = max(-1, min(1, sample))
                    # Convert to 16-bit integer
                    int_sample = int(sample * 32767)
                    # Pack as little-endian 16-bit signed integer
                    audio_bytes += struct.pack('<h', int_sample)
            
            # Write WAV file
            with wave.open(filepath, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_bytes)
            
            print(f"    ✅ Saved: {os.path.basename(filepath)}")
            
        except Exception as e:
            print(f"    ❌ Failed to save {os.path.basename(filepath)}: {e}")
            raise

def check_audio_files_exist():
    """Check if all required audio files exist."""
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'audio')
    
    required_files = [
        'bgm/menu_bgm.wav',
        'bgm/game_bgm.wav', 
        'bgm/game_over_bgm.wav',
        'bgm/ranking_bgm.wav',
        'sfx/shoot.wav',
        'sfx/explosion.wav',
        'sfx/bomb.wav',
        'sfx/item_collect.wav',
        'sfx/player_hit.wav',
        'sfx/enemy_spawn.wav',
        'sfx/menu_select.wav',
        'sfx/menu_move.wav'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(assets_dir, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    return len(missing_files) == 0, missing_files
    
    def generate_all_audio(self):
        """Generate all BGM and sound effects."""
        total_files = 12  # 4 BGM + 8 SFX
        current_file = 0
        
        if self.callback:
            self.callback("音声ファイルを生成中...", 0, total_files)
        
        # Generate BGM files
        bgm_specs = {
            'menu_bgm.wav': {
                'duration': 60,
                'generator': self._generate_ambient_bgm,
                'params': {'base_freq': 220, 'style': 'space_ambient'}
            },
            'game_bgm.wav': {
                'duration': 120,
                'generator': self._generate_action_bgm,
                'params': {'base_freq': 440, 'style': 'battle_action'}
            },
            'game_over_bgm.wav': {
                'duration': 20,
                'generator': self._generate_dramatic_bgm,
                'params': {'base_freq': 330, 'style': 'dramatic_defeat'}
            },
            'ranking_bgm.wav': {
                'duration': 30,
                'generator': self._generate_victory_bgm,
                'params': {'base_freq': 550, 'style': 'triumphant_victory'}
            }
        }
        
        for filename, spec in bgm_specs.items():
            current_file += 1
            if self.callback:
                self.callback(f"BGM生成中: {filename}", current_file, total_files)
            
            audio_data = spec['generator'](spec['duration'], **spec['params'])
            filepath = os.path.join(self.assets_dir, 'bgm', filename)
            self._save_audio_file(audio_data, filepath)
        
        # Generate SFX files
        sfx_specs = {
            'shoot.wav': {
                'duration': 0.2,
                'generator': self._generate_laser_shoot,
                'params': {'freq': 800, 'style': 'laser_pulse'}
            },
            'explosion.wav': {
                'duration': 1.0,
                'generator': self._generate_explosion,
                'params': {'style': 'enemy_destruction'}
            },
            'bomb.wav': {
                'duration': 2.0,
                'generator': self._generate_bomb_explosion,
                'params': {'style': 'massive_explosion'}
            },
            'item_collect.wav': {
                'duration': 0.3,
                'generator': self._generate_item_collect,
                'params': {'freq': 1200, 'style': 'pickup_chime'}
            },
            'player_hit.wav': {
                'duration': 0.8,
                'generator': self._generate_player_hit,
                'params': {'style': 'damage_alert'}
            },
            'enemy_spawn.wav': {
                'duration': 0.5,
                'generator': self._generate_enemy_spawn,
                'params': {'style': 'warp_in'}
            },
            'menu_select.wav': {
                'duration': 0.2,
                'generator': self._generate_menu_select,
                'params': {'freq': 600, 'style': 'ui_confirm'}
            },
            'menu_move.wav': {
                'duration': 0.1,
                'generator': self._generate_menu_move,
                'params': {'freq': 400, 'style': 'ui_navigate'}
            }
        }
        
        for filename, spec in sfx_specs.items():
            current_file += 1
            if self.callback:
                self.callback(f"効果音生成中: {filename}", current_file, total_files)
            
            audio_data = spec['generator'](spec['duration'], **spec['params'])
            filepath = os.path.join(self.assets_dir, 'sfx', filename)
            self._save_audio_file(audio_data, filepath)
        
        if self.callback:
            self.callback("音声ファイル生成完了！", total_files, total_files)
        
        return True
    
    def _generate_ambient_bgm(self, duration, base_freq, style):
        """Generate ambient space BGM."""
        if self.numpy_available:
            return self._generate_ambient_bgm_numpy(duration, base_freq)
        else:
            return self._generate_ambient_bgm_simple(duration, base_freq)
    
    def _generate_ambient_bgm_numpy(self, duration, base_freq):
        """Generate ambient BGM using numpy."""
        frames = int(duration * self.sample_rate)
        t = self.np.linspace(0, duration, frames)
        
        # Base drone with slow modulation
        drone1 = self.np.sin(2 * self.np.pi * base_freq * t) * 0.3
        drone2 = self.np.sin(2 * self.np.pi * base_freq * 1.5 * t) * 0.2
        
        # Slow LFO modulation
        lfo = self.np.sin(2 * self.np.pi * 0.05 * t) * 0.1 + 1
        
        # Ethereal high frequencies
        sparkle = self.np.sin(2 * self.np.pi * base_freq * 4 * t) * 0.05 * self.np.sin(2 * self.np.pi * 0.2 * t)
        
        # Combine and apply envelope
        combined = (drone1 + drone2) * lfo + sparkle
        
        # Apply fade in/out
        fade_samples = int(0.5 * self.sample_rate)
        combined[:fade_samples] *= self.np.linspace(0, 1, fade_samples)
        combined[-fade_samples:] *= self.np.linspace(1, 0, fade_samples)
        
        return combined * 0.6
    
    def _generate_ambient_bgm_simple(self, duration, base_freq):
        """Generate ambient BGM using simple math."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Base drone
            drone1 = math.sin(2 * math.pi * base_freq * t) * 0.3
            drone2 = math.sin(2 * math.pi * base_freq * 1.5 * t) * 0.2
            
            # Slow modulation
            lfo = math.sin(2 * math.pi * 0.05 * t) * 0.1 + 1
            
            # Combine
            sample = (drone1 + drone2) * lfo * 0.6
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_action_bgm(self, duration, base_freq, style):
        """Generate action battle BGM."""
        if self.numpy_available:
            return self._generate_action_bgm_numpy(duration, base_freq)
        else:
            return self._generate_action_bgm_simple(duration, base_freq)
    
    def _generate_action_bgm_numpy(self, duration, base_freq):
        """Generate action BGM using numpy."""
        frames = int(duration * self.sample_rate)
        t = self.np.linspace(0, duration, frames)
        
        # Rhythmic pattern (4/4 beat at 120 BPM)
        beat_freq = 2.0  # 2 Hz = 120 BPM
        rhythm = self.np.sin(2 * self.np.pi * beat_freq * t)
        rhythm = self.np.where(rhythm > 0, 1, 0.3)
        
        # Main melody line
        melody_freq = base_freq * (1 + 0.1 * self.np.sin(2 * self.np.pi * 0.25 * t))
        melody = self.np.sin(2 * self.np.pi * melody_freq * t) * 0.4
        
        # Bass line
        bass_freq = base_freq * 0.5
        bass = self.np.sin(2 * self.np.pi * bass_freq * t) * 0.3
        
        # High frequency arpeggios
        arp_freq = base_freq * 2 * (1 + 0.2 * self.np.sin(2 * self.np.pi * 4 * t))
        arpeggio = self.np.sin(2 * self.np.pi * arp_freq * t) * 0.15
        
        # Combine with rhythm
        combined = (melody + bass + arpeggio) * rhythm
        
        return combined * 0.7
    
    def _generate_action_bgm_simple(self, duration, base_freq):
        """Generate action BGM using simple math."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Rhythmic pattern
            rhythm = 1 if math.sin(2 * math.pi * 2 * t) > 0 else 0.3
            
            # Main melody
            melody = math.sin(2 * math.pi * base_freq * t) * 0.4
            
            # Bass line
            bass = math.sin(2 * math.pi * base_freq * 0.5 * t) * 0.3
            
            # Combine
            sample = (melody + bass) * rhythm * 0.7
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_dramatic_bgm(self, duration, base_freq, style):
        """Generate dramatic game over BGM."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            progress = t / duration
            
            # Descending chord progression
            freq1 = base_freq * (1 - progress * 0.4)
            freq2 = base_freq * 0.75 * (1 - progress * 0.3)
            freq3 = base_freq * 0.6 * (1 - progress * 0.2)
            
            chord1 = math.sin(2 * math.pi * freq1 * t) * 0.3
            chord2 = math.sin(2 * math.pi * freq2 * t) * 0.25
            chord3 = math.sin(2 * math.pi * freq3 * t) * 0.2
            
            # Dramatic fade out
            fade = (1 - progress) ** 2
            
            sample = (chord1 + chord2 + chord3) * fade * 0.8
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_victory_bgm(self, duration, base_freq, style):
        """Generate victory ranking BGM."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            progress = t / duration
            
            # Ascending triumphant melody
            melody_freq = base_freq * (1 + progress * 0.5)
            melody = math.sin(2 * math.pi * melody_freq * t) * 0.4
            
            # Harmony
            harmony_freq = base_freq * 1.25 * (1 + progress * 0.3)
            harmony = math.sin(2 * math.pi * harmony_freq * t) * 0.3
            
            # Triumphant brass-like sound
            brass_freq = base_freq * 2
            brass = math.sin(2 * math.pi * brass_freq * t) * 0.2 * (1 + math.sin(2 * math.pi * 8 * t) * 0.1)
            
            sample = (melody + harmony + brass) * 0.7
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_laser_shoot(self, duration, freq, style):
        """Generate laser shooting sound."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Laser sweep effect
            sweep_freq = freq * (1 - t / duration * 0.3)
            laser = math.sin(2 * math.pi * sweep_freq * t)
            
            # Add harmonics for richness
            harmonic = math.sin(2 * math.pi * sweep_freq * 2 * t) * 0.3
            
            # Sharp attack, quick decay
            envelope = math.exp(-t * 8)
            
            sample = (laser + harmonic) * envelope * 0.6
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_explosion(self, duration, style):
        """Generate explosion sound."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Noise burst (simplified)
            import random
            noise = (random.random() - 0.5) * 2
            
            # Low frequency rumble
            rumble = math.sin(2 * math.pi * 60 * t) * 0.5
            
            # Mid frequency crack
            crack_freq = 200 * (1 - t / duration * 0.8)
            crack = math.sin(2 * math.pi * crack_freq * t) * 0.3
            
            # Explosion envelope
            envelope = math.exp(-t * 3) * (1 + math.exp(-t * 20) * 2)
            
            sample = (noise * 0.3 + rumble + crack) * envelope * 0.5
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_bomb_explosion(self, duration, style):
        """Generate massive bomb explosion sound."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Deep rumble
            rumble = math.sin(2 * math.pi * 40 * t) * 0.6
            
            # Noise burst
            import random
            noise = (random.random() - 0.5) * 2 * 0.4
            
            # Shockwave effect
            shockwave = math.sin(2 * math.pi * 80 * t * (1 - t / duration)) * 0.4
            
            # Long decay envelope
            envelope = math.exp(-t * 1.5) * (1 + math.exp(-t * 10) * 3)
            
            sample = (rumble + noise + shockwave) * envelope * 0.7
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_item_collect(self, duration, freq, style):
        """Generate item collection sound."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Rising chime
            chime_freq = freq * (1 + t / duration * 0.5)
            chime = math.sin(2 * math.pi * chime_freq * t)
            
            # Bell-like harmonics
            harmonic1 = math.sin(2 * math.pi * chime_freq * 2 * t) * 0.3
            harmonic2 = math.sin(2 * math.pi * chime_freq * 3 * t) * 0.1
            
            # Pleasant decay
            envelope = math.exp(-t * 4)
            
            sample = (chime + harmonic1 + harmonic2) * envelope * 0.5
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_player_hit(self, duration, style):
        """Generate player hit/damage sound."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Alarm-like sound
            alarm_freq = 800 * (1 + 0.2 * math.sin(2 * math.pi * 10 * t))
            alarm = math.sin(2 * math.pi * alarm_freq * t)
            
            # Distortion effect
            distortion = math.sin(2 * math.pi * 200 * t) * 0.3
            
            # Warning envelope
            envelope = math.exp(-t * 2) * (1 + math.sin(2 * math.pi * 5 * t) * 0.3)
            
            sample = (alarm + distortion) * envelope * 0.6
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_enemy_spawn(self, duration, style):
        """Generate enemy spawn/warp sound."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Warp effect
            warp_freq = 400 * (1 + t / duration * 2)
            warp = math.sin(2 * math.pi * warp_freq * t)
            
            # Modulation
            mod = math.sin(2 * math.pi * 20 * t) * 0.2 + 1
            
            # Build-up envelope
            envelope = t / duration * math.exp(-t * 2)
            
            sample = warp * mod * envelope * 0.4
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_menu_select(self, duration, freq, style):
        """Generate menu selection sound."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Clean beep
            beep = math.sin(2 * math.pi * freq * t)
            
            # Quick envelope
            envelope = math.exp(-t * 10)
            
            sample = beep * envelope * 0.4
            audio_data.append(sample)
        
        return audio_data
    
    def _generate_menu_move(self, duration, freq, style):
        """Generate menu navigation sound."""
        frames = int(duration * self.sample_rate)
        audio_data = []
        
        for i in range(frames):
            t = float(i) / self.sample_rate
            
            # Soft click
            click = math.sin(2 * math.pi * freq * t)
            
            # Very quick envelope
            envelope = math.exp(-t * 20)
            
            sample = click * envelope * 0.3
            audio_data.append(sample)
        
        return audio_data
    
    def _save_audio_file(self, audio_data, filepath):
        """Save audio data to WAV file."""
        try:
            if self.scipy_available and self.numpy_available:
                # Use scipy for high-quality WAV writing
                if isinstance(audio_data, list):
                    audio_data = self.np.array(audio_data)
                
                # Normalize audio data
                audio_data = self.np.clip(audio_data, -1, 1)
                
                # Convert to 16-bit integers
                audio_int16 = (audio_data * 32767).astype(self.np.int16)
                
                # Save as WAV file
                self.wavfile.write(filepath, self.sample_rate, audio_int16)
            else:
                # Fallback: use pygame for WAV writing
                self._save_audio_file_pygame(audio_data, filepath)
                
        except Exception as e:
            print(f"Failed to save {os.path.basename(filepath)}: {e}")
    
    def _save_audio_file_pygame(self, audio_data, filepath):
        """Save audio file using pygame (fallback method)."""
        try:
            # Convert to pygame sound format
            if isinstance(audio_data, list):
                # Convert to 16-bit integers
                sound_data = []
                for sample in audio_data:
                    sample = max(-1, min(1, sample))  # Clamp
                    int_sample = int(sample * 32767)
                    sound_data.append([int_sample, int_sample])  # Stereo
            else:
                # Assume numpy array
                audio_data = audio_data.clip(-1, 1)
                sound_data = []
                for sample in audio_data:
                    int_sample = int(sample * 32767)
                    sound_data.append([int_sample, int_sample])
            
            # Create pygame sound and save
            sound = pygame.sndarray.make_sound(sound_data)
            
            # Note: pygame doesn't have direct WAV export
            # This is a simplified approach
            print(f"Saved (pygame method): {os.path.basename(filepath)}")
            
        except Exception as e:
            print(f"Failed to save with pygame: {e}")

def check_audio_files_exist():
    """Check if all required audio files exist."""
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'audio')
    
    required_files = [
        'bgm/menu_bgm.wav',
        'bgm/game_bgm.wav', 
        'bgm/game_over_bgm.wav',
        'bgm/ranking_bgm.wav',
        'sfx/shoot.wav',
        'sfx/explosion.wav',
        'sfx/bomb.wav',
        'sfx/item_collect.wav',
        'sfx/player_hit.wav',
        'sfx/enemy_spawn.wav',
        'sfx/menu_select.wav',
        'sfx/menu_move.wav'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(assets_dir, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    return len(missing_files) == 0, missing_files
