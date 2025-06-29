# QGamen_DanmakuShooting

A bullet hell shooting game developed with Pygame.

## Description

This is a classic-style bullet hell (danmaku) shooting game where players control a ship and dodge intricate bullet patterns while defeating enemies.

## Features

- Classic bullet hell gameplay
- Multiple enemy types with unique bullet patterns
- Power-up system
- Score tracking
- Smooth 60 FPS gameplay

## Requirements

- Python 3.7+
- Pygame 2.0+

## Installation

1. Clone this repository:
```bash
git clone https://github.com/<username>/QGamen_DanmakuShooting.git
cd QGamen_DanmakuShooting
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the game:
```bash
python main.py
```

## Controls

- Arrow Keys: Move player
- Space: Shoot
- ESC: Pause/Menu

## Development

### Project Structure

```
QGamen_DanmakuShooting/
├── main.py              # Main game entry point
├── src/                 # Source code
│   ├── game.py         # Main game class
│   ├── player.py       # Player class
│   ├── enemy.py        # Enemy classes
│   ├── bullet.py       # Bullet classes
│   ├── powerup.py      # Power-up system
│   └── utils.py        # Utility functions
├── assets/             # Game assets
│   ├── images/         # Sprite images
│   ├── sounds/         # Sound effects
│   └── fonts/          # Font files
├── tests/              # Unit tests
└── docs/               # Documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by classic bullet hell games like Touhou series
- Built with Pygame community support
