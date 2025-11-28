import pygame
from sys import exit

from pygame import key

pygame.init()

rocket_x = 50


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Emoji Invaders")

clock = pygame.time.Clock()

angry_emoji = pygame.image.load('assets/angry.png').convert_alpha()
angry_emoji = pygame.transform.scale(angry_emoji,(50,50))
angry_rect = angry_emoji.get_rect(midtop= (770,550))


rocket = pygame.image.load('assets/rocket.png').convert_alpha()
rocket = pygame.transform.scale(rocket,(50,50))
rocket_rect = rocket.get_rect(midtop= (rocket_x,550))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()



    screen.fill((0,0,0))
    screen.blit(angry_emoji,angry_rect)
    screen.blit(rocket,rocket_rect)
    rocket_rect.midtop = (rocket_x,550)
    if rocket_x > 800:
        rocket_x = 0
    if rocket_x < 0:
        rocket_x = 800

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        rocket_x -= 5
    if keys[pygame.K_d]:
        rocket_x += 5



    pygame.display.update()
    print(rocket_rect.colliderect(angry_rect))
    clock.tick(60)