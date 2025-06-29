#!/usr/bin/env python3
"""
QGamen_DanmakuShooting - Main Entry Point
A bullet hell shooting game developed with Pygame.
"""

import sys
import os
import pygame

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game import Game

def main():
    """Main function to start the game."""
    try:
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()  # Initialize sound mixer
        
        # Create and run the game
        game = Game()
        game.run()
        
    except Exception as e:
        print(f"Error starting game: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()
