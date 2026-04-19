# Emoji Invaders Design Notes

## High-Level Flow

Emoji Invaders is built around a straightforward Pygame game loop in `main.py`. The program initializes Pygame, sets up the display and fonts, loads the background and icon, initializes the score and audio systems, and then switches between a menu loop and the active game loop.

The active game loop draws the background, starts the looping music, renders the score, draws enemy-related sprites, updates the player, updates all enemy logic, and refreshes the display at a fixed FPS. The menu loop is separate and handles the play/quit buttons plus the persisted high score display.

The architecture is simple and direct: `main.py` owns the application loop, `enemy_factory.py` manages wave state, `player.py` owns player-side input and temporary boosts, and the sprite modules hold behavior for bullets, enemies, shields, bosses, and drops.

## Core Gameplay Systems

### Player

The player is implemented as a `pygame.sprite.Sprite` in `sprites/player.py`. It stores horizontal position, a bullet group, and two temporary power-up timers.

Movement is keyboard-driven:
- `A` moves left
- `D` moves right
- `Space` fires if enough time has passed since the last shot

The player wraps around the screen horizontally instead of clamping at the edges. The shooting delay normally comes from `SHOOTING_DELAY`, but the bolt power-up reduces it to one quarter for five seconds. The fast power-up increases movement speed for five seconds.

Player death can happen in two ways:
- direct collision with an enemy sprite
- collision with an enemy bullet

The player also triggers the death sound and posts a `pygame.NOEVENT` to end the current run and return control to the menu flow.

### Bullets

`sprites/Bullet.py` handles both player bullets and enemy bullets with one class. The behavior changes based on the `is_from_enemy` flag.

Player bullets:
- spawn from the player’s `midtop`
- move upward
- destroy the first enemy they collide with

Enemy bullets:
- spawn from the enemy’s lower center
- move downward
- kill the player on collision

Both bullet types can destroy shields. This is handled before enemy collision, so shields work as a shared layer of protection.

### Enemies

The base enemy behavior lives in `sprites/EnemySprite.py`. Each enemy stores:
- sprite image and position
- score value
- `importance`
- shooting state
- optional bullet

The actual enemy subclasses are lightweight wrappers:

- `EasyEnemy`: importance 1, score 15
- `MediumEnemy`: importance 2, score 20
- `HardEnemy`: importance 3, score 30
- `Ufo_Enemy`: importance 4, score 50

The base class also handles death, score updates, and power-up drop attempts.

## Enemy Wave Management

The main enemy system is centralized in `game_logic/enemy_factory.py`. This file is effectively the wave controller for the game.

It owns several sprite groups:
- separate row groups for the main formation
- a UFO row
- a boss row
- shield and power-up groups
- aggregate groups such as `ALL_ENEMIES` and `ALL_SHIELDS`

The wave is only spawned when the system is marked as not yet rendered. At that point the factory:
1. clears the previous wave state
2. increments the round counter
3. decides whether the next wave is a boss round
4. optionally spawns a UFO
5. spawns the normal enemy rows if it is not a boss round
6. spawns shields in random positions

This means a “round” is effectively one full generated wave, and boss rounds occur every third wave.

## Boss Design

The boss is implemented in `sprites/BossSprite.py` as a subclass of the base enemy class, but it overrides several behaviors.

Key differences:
- it uses a much larger image than the standard enemies
- it appears alone on boss rounds
- it has a resistance value and only dies after multiple hits
- it moves horizontally on its own instead of following the formation
- it shakes briefly when hit
- it fires much faster than regular enemies
- every five boss shots, it spawns a random power-up

In practice, the boss is treated as part of the general enemy system, but it is intentionally excluded from the normal formation movement and edge-triggered row drops.

## UFO Behavior

The UFO is a special enemy spawned randomly at the top of non-boss rounds. It lives in its own row and is updated separately from the regular enemy formation.

Its horizontal movement is random in direction and independent of the formation’s edge logic. It still gets drawn and updated as part of the shared enemy system, but its movement pattern is distinct.

## Shields

Shields are simple stationary sprites created in `sprites/Shield.py`. They are spawned one row above the player and are managed by `enemy_factory.py`.

Current behavior:
- shields are randomly positioned from a predefined spaced set of x coordinates
- a bullet from either side destroys a shield on contact
- the shield power-up clears and respawns the shield set

This keeps shield handling simple while still making them part of the game’s risk/reward loop.

## Power-Ups

Power-ups are implemented as falling sprite pickups in `sprites/PowerUp.py`. They are intentionally treated more like collectible bullets than like a separate inventory system.

There are three types:
- `bolt`: rapid fire for 5 seconds
- `fast`: faster player movement for 5 seconds
- `shield`: respawns the shield line

Drop rules currently implemented:
- normal enemies: random 5% to 10% drop chance
- UFO: 33% drop chance
- boss: spawns one random power-up every five bullets fired

The power-up implementation is reasonably lightweight. The player does not maintain a list of active effects; instead, it uses timestamp-based timers. That keeps the feature easy to extend and keeps the player update loop simple.

One practical optimization already present is image caching inside `PowerUp.py`, so repeated drops do not constantly reload and rescale images from disk.

## Scoring and High Score

Scoring is handled by `game_logic/score.py`. It uses module-level state rather than a class instance shared around the project. The module stores the current score, renders the text surface, and exposes helper functions like `update_score()`, `get_score()`, `render_score()`, and `reset()`.

Persistent high score storage is handled in `config.py` using `configparser`. The high score is written to and read from `assets/highscore.emoji`. This is a simple approach, but it works well for a student project and keeps persistence logic easy to understand.

## Audio

Audio is handled in `game_logic/audio_factory.py` using `pygame.mixer`. The module lazily initializes audio and then exposes small helpers for:
- looping background music
- player shooting
- enemy death
- player death

The game loop calls `audio_loop()` each frame, but the method only starts playback if the music channel is not already busy. This is a practical, low-complexity way to keep background music running.

## Difficulty Scaling

There are two main difficulty scaling mechanisms in the current codebase.

### Enemy movement speed

The regular formation gets faster as more enemies are eliminated. The speed function is:

```python
progress = 1 - (enemies_left / TOTAL_ENEMIES_COUNT)
speed = ENEMY_MOVE_SPEED + (progress ** 2) * 0.8
```

This creates a gradual acceleration curve instead of a linear jump.

### Enemy shooting rate

Enemy shooting is also influenced by `importance`, which functions as a rough aggression level.

Regular enemy shooting currently uses:

```python
effective_delay = (SHOOTING_DELAY * max(1, 5 - self.importance)) / ((total_enemies_killed // 10) + 1)
```

That means:
- higher-importance enemies shoot more frequently
- enemies generally shoot faster later in a wave
- the acceleration is moderated by a coarse kill-based divisor instead of ramping every single kill

The boss overrides this with its own much faster firing formula.

## Architecture and Interactions

This project uses a fairly common small-game structure built around shared modules and sprite groups.

Some notable interactions:
- `main.py` drives rendering and frame updates
- `enemy_factory.py` owns wave construction, enemy groups, shields, and power-ups
- `player.py` owns input, movement, shooting, and timed boosts
- `EnemySprite.py` defines shared enemy behavior used by all enemy variants
- `BossSprite.py` extends the base enemy without needing a separate boss system
- `Bullet.py` acts as the collision bridge between player, enemies, and shields
- `audio_factory.py` and `score.py` are simple service-style modules

## Strengths

A strong part of the project is that it layers new mechanics onto a familiar arcade base without losing readability. Boss waves, UFOs, destructible shields, power-ups, and audio are all integrated into the same loop without requiring a large framework.

The use of dedicated sprite classes plus a central wave factory also makes the feature set easier to reason about. There is a clear place to look for player behavior, enemy behavior, and wave setup.

Another strength is that the project already includes enough variation to feel like more than a minimal clone. The additions change the pacing of the game in visible ways.

## Current Limitations

The main limitation is coupling. `enemy_factory.py` has become the home for several unrelated responsibilities: spawning waves, moving enemies, tracking rounds, managing shields, tracking current player state, and handling power-up creation. It works, but it is carrying a lot of logic.

A second limitation is that several systems rely on module-level globals. That keeps the code short, but it also makes some behaviors harder to isolate or test.

Balancing is also still a moving target. Because movement speed, shot timing, boss frequency, and drop logic all interact, small tuning changes can have a large effect on the overall difficulty curve.

## Possible Next Refactors

If I were to expand this project further, the next useful refactors would probably be:
- separating wave generation from per-frame enemy updates
- moving power-up spawning into its own small manager
- consolidating timing formulas into configuration values
- cleaning up global state so fewer modules need to know about each other directly

This project definitely made my understanding of game development more in depth and taught me a different way I can apply my programming skills for.