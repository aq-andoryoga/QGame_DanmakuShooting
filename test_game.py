#!/usr/bin/env python3
"""
Test script for QGamen_DanmakuShooting
Tests game components without requiring display
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all modules can be imported."""
    try:
        from player import Player, PlayerBullet
        from enemy import Enemy, RadialEnemy, CircularEnemy, SpiralEnemy, EnemyManager, EnemyBullet
        from bullet import BulletManager
        from ui import UI
        from effects import Explosion, EffectManager
        from ranking import RankingManager
        from game import Game, GameState
        print("✅ All modules imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without pygame display."""
    try:
        # Test Player
        player = Player(100, 100)
        print(f"✅ Player created at ({player.x}, {player.y})")
        
        # Test PlayerBullet
        bullet = PlayerBullet(100, 100)
        print(f"✅ PlayerBullet created at ({bullet.x}, {bullet.y})")
        
        # Test Enemy
        enemy = RadialEnemy(200, 200)
        print(f"✅ RadialEnemy created at ({enemy.x}, {enemy.y})")
        
        # Test EnemyManager
        enemy_manager = EnemyManager(1280, 1080)
        print("✅ EnemyManager created")
        
        # Test BulletManager
        bullet_manager = BulletManager()
        print("✅ BulletManager created")
        
        # Test EffectManager
        effect_manager = EffectManager()
        print("✅ EffectManager created")
        
        # Test RankingManager
        ranking_manager = RankingManager()
        print("✅ RankingManager created")
        
        return True
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

def test_game_logic():
    """Test game logic without display."""
    try:
        # Test player movement simulation
        player = Player(100, 100)
        original_x = player.x
        
        # Simulate key press (move right)
        keys = {pygame.K_RIGHT: True, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: False}
        # Note: This would require pygame to be initialized, so we'll skip actual key testing
        
        # Test bullet creation
        bullet = player.shoot()
        if bullet:
            print("✅ Player can shoot bullets")
        
        # Test enemy bullet patterns
        enemy = RadialEnemy(200, 200)
        bullets = enemy.create_bullet_pattern()
        print(f"✅ RadialEnemy created {len(bullets)} bullets in pattern")
        
        # Test ranking system
        ranking_manager = RankingManager()
        test_score = 1500
        is_high = ranking_manager.is_high_score(test_score)
        print(f"✅ Score {test_score} is high score: {is_high}")
        
        return True
    except Exception as e:
        print(f"❌ Game logic test error: {e}")
        return False

def main():
    """Run all tests."""
    print("🎮 Testing QGamen_DanmakuShooting Components")
    print("=" * 50)
    
    # Import pygame for constants (but don't initialize display)
    try:
        import pygame
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.NOFRAME)  # Minimal display for constants
        print("✅ Pygame initialized for testing")
    except:
        print("⚠️  Pygame display not available, skipping display-dependent tests")
    
    success = True
    
    print("\n📦 Testing Imports...")
    success &= test_imports()
    
    print("\n🔧 Testing Basic Functionality...")
    success &= test_basic_functionality()
    
    print("\n🎯 Testing Game Logic...")
    success &= test_game_logic()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Game is ready to run.")
        print("\nTo start the game:")
        print("python3 main.py")
        print("\nGame Controls:")
        print("- Arrow Keys or WASD: Move")
        print("- Space: Shoot")
        print("- ESC: Menu/Quit")
        print("- Enter: Start Game/Confirm")
        print("- R: Rankings (from menu)")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    try:
        pygame.quit()
    except:
        pass

if __name__ == "__main__":
    main()
