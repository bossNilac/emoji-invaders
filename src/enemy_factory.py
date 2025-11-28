import pygame

from config import WIDTH
from sprites.Hard_Enemy import HardEnemy

enemies = pygame.sprite.Group()

rendered = False

def add_hard_enemy(x,y):
    print("Added enemy")
    enemies.add(HardEnemy(x,y))

def render_hard_enemies(screen):
    global rendered
    if not rendered:
        start_x = 0
        start_y = 0
        for i in range(int(WIDTH/50) -1):
            start_x += 50
            add_hard_enemy(start_x,start_y)
        rendered = True
    enemies.draw(screen)

def update_hard_enemies():
    global rendered
    if not rendered:
        enemies.update()
