import random

import pygame

from config import MEASURE_UNIT_SPACE, MEASURE_UNIT_SIZE, WIDTH, ENEMY_MOVE_SPEED, TOTAL_ENEMIES_COUNT, UFO_SPAWN_CHANCE
from sprites import player
from sprites.Easy_Enemy import EasyEnemy
from sprites.Hard_Enemy import HardEnemy
from sprites.Medium_Enemy import MediumEnemy
from sprites.Shield import Shield
from sprites.Ufo_Enemy import Ufo_Enemy

ufo_row = pygame.sprite.Group()
enemies_row_5 = pygame.sprite.Group()
enemies_row_4 = pygame.sprite.Group()
enemies_row_3 = pygame.sprite.Group()
enemies_row_2 = pygame.sprite.Group()
enemies_row_1 = pygame.sprite.Group()
shields = pygame.sprite.Group()

ENEMY_ROWS = [
    ufo_row,
    enemies_row_5,
    enemies_row_4,
    enemies_row_3,
    enemies_row_2,
    enemies_row_1,
]

ALL_ENEMIES = pygame.sprite.Group()
ALL_SHIELDS = pygame.sprite.Group()


rendered = False
going_left = False
ufo_going_left = bool(random.randint(0, 1))
ufo_move_tick = 0

def _add_enemy_to_row(enemy, row_group):
    row_group.add(enemy)
    ALL_ENEMIES.add(enemy)


def add_ufo_enemy(x, y):
    print("Added Ufo enemy")
    enemy = Ufo_Enemy(x, y)
    _add_enemy_to_row(enemy, ufo_row)


def add_hard_enemy(x, y):
    print("Added Hard enemy")
    enemy = HardEnemy(x, y)
    _add_enemy_to_row(enemy, enemies_row_5)


def add_medium_enemy(x, y):
    print("Added Medium enemy")
    enemy = MediumEnemy(x, y)

    if len(enemies_row_4.sprites()) >= 10:
        _add_enemy_to_row(enemy, enemies_row_3)
    else:
        _add_enemy_to_row(enemy, enemies_row_4)


def add_easy_enemy(x, y):
    print("Added Easy enemy")
    enemy = EasyEnemy(x, y)

    if len(enemies_row_2.sprites()) >= 10:
        _add_enemy_to_row(enemy, enemies_row_1)
    else:
        _add_enemy_to_row(enemy, enemies_row_2)


def draw_enemies(screen):
    for row in ENEMY_ROWS:
        row.draw(screen)


def add_shield(x, y):
    print("Added Shield")
    shield = Shield(x, y)
    shields.add(shield)
    ALL_SHIELDS.add(shield)


def draw_shields(screen):
    shields.draw(screen)


def _clear_all_enemies():
    for row in ENEMY_ROWS:
        row.empty()
    ALL_ENEMIES.empty()


def _clear_all_shields():
    shields.empty()
    ALL_SHIELDS.empty()


def render_enemies(screen):
    global rendered

    if not rendered:
        _clear_all_enemies()
        _clear_all_shields()

        start_y = 30
        if random.random() < UFO_SPAWN_CHANCE:
            add_ufo_enemy(WIDTH // 2, start_y)

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
        for shield_x in [150, 300, 500, 650]:
            add_shield(shield_x, shield_y)

        rendered = True

    draw_enemies(screen)
    draw_shields(screen)

def move(enemy):
    speed = get_enemy_speed(50 - player.total_enemies_killed % 50)
    if going_left:
        enemy.rect.x -= speed
    else:
        enemy.rect.x += speed

def get_enemy_speed(enemies_left):
    progress = 1 - (enemies_left / TOTAL_ENEMIES_COUNT)
    return ENEMY_MOVE_SPEED + (progress ** 2) * 2.0

def switch_direction():
    global going_left
    going_left = not going_left


def switch_row_all():
    for row in ENEMY_ROWS:
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


def update_enemies(p,screen):
    global rendered

    if not rendered:
        render_enemies(screen)
        return

    edge_hit = False

    for row in ENEMY_ROWS:
        for enemy in row.sprites():
            if row != ufo_row:
                move(enemy)
            enemy.update_bullets(p,screen)
            if row != ufo_row and (enemy.rect.left <= 0 or enemy.rect.right >= WIDTH):
                edge_hit = True

    move_ufo()

    if edge_hit:
        switch_direction()
        switch_row_all()


    if all(not row.sprites() for row in ENEMY_ROWS):
        rendered = False
        render_enemies(screen)

def on_game_reset():
    _clear_all_enemies()
    _clear_all_shields()
    global rendered
    rendered = False
    player.total_enemies_killed = 0

