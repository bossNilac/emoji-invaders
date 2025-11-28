import pygame

from config import ASSETS_DIR, SHOOTING_DELAY, MEASURE_UNIT_SIZE
from sprites.Bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self,surface):

        pygame.sprite.Sprite.__init__(self)
        self.image = (pygame.transform.scale
                      (pygame.image.load
                       (ASSETS_DIR+'rocket.png').convert_alpha(),
                       (MEASURE_UNIT_SIZE, MEASURE_UNIT_SIZE)))
        self.rect = self.image.get_rect(midtop= (50,550))
        self.rocket_x = 50
        self.bullets = pygame.sprite.Group()
        self.surface = surface
        self.start_tick = pygame.time.get_ticks()
        self.current_tick = pygame.time.get_ticks()

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rocket_x -= 5
        if keys[pygame.K_d]:
            self.rocket_x += 5
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.start_tick > SHOOTING_DELAY:
                self.shoot()

        if self.rocket_x > 800:
            self.rocket_x = 0
        if self.rocket_x < 0:
            self.rocket_x = 800
        self.rect.midtop = (self.rocket_x, 550)

    def shoot(self):
        self.bullets.add(Bullet(self))
        self.start_tick = pygame.time.get_ticks()

    def update(self):
        self.move()
        self.bullets.update()
        self.bullets.draw(self.surface)


