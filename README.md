# Emoji Invaders

## Overview

Emoji Invaders is an arcade shooter inspired by classic Space Invaders gameplay. The project recreates the core loop of moving enemy waves, player shooting, and escalating pressure, while adding modern features such as power-ups, boss fights, audio feedback, persistent high scores, and difficulty scaling.

## Gameplay

<video src="https://github.com/bossNilac/emoji-invaders/blob/main/docs/space-invaders.mp4" controls></video>

This should be a short, sped-up gameplay preview that shows the flow of a full round, enemy patterns, power-up drops, and a boss wave.

## Features

- Classic fixed-screen arcade gameplay inspired by Space Invaders
- Multiple enemy types with different score values and shooting behavior
- Random UFO encounters above the main formation
- Boss-only rounds that appear every three rounds
- Boss health system that requires multiple hits to defeat
- Power-ups for rapid fire, faster movement, and shield restoration
- Destructible shields placed between the player and enemies
- Enemy bullet patterns and player bullet collision system
- Score tracking during gameplay
- Persistent high score stored locally in `highscore.emoji`
- Main menu with play/continue flow and visible high score
- Background music plus shooting, enemy death, and player death sound effects
- Difficulty scaling for enemy movement and shooting across a wave

## Controls

- `A`: Move left
- `D`: Move right
- `Space`: Shoot
- `Escape`: Return to the menu / continue later
- Mouse click: Start or quit from the main menu

## Tech Stack

- Python
- Pygame
- Standard library modules such as `os` and `configparser`

## How to Run

1. Create and activate a virtual environment.
2. Install Pygame:
   ```bash
   pip install pygame
   ```
3. Run the game from the `src` directory:
   ```bash
   python main.py
   ```

Notes:
- The project expects the `assets/` folder to remain inside `src/`.
- Audio files, sprite images, and the high score file are loaded from that folder.
- The high score file is stored as `src/assets/highscore.emoji`.

## Project Structure

```text
src/
├── main.py
├── config.py
├── assets/
│   ├── sprite images
│   ├── sound effects
│   ├── music
│   └── highscore.emoji
├── game_logic/
│   ├── audio_factory.py
│   ├── enemy_factory.py
│   └── score.py
└── sprites/
    ├── player.py
    ├── Bullet.py
    ├── EnemySprite.py
    ├── Easy_Enemy.py
    ├── Medium_Enemy.py
    ├── Hard_Enemy.py
    ├── Ufo_Enemy.py
    ├── BossSprite.py
    ├── Shield.py
    └── PowerUp.py
```

## What I Learned

- How to structure a real-time game loop in Pygame
- How to organize game logic into factories, sprite classes, and shared configuration
- How to manage collision systems between enemies, bullets, shields, and power-ups
- How to balance arcade mechanics like spawn rates, speed scaling, and shot timing
- How to add persistent data such as a saved high score
- How to integrate sound effects and looping background audio into gameplay events

## Challenges

- Balancing enemy movement and shooting so the game stays difficult without feeling unfair
- Coordinating multiple sprite groups at once: enemies, shields, bullets, UFOs, bosses, and power-ups
- Preventing feature additions like boss fights and drops from making the main loop too complex
- Making timed power-ups interact cleanly with existing player movement and shooting logic
- Handling audio initialization safely inside a Pygame project
- Keeping the game responsive as more systems were layered in over time

## Future Improvements
If I were to continue this project I would probably do/fix the following:

- Add a proper game over screen
- Improve balancing for power-up frequency and boss pacing
- Introduce animations, particle effects, and smoother hit feedback
- Add enemy bullet variety and more boss attack patterns
- Refactor some systems to reduce coupling between factories and sprite classes
- Add automated tests for helper logic such as score persistence and drop chances
