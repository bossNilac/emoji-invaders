from sys import exit

import pygame

from sprites.Player import Player

pygame.init()



screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Emoji Invaders")

clock = pygame.time.Clock()

player = pygame.sprite.GroupSingle()

player.add(Player(screen))

angry_emoji = pygame.image.load('assets/angry.png').convert_alpha()
angry_emoji = pygame.transform.scale(angry_emoji,(50,50))
angry_rect = angry_emoji.get_rect(midtop= (770,550))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()



    screen.fill((0,0,0))
    screen.blit(angry_emoji,angry_rect)
    player.draw(screen)
    player.update()




    pygame.display.update()
    clock.tick(60)