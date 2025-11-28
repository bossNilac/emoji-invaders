from operator import index

import pygame

from config import MEASURE_UNIT_SPACE, MEASURE_UNIT_SIZE, WIDTH, ENEMY_MOVE_SPEED
from sprites.Easy_Enemy import EasyEnemy
from sprites.Hard_Enemy import HardEnemy
from sprites.Medium_Enemy import MediumEnemy

enemies_row_5 = pygame.sprite.Group()
enemies_row_4 = pygame.sprite.Group()
enemies_row_3 = pygame.sprite.Group()
enemies_row_2 = pygame.sprite.Group()
enemies_row_1 = pygame.sprite.Group()

ENEMY_ROWS = [
    enemies_row_5,
    enemies_row_4,
    enemies_row_3,
    enemies_row_2,
    enemies_row_1,
]

ALL_ENEMIES = pygame.sprite.Group()

rendered = False

going_left = False


def _add_enemy_to_row(enemy, row_group):
    row_group.add(enemy)
    ALL_ENEMIES.add(enemy)


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


def _clear_all_enemies():
    for row in ENEMY_ROWS:
        row.empty()
    ALL_ENEMIES.empty()


def render_enemies(screen):
    global rendered

    if not rendered:
        _clear_all_enemies()

        start_y = 0
        start_x = 125
        for _ in range(10):
            start_x += MEASURE_UNIT_SPACE
            add_hard_enemy(start_x, start_y)

        for _ in range(2):
            start_x = 125
            start_y += MEASURE_UNIT_SIZE
            for _ in range(10):
                start_x += MEASURE_UNIT_SPACE
                add_medium_enemy(start_x, start_y)

        for _ in range(2):
            start_x = 125
            start_y += MEASURE_UNIT_SIZE
            for _ in range(10):
                start_x += MEASURE_UNIT_SPACE
                add_easy_enemy(start_x, start_y)

        rendered = True

    draw_enemies(screen)

def move(enemy):
    if going_left:
        enemy.rect.x -= ENEMY_MOVE_SPEED
    else:
        enemy.rect.x += ENEMY_MOVE_SPEED

def switch_direction():
    global going_left
    going_left = not going_left


def switch_row_all():
    """Move the entire formation down by one row."""
    for row in ENEMY_ROWS:
        for enemy in row.sprites():
            enemy.rect.y += MEASURE_UNIT_SIZE


def update_enemies(screen):
    global rendered

    if not rendered:
        render_enemies(screen)
        return

    edge_hit = False

    # 1) Move all enemies horizontally
    for row in ENEMY_ROWS:
        for enemy in row.sprites():
            move(enemy)
            # Detect if any enemy hits the edge
            if enemy.rect.left <= 0 or enemy.rect.right >= WIDTH:
                edge_hit = True

    # 2) If any enemy hit the edge: reverse direction + move whole block down
    if edge_hit:
        switch_direction()
        switch_row_all()

    # 3) Respawn when all are dead
    if all(not row.sprites() for row in ENEMY_ROWS):
        rendered = False
        render_enemies(screen)

