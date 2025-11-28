import pygame

from config import WIDTH, MEASURE_UNIT_SPACE, MEASURE_UNIT_SIZE
from sprites.Easy_Enemy import EasyEnemy
from sprites.Hard_Enemy import HardEnemy
from sprites.Medium_Enemy import MediumEnemy

enemies = pygame.sprite.Group()

rendered = False

def add_hard_enemy(x,y):
    print("Added Hard enemy")
    enemies.add(HardEnemy(x, y))

def add_medium_enemy(x,y):
    print("Added Medium enemy")
    enemies.add(MediumEnemy(x, y))

def add_easy_enemy(x,y):
    print("Added Easy enemy")
    enemies.add(EasyEnemy(x, y))

def render_enemies(screen):
    global rendered
    if not rendered:
        start_x = 125
        start_y = 0
        for i in range(10) :
            start_x += MEASURE_UNIT_SPACE
            add_hard_enemy(start_x,start_y)
        for i in range(2):
            start_x = 125
            start_y += MEASURE_UNIT_SIZE
            for j in range(10) :
                start_x += MEASURE_UNIT_SPACE
                add_medium_enemy(start_x,start_y)
        for i in range(2):
            start_x = 125
            start_y += MEASURE_UNIT_SIZE
            for j in range(10) :
                start_x += MEASURE_UNIT_SPACE
                add_easy_enemy(start_x, start_y)
        rendered = True
    enemies.draw(screen)

def update_enemies():
    global rendered
    if not rendered:
        enemies.update()