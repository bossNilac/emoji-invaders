import pygame

from game_logic import enemy_factory
from config import ASSETS_DIR, SHOOTING_DELAY, MEASURE_UNIT_SIZE
from sprites.Bullet import Bullet

total_enemies_killed = 0

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
        self.move_speed = 5
        self.bolt_until = 0
        self.fast_until = 0

    def move(self):
        self.update_power_ups()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rocket_x -= self.move_speed
        if keys[pygame.K_d]:
            self.rocket_x += self.move_speed
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.start_tick > self.get_shooting_delay():
                self.shoot()

        if self.rocket_x > 800:
            self.rocket_x = 0
        if self.rocket_x < 0:
            self.rocket_x = 800
        self.rect.midtop = (self.rocket_x, 550)

    def shoot(self):
        self.bullets.add(Bullet(False,player=self))
        self.start_tick = pygame.time.get_ticks()

    def get_shooting_delay(self):
        if pygame.time.get_ticks() < self.bolt_until:
            return SHOOTING_DELAY / 4
        return SHOOTING_DELAY

    def update_power_ups(self):
        if pygame.time.get_ticks() < self.fast_until:
            self.move_speed = 10
        else:
            self.move_speed = 5

    def apply_power_up(self, power_up_type):
        now = pygame.time.get_ticks()
        if power_up_type == "bolt":
            self.bolt_until = now + 5000
        elif power_up_type == "fast":
            self.fast_until = now + 5000
        elif power_up_type == "shield":
            enemy_factory.respawn_shields()

    def check_collisions(self):
        for enemy in enemy_factory.ALL_ENEMIES.sprites():
            if enemy.rect.colliderect(self.rect):
                self.kill()
                pygame.event.post(pygame.event.Event(pygame.NOEVENT))

    def update(self):
        self.move()
        self.bullets.update()
        self.check_collisions()
        self.bullets.draw(self.surface)


