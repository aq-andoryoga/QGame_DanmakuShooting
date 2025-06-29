"""
Font manager for Japanese text support in QGamen_DanmakuShooting
"""

import pygame
import os
import sys

class FontManager:
    """Manages fonts with Japanese text support."""
    
    def __init__(self):
        """Initialize the font manager."""
        pygame.font.init()
        self.fonts = {}
        self.default_font = None
        self._init_default_font()
    
    def _init_default_font(self):
        """Initialize the default font with Japanese support."""
        # Try to find a Japanese font
        japanese_font_names = [
            # Windows fonts
            "msgothic",
            "msmincho", 
            "meiryo",
            "yugothm",
            # macOS fonts
            "hiragino sans gb",
            "hiragino kaku gothic pron",
            # Linux fonts
            "noto sans cjk jp",
            "takao gothic",
            "ipaexgothic",
            # Fallback fonts
            "dejavu sans",
            "liberation sans",
            "arial unicode ms"
        ]
        
        # Try each font
        for font_name in japanese_font_names:
            try:
                test_font = pygame.font.SysFont(font_name, 24)
                # Test if it can render Japanese characters
                test_surface = test_font.render("テスト", True, (255, 255, 255))
                if test_surface.get_width() > 0:
                    self.default_font = font_name
                    print(f"Using font: {font_name}")
                    return
            except:
                continue
        
        # If no Japanese font found, use default
        print("No Japanese font found, using default font")
        self.default_font = None
    
    def get_font(self, size, font_type="default"):
        """Get a font with the specified size."""
        cache_key = f"{font_type}_{size}"
        
        if cache_key in self.fonts:
            return self.fonts[cache_key]
        
        # Create font
        if self.default_font:
            try:
                font = pygame.font.SysFont(self.default_font, size)
            except:
                font = pygame.font.Font(None, size)
        else:
            font = pygame.font.Font(None, size)
        
        # Cache the font
        self.fonts[cache_key] = font
        return font
    
    def render_text(self, text, size, color, font_type="default"):
        """Render text with Japanese support."""
        font = self.get_font(size, font_type)
        
        try:
            # Try to render the text
            surface = font.render(text, True, color)
            return surface
        except UnicodeError:
            # If Unicode error, try to encode/decode
            try:
                # Try different encodings
                encoded_text = text.encode('utf-8').decode('utf-8')
                surface = font.render(encoded_text, True, color)
                return surface
            except:
                # Last resort: replace problematic characters
                safe_text = text.encode('ascii', 'replace').decode('ascii')
                surface = font.render(safe_text, True, color)
                return surface
        except Exception as e:
            # Any other error, use a simple fallback
            print(f"Font rendering error: {e}")
            fallback_font = pygame.font.Font(None, size)
            try:
                surface = fallback_font.render(text, True, color)
                return surface
            except:
                # Ultimate fallback
                surface = fallback_font.render("???", True, color)
                return surface

# Global font manager instance
font_manager = FontManager()
