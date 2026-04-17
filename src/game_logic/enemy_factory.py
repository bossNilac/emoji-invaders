import pygame

from config import MEASURE_UNIT_SPACE, MEASURE_UNIT_SIZE, WIDTH, ENEMY_MOVE_SPEED, TOTAL_ENEMIES_COUNT
from sprites import player
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

        start_y = 70
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

        rendered = True

    draw_enemies(screen)

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


def update_enemies(p,screen):
    global rendered

    if not rendered:
        render_enemies(screen)
        return

    edge_hit = False

    for row in ENEMY_ROWS:
        for enemy in row.sprites():
            move(enemy)
            enemy.update_bullets(p,screen)
            if enemy.rect.left <= 0 or enemy.rect.right >= WIDTH:
                edge_hit = True

    if edge_hit:
        switch_direction()
        switch_row_all()


    if all(not row.sprites() for row in ENEMY_ROWS):
        rendered = False
        render_enemies(screen)

def on_game_reset():
    _clear_all_enemies()
    global rendered
    rendered = False

