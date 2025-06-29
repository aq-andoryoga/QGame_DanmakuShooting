#!/usr/bin/env python3
"""
Audio file generator for QGamen_DanmakuShooting
Generates BGM and sound effects as MP3/WAV files
"""

import os
import sys
import numpy as np
import pygame
from scipy.io import wavfile
import math

class AudioFileGenerator:
    """Generates audio files for the game."""
    
    def __init__(self):
        """Initialize the audio file generator."""
        self.sample_rate = 44100  # Higher quality for file output
        self.assets_dir = os.path.join(os.path.dirname(__file__), 'assets', 'audio')
        
        # Create assets directory structure
        os.makedirs(os.path.join(self.assets_dir, 'bgm'), exist_ok=True)
        os.makedirs(os.path.join(self.assets_dir, 'sfx'), exist_ok=True)
        
        print(f"📁 Audio files will be saved to: {self.assets_dir}")
    
    def generate_all_audio(self):
        """Generate all BGM and sound effects."""
        print("🎵 Generating BGM files...")
        self.generate_bgm_files()
        
        print("🔊 Generating sound effect files...")
        self.generate_sfx_files()
        
        print("✅ All audio files generated successfully!")
    
    def generate_bgm_files(self):
        """Generate all BGM files."""
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
            print(f"  🎼 Generating {filename}...")
            audio_data = spec['generator'](spec['duration'], **spec['params'])
            filepath = os.path.join(self.assets_dir, 'bgm', filename)
            self._save_audio_file(audio_data, filepath)
    
    def generate_sfx_files(self):
        """Generate all sound effect files."""
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
            print(f"  🔊 Generating {filename}...")
            audio_data = spec['generator'](spec['duration'], **spec['params'])
            filepath = os.path.join(self.assets_dir, 'sfx', filename)
            self._save_audio_file(audio_data, filepath)
    
    def _generate_ambient_bgm(self, duration, base_freq, style):
        """Generate ambient space BGM."""
        frames = int(duration * self.sample_rate)
        t = np.linspace(0, duration, frames)
        
        # Base drone with slow modulation
        drone1 = np.sin(2 * np.pi * base_freq * t) * 0.3
        drone2 = np.sin(2 * np.pi * base_freq * 1.5 * t) * 0.2
        
        # Slow LFO modulation
        lfo = np.sin(2 * np.pi * 0.05 * t) * 0.1 + 1
        
        # Ethereal high frequencies
        sparkle = np.sin(2 * np.pi * base_freq * 4 * t) * 0.05 * np.sin(2 * np.pi * 0.2 * t)
        
        # Combine and apply envelope
        combined = (drone1 + drone2) * lfo + sparkle
        
        # Apply fade in/out
        fade_samples = int(0.5 * self.sample_rate)
        combined[:fade_samples] *= np.linspace(0, 1, fade_samples)
        combined[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        return combined * 0.6
    
    def _generate_action_bgm(self, duration, base_freq, style):
        """Generate action battle BGM."""
        frames = int(duration * self.sample_rate)
        t = np.linspace(0, duration, frames)
        
        # Rhythmic pattern (4/4 beat at 120 BPM)
        beat_freq = 2.0  # 2 Hz = 120 BPM
        rhythm = np.sin(2 * np.pi * beat_freq * t)
        rhythm = np.where(rhythm > 0, 1, 0.3)
        
        # Main melody line
        melody_freq = base_freq * (1 + 0.1 * np.sin(2 * np.pi * 0.25 * t))
        melody = np.sin(2 * np.pi * melody_freq * t) * 0.4
        
        # Bass line
        bass_freq = base_freq * 0.5
        bass = np.sin(2 * np.pi * bass_freq * t) * 0.3
        
        # High frequency arpeggios
        arp_freq = base_freq * 2 * (1 + 0.2 * np.sin(2 * np.pi * 4 * t))
        arpeggio = np.sin(2 * np.pi * arp_freq * t) * 0.15
        
        # Combine with rhythm
        combined = (melody + bass + arpeggio) * rhythm
        
        return combined * 0.7
    
    def _generate_dramatic_bgm(self, duration, base_freq, style):
        """Generate dramatic game over BGM."""
        frames = int(duration * self.sample_rate)
        t = np.linspace(0, duration, frames)
        
        # Descending chord progression
        freq1 = base_freq * (1 - t / duration * 0.4)
        freq2 = base_freq * 0.75 * (1 - t / duration * 0.3)
        freq3 = base_freq * 0.6 * (1 - t / duration * 0.2)
        
        chord1 = np.sin(2 * np.pi * freq1 * t) * 0.3
        chord2 = np.sin(2 * np.pi * freq2 * t) * 0.25
        chord3 = np.sin(2 * np.pi * freq3 * t) * 0.2
        
        # Dramatic fade out
        fade = (1 - t / duration) ** 2
        
        combined = (chord1 + chord2 + chord3) * fade
        
        return combined * 0.8
    
    def _generate_victory_bgm(self, duration, base_freq, style):
        """Generate victory ranking BGM."""
        frames = int(duration * self.sample_rate)
        t = np.linspace(0, duration, frames)
        
        # Ascending triumphant melody
        melody_freq = base_freq * (1 + t / duration * 0.5)
        melody = np.sin(2 * np.pi * melody_freq * t) * 0.4
        
        # Harmony
        harmony_freq = base_freq * 1.25 * (1 + t / duration * 0.3)
        harmony = np.sin(2 * np.pi * harmony_freq * t) * 0.3
        
        # Triumphant brass-like sound
        brass_freq = base_freq * 2
        brass = np.sin(2 * np.pi * brass_freq * t) * 0.2 * (1 + np.sin(2 * np.pi * 8 * t) * 0.1)
        
        combined = melody + harmony + brass
        
        return combined * 0.7
    
    def _generate_laser_shoot(self, duration, freq, style):
        """Generate laser shooting sound."""
        frames = int(duration * self.sample_rate)
        t = np.linspace(0, duration, frames)
        
        # Laser sweep effect
        sweep_freq = freq * (1 - t / duration * 0.3)
        laser = np.sin(2 * np.pi * sweep_freq * t)
        
        # Add harmonics for richness
        harmonic = np.sin(2 * np.pi * sweep_freq * 2 * t) * 0.3
        
        # Sharp attack, quick decay
        envelope = np.exp(-t * 8)
        
        combined = (laser + harmonic) * envelope
        
        return combined * 0.6
    
    def _generate_explosion(self, duration, style):
        """Generate explosion sound."""
        frames = int(duration * self.sample_rate)
        t = np.linspace(0, duration, frames)
        
        # Noise burst
        noise = np.random.normal(0, 1, frames)
        
        # Low frequency rumble
        rumble = np.sin(2 * np.pi * 60 * t) * 0.5
        
        # Mid frequency crack
        crack_freq = 200 * (1 - t / duration * 0.8)
        crack = np.sin(2 * np.pi * crack_freq * t) * 0.3
        
        # Explosion envelope
        envelope = np.exp(-t * 3) * (1 + np.exp(-t * 20) * 2)
        
        combined = (noise * 0.3 + rumble + crack) * envelope
        
        return combined * 0.5
    
    def _generate_bomb_explosion(self, duration, style):
        """Generate massive bomb explosion sound."""
        frames = int(duration * self.sample_rate)
        t = np.linspace(0, duration, frames)
        
        # Deep rumble
        rumble = np.sin(2 * np.pi * 40 * t) * 0.6
        
        # Noise burst
        noise = np.random.normal(0, 1, frames) * 0.4
        
        # Shockwave effect
        shockwave = np.sin(2 * np.pi * 80 * t * (1 - t / duration)) * 0.4
        
        # Long decay envelope
        envelope = np.exp(-t * 1.5) * (1 + np.exp(-t * 10) * 3)
        
        combined = (rumble + noise + shockwave) * envelope
        
        return combined * 0.7
    
    def _generate_item_collect(self, duration, freq, style):
        """Generate item collection sound."""
        frames = int(duration * self.sample_rate)
        t = np.linspace(0, duration, frames)
        
        # Rising chime
        chime_freq = freq * (1 + t / duration * 0.5)
        chime = np.sin(2 * np.pi * chime_freq * t)
        
        # Bell-like harmonics
        harmonic1 = np.sin(2 * np.pi * chime_freq * 2 * t) * 0.3
        harmonic2 = np.sin(2 * np.pi * chime_freq * 3 * t) * 0.1
        
        # Pleasant decay
        envelope = np.exp(-t * 4)
        
        combined = (chime + harmonic1 + harmonic2) * envelope
        
        return combined * 0.5
    
    def _generate_player_hit(self, duration, style):
        """Generate player hit/damage sound."""
        frames = int(duration * self.sample_rate)
        t = np.linspace(0, duration, frames)
        
        # Alarm-like sound
        alarm_freq = 800 * (1 + 0.2 * np.sin(2 * np.pi * 10 * t))
        alarm = np.sin(2 * np.pi * alarm_freq * t)
        
        # Distortion effect
        distortion = np.sin(2 * np.pi * 200 * t) * 0.3
        
        # Warning envelope
        envelope = np.exp(-t * 2) * (1 + np.sin(2 * np.pi * 5 * t) * 0.3)
        
        combined = (alarm + distortion) * envelope
        
        return combined * 0.6
    
    def _generate_enemy_spawn(self, duration, style):
        """Generate enemy spawn/warp sound."""
        frames = int(duration * self.sample_rate)
        t = np.linspace(0, duration, frames)
        
        # Warp effect
        warp_freq = 400 * (1 + t / duration * 2)
        warp = np.sin(2 * np.pi * warp_freq * t)
        
        # Modulation
        mod = np.sin(2 * np.pi * 20 * t) * 0.2 + 1
        
        # Build-up envelope
        envelope = t / duration * np.exp(-t * 2)
        
        combined = warp * mod * envelope
        
        return combined * 0.4
    
    def _generate_menu_select(self, duration, freq, style):
        """Generate menu selection sound."""
        frames = int(duration * self.sample_rate)
        t = np.linspace(0, duration, frames)
        
        # Clean beep
        beep = np.sin(2 * np.pi * freq * t)
        
        # Quick envelope
        envelope = np.exp(-t * 10)
        
        combined = beep * envelope
        
        return combined * 0.4
    
    def _generate_menu_move(self, duration, freq, style):
        """Generate menu navigation sound."""
        frames = int(duration * self.sample_rate)
        t = np.linspace(0, duration, frames)
        
        # Soft click
        click = np.sin(2 * np.pi * freq * t)
        
        # Very quick envelope
        envelope = np.exp(-t * 20)
        
        combined = click * envelope
        
        return combined * 0.3
    
    def _save_audio_file(self, audio_data, filepath):
        """Save audio data to WAV file."""
        try:
            # Normalize audio data
            audio_data = np.clip(audio_data, -1, 1)
            
            # Convert to 16-bit integers
            audio_int16 = (audio_data * 32767).astype(np.int16)
            
            # Save as WAV file
            wavfile.write(filepath, self.sample_rate, audio_int16)
            
            print(f"    ✅ Saved: {os.path.basename(filepath)}")
            
        except Exception as e:
            print(f"    ❌ Failed to save {os.path.basename(filepath)}: {e}")

def main():
    """Generate all audio files."""
    print("🎵 QGamen Audio File Generator")
    print("=" * 50)
    
    try:
        generator = AudioFileGenerator()
        generator.generate_all_audio()
        
        print("\n" + "=" * 50)
        print("🎉 Audio file generation completed!")
        print(f"📁 Files saved to: {generator.assets_dir}")
        print("\nGenerated files:")
        print("BGM:")
        print("  - menu_bgm.wav (60s ambient space theme)")
        print("  - game_bgm.wav (120s action battle theme)")
        print("  - game_over_bgm.wav (20s dramatic theme)")
        print("  - ranking_bgm.wav (30s victory theme)")
        print("SFX:")
        print("  - shoot.wav (laser shooting)")
        print("  - explosion.wav (enemy destruction)")
        print("  - bomb.wav (massive explosion)")
        print("  - item_collect.wav (pickup chime)")
        print("  - player_hit.wav (damage alert)")
        print("  - enemy_spawn.wav (warp in)")
        print("  - menu_select.wav (UI confirm)")
        print("  - menu_move.wav (UI navigate)")
        
    except ImportError as e:
        print(f"❌ Missing required packages: {e}")
        print("Please install: pip install numpy scipy")
    except Exception as e:
        print(f"❌ Error generating audio files: {e}")

if __name__ == "__main__":
    main()
