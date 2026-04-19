import pygame

from config import ASSETS_DIR, MEASURE_UNIT_SIZE, SHOOTING_DELAY, WIDTH
from sprites.EnemySprite import Enemy
from sprites.Bullet import Bullet
from sprites.player import total_enemies_killed


class BossSprite(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "boss", 20, 1000)
        self.image = (pygame.transform.scale
                      (pygame.image.load
                       (ASSETS_DIR + "boss.png").convert_alpha(),
                       (MEASURE_UNIT_SIZE * 4, MEASURE_UNIT_SIZE * 4)))
        self.rect = self.image.get_rect(midtop=(x, y))
        self.resistance = 8
        self.real_x = float(self.rect.x)
        self.move_speed = 10
        self.move_right = True
        self.shake_until = 0
        self.shake_strength = 8

    def move(self):
        if self.move_right:
            self.real_x += self.move_speed
        else:
            self.real_x -= self.move_speed

        if self.real_x <= 0:
            self.real_x = 0
            self.move_right = True
        if self.real_x + self.rect.width >= WIDTH:
            self.real_x = WIDTH - self.rect.width
            self.move_right = False

        self.rect.x = int(self.real_x)

        if pygame.time.get_ticks() < self.shake_until:
            self.rect.x += self.shake_strength if pygame.time.get_ticks() % 2 == 0 else -self.shake_strength

    def shoot_back(self,p):
        now = pygame.time.get_ticks()
        if self.shooter and not self.bullet:
            if now - self.shoot_tick > SHOOTING_DELAY / (self.importance * 4 * ((total_enemies_killed//2) + 1)):
                self.bullet = Bullet(True, p, self.rect.centerx, self.rect.bottom)
                self.shoot_tick = pygame.time.get_ticks()
                return True
        return False

    def die(self):
        self.resistance -= 1
        self.shake_until = pygame.time.get_ticks() + 180
        if self.resistance <= 0:
            super().die()
