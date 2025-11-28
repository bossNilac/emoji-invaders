import pygame
from pygame.sprite import Sprite

import enemy_factory
from config import ASSETS_DIR


class Bullet(Sprite):
    def __init__(self,player):
        pygame.sprite.Sprite.__init__(self)
        self.image = (pygame.transform.scale
                  (pygame.image.load
                   (ASSETS_DIR + 'bullet.png').convert_alpha(), (10, 10)))
        self.rect = self.image.get_rect()
        self.player_rect = player.rect
        self.start_x = player.rect.midtop[0]
        self.start_y = player.rect.midtop[1]
        self.player = player
        self.y = self.start_y

    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def move(self):
        self.y -= 10
        self.rect.midtop = (self.start_x, self.y)

    def check_collision(self):
        hits = pygame.sprite.spritecollide(self, enemy_factory.ALL_ENEMIES, False)

        if hits:
            enemy = hits[0]
            enemy.die()
            self.kill()

    def update(self):
        self.move()
        self.check_collision()