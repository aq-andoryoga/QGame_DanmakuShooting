"""
Ranking system for QGamen_DanmakuShooting
"""

import pygame
import json
import os

class RankingManager:
    """Manages high scores and rankings."""
    
    def __init__(self, filename="rankings.json"):
        """Initialize the ranking manager."""
        self.filename = filename
        self.rankings = []
        self.max_rankings = 10
        self.current_name = ""
        self.name_input_complete = False
        self.load_rankings()
    
    def load_rankings(self):
        """Load rankings from file."""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.rankings = data.get('rankings', [])
            else:
                # Create default rankings
                self.rankings = [
                    ("PLAYER", 1000),
                    ("PLAYER", 900),
                    ("PLAYER", 800),
                    ("PLAYER", 700),
                    ("PLAYER", 600),
                    ("PLAYER", 500),
                    ("PLAYER", 400),
                    ("PLAYER", 300),
                    ("PLAYER", 200),
                    ("PLAYER", 100)
                ]
                self.save_rankings()
        except Exception as e:
            print(f"Error loading rankings: {e}")
            # Create default rankings on error
            self.rankings = [("PLAYER", 100 * (10 - i)) for i in range(10)]
    
    def save_rankings(self):
        """Save rankings to file."""
        try:
            data = {'rankings': self.rankings}
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving rankings: {e}")
    
    def is_high_score(self, score):
        """Check if score qualifies for high score list."""
        if len(self.rankings) < self.max_rankings:
            return True
        return score > self.rankings[-1][1]
    
    def add_score(self, name, score):
        """Add a new score to rankings."""
        self.rankings.append((name, score))
        self.rankings.sort(key=lambda x: x[1], reverse=True)
        self.rankings = self.rankings[:self.max_rankings]
        self.save_rankings()
    
    def get_rankings(self):
        """Get current rankings."""
        return self.rankings
    
    def handle_name_input(self, event, score):
        """Handle name input for high score."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Finish name input
                if not self.current_name:
                    self.current_name = "ANONYMOUS"
                self.add_score(self.current_name, score)
                self.current_name = ""
                self.name_input_complete = True
            elif event.key == pygame.K_BACKSPACE:
                # Remove last character
                self.current_name = self.current_name[:-1]
            else:
                # Add character (limit to 10 characters)
                if len(self.current_name) < 10:
                    char = event.unicode
                    if char.isprintable() and char != ' ':
                        self.current_name += char.upper()
    
    def reset_name_input(self):
        """Reset name input state."""
        self.current_name = ""
        self.name_input_complete = False
