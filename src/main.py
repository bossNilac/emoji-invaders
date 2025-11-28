from sys import exit

import pygame

import config
from config import FPS, HEIGHT, WIDTH, BLACK
from enemy_factory import update_enemies, render_enemies
from sprites.Player import Player

pygame.init()



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Emoji Invaders")
icon= pygame.image.load(config.ASSETS_DIR + 'rocket.png').convert()
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

player = pygame.sprite.GroupSingle()

player.add(Player(screen))



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill(BLACK)
    render_enemies(screen)
    player.draw(screen)
    player.update()
    update_enemies(screen)



    pygame.display.update()
    clock.tick(FPS)