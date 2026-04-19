import random

import pygame

from config import MEASURE_UNIT_SPACE, MEASURE_UNIT_SIZE, WIDTH, ENEMY_MOVE_SPEED, TOTAL_ENEMIES_COUNT, UFO_SPAWN_CHANCE
from sprites.BossSprite import BossSprite
from sprites import player
from sprites.Easy_Enemy import EasyEnemy
from sprites.Hard_Enemy import HardEnemy
from sprites.Medium_Enemy import MediumEnemy
from sprites.PowerUp import PowerUp
from sprites.Shield import Shield
from sprites.Ufo_Enemy import Ufo_Enemy

boss_row = pygame.sprite.Group()
ufo_row = pygame.sprite.Group()
enemies_row_5 = pygame.sprite.Group()
enemies_row_4 = pygame.sprite.Group()
enemies_row_3 = pygame.sprite.Group()
enemies_row_2 = pygame.sprite.Group()
enemies_row_1 = pygame.sprite.Group()
shields = pygame.sprite.Group()
power_ups = pygame.sprite.Group()

ENEMY_ROWS = [
    boss_row,
    ufo_row,
    enemies_row_5,
    enemies_row_4,
    enemies_row_3,
    enemies_row_2,
    enemies_row_1,
]

ALL_ENEMIES = pygame.sprite.Group()
ALL_SHIELDS = pygame.sprite.Group()
ALL_POWER_UPS = pygame.sprite.Group()


rendered = False
going_left = False
ufo_going_left = bool(random.randint(0, 1))
ufo_move_tick = 0
round_count = 0
current_player_group = None

def _add_enemy_to_row(enemy, row_group):
    row_group.add(enemy)
    ALL_ENEMIES.add(enemy)


def add_ufo_enemy(x, y):
    enemy = Ufo_Enemy(x, y)
    _add_enemy_to_row(enemy, ufo_row)


def add_boss_enemy(x, y):
    enemy = BossSprite(x, y)
    _add_enemy_to_row(enemy, boss_row)


def add_hard_enemy(x, y):
    enemy = HardEnemy(x, y)
    _add_enemy_to_row(enemy, enemies_row_5)


def add_medium_enemy(x, y):
    enemy = MediumEnemy(x, y)

    if len(enemies_row_4.sprites()) >= 10:
        _add_enemy_to_row(enemy, enemies_row_3)
    else:
        _add_enemy_to_row(enemy, enemies_row_4)


def add_easy_enemy(x, y):
    enemy = EasyEnemy(x, y)

    if len(enemies_row_2.sprites()) >= 10:
        _add_enemy_to_row(enemy, enemies_row_1)
    else:
        _add_enemy_to_row(enemy, enemies_row_2)


def draw_enemies(screen):
    for row in ENEMY_ROWS:
        row.draw(screen)


def add_shield(x, y):
    shield = Shield(x, y)
    shields.add(shield)
    ALL_SHIELDS.add(shield)


def draw_shields(screen):
    shields.draw(screen)


def add_power_up(power_up_type, x, y):
    power_up = PowerUp(power_up_type, current_player_group, x, y)
    power_ups.add(power_up)
    ALL_POWER_UPS.add(power_up)


def draw_power_ups(screen):
    power_ups.draw(screen)


def _clear_all_enemies():
    for row in ENEMY_ROWS:
        row.empty()
    ALL_ENEMIES.empty()


def _clear_all_shields():
    shields.empty()
    ALL_SHIELDS.empty()


def _clear_all_power_ups():
    power_ups.empty()
    ALL_POWER_UPS.empty()


def get_random_shield_positions():
    possible_positions = list(range(100, WIDTH - 100, MEASURE_UNIT_SPACE * 2))
    return sorted(random.sample(possible_positions, 4))


def respawn_shields():
    _clear_all_shields()
    shield_y = 550 - MEASURE_UNIT_SIZE
    for shield_x in get_random_shield_positions():
        add_shield(shield_x, shield_y)


def spawn_random_power_up(x, y):
    if current_player_group is None:
        return
    add_power_up(random.choice(["bolt", "fast", "shield"]), x, y)


def try_spawn_power_up_from_enemy(enemy):
    if enemy.__class__.__name__ == "BossSprite":
        return

    if enemy.__class__.__name__ == "Ufo_Enemy":
        drop_chance = 0.33
    else:
        drop_chance = random.uniform(0.05, 0.10)

    if random.random() < drop_chance:
        spawn_random_power_up(enemy.rect.centerx, enemy.rect.bottom)


def render_enemies(screen):
    global rendered
    global round_count

    if not rendered:
        round_count += 1
        _clear_all_enemies()
        _clear_all_shields()
        _clear_all_power_ups()

        start_y = 30
        is_boss_round = round_count % 3 == 0

        if is_boss_round:
            add_boss_enemy(WIDTH // 2, start_y)
        elif random.random() < UFO_SPAWN_CHANCE:
            add_ufo_enemy(WIDTH // 2, start_y)

        if not is_boss_round:
            start_y += MEASURE_UNIT_SIZE
            start_x = 0
            for _ in range(10):
                start_x += MEASURE_UNIT_SPACE
                add_hard_enemy(start_x, start_y)

            for _ in range(2):
                start_x = 0
                start_y += MEASURE_UNIT_SIZE
                for _ in range(10):
                    start_x += MEASURE_UNIT_SPACE
                    add_medium_enemy(start_x, start_y)

            for _ in range(2):
                start_x = 0
                start_y += MEASURE_UNIT_SIZE
                for _ in range(10):
                    start_x += MEASURE_UNIT_SPACE
                    add_easy_enemy(start_x, start_y)

        shield_y = 550 - MEASURE_UNIT_SIZE
        for shield_x in get_random_shield_positions():
            add_shield(shield_x, shield_y)

        rendered = True

    draw_enemies(screen)
    draw_shields(screen)
    draw_power_ups(screen)

def move(enemy):
    speed = get_enemy_speed(50 - player.total_enemies_killed % 50)
    if going_left:
        enemy.rect.x -= speed
    else:
        enemy.rect.x += speed

def get_enemy_speed(enemies_left):
    progress = 1 - (enemies_left / TOTAL_ENEMIES_COUNT)
    return ENEMY_MOVE_SPEED + (progress ** 2) * 0.8

def switch_direction():
    global going_left
    going_left = not going_left


def switch_row_all():
    for row in ENEMY_ROWS:
        if row == boss_row:
            continue
        for enemy in row.sprites():
            enemy.rect.y += MEASURE_UNIT_SIZE


def move_ufo():
    global ufo_going_left
    global ufo_move_tick

    if not ufo_row.sprites():
        return

    now = pygame.time.get_ticks()
    if now - ufo_move_tick > 650:
        ufo_going_left = bool(random.randint(0, 1))
        ufo_move_tick = now

    for enemy in ufo_row.sprites():
        if ufo_going_left:
            enemy.rect.x -= ENEMY_MOVE_SPEED * 3
        else:
            enemy.rect.x += ENEMY_MOVE_SPEED * 3

        if enemy.rect.left <= 0:
            enemy.rect.left = 0
            ufo_going_left = False
        if enemy.rect.right >= WIDTH:
            enemy.rect.right = WIDTH
            ufo_going_left = True


def move_boss():
    for enemy in boss_row.sprites():
        enemy.move()


def update_enemies(p,screen):
    global rendered
    global current_player_group
    current_player_group = p

    if not rendered:
        render_enemies(screen)
        return

    edge_hit = False

    for row in ENEMY_ROWS:
        for enemy in row.sprites():
            if row != ufo_row and row != boss_row:
                move(enemy)
            enemy.update_bullets(p,screen)
            if row != ufo_row and row != boss_row and (enemy.rect.left <= 0 or enemy.rect.right >= WIDTH):
                edge_hit = True

    move_ufo()
    move_boss()
    power_ups.update()

    if edge_hit:
        switch_direction()
        switch_row_all()


    if all(not row.sprites() for row in ENEMY_ROWS):
        rendered = False
        render_enemies(screen)

def on_game_reset():
    _clear_all_enemies()
    _clear_all_shields()
    _clear_all_power_ups()
    global rendered
    global round_count
    global current_player_group
    rendered = False
    round_count = 0
    current_player_group = None
    player.total_enemies_killed = 0
