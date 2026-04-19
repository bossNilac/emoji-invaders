import pygame
from pygame.sprite import Sprite, GroupSingle

import config
from game_logic import enemy_factory
from config import ASSETS_DIR


class Bullet(Sprite):
    def __init__(self,is_from_enemy,player,x= None,y = None):
        pygame.sprite.Sprite.__init__(self)
        self.image = (pygame.transform.scale
                  (pygame.image.load
                   (ASSETS_DIR + 'bullet.png').convert_alpha(), (10, 10)))
        self.player = player
        self.rect = self.image.get_rect()
        self.is_from_enemy = is_from_enemy
        if not is_from_enemy:
            self.player_rect = player.rect
            self.start_x = player.rect.midtop[0]
            self.start_y = player.rect.midtop[1]
            self.y = self.start_y
        else:
            self.y = y
            self.start_x = x
            self.single_group = pygame.sprite.GroupSingle()
            self.single_group.add(self)


    def move(self):
        if not self.is_from_enemy:
            self.y -= 10
            self.rect.midtop = (self.start_x, self.y)
        else:
            self.y += 10
            self.rect.midbottom = (self.start_x, self.y)

    def check_collision(self):
        shield_hits = pygame.sprite.spritecollide(self, enemy_factory.ALL_SHIELDS, False)
        if shield_hits:
            shield = shield_hits[0]
            shield.kill()
            self.kill()
            return

        hits = pygame.sprite.spritecollide(self, enemy_factory.ALL_ENEMIES, False)
        if hits and not self.is_from_enemy:
            enemy = hits[0]
            enemy.die()
            self.kill()

        if isinstance(self.player,GroupSingle) and self.player.sprite is not None:
            if self.is_from_enemy & self.rect.colliderect(self.player.sprite.rect):
                if hasattr(self.player.sprite, "die"):
                    self.player.sprite.die()
                else:
                    self.player.sprite.kill()
                    pygame.event.post(pygame.event.Event(pygame.NOEVENT))

    def update(self):
        self.move()
        self.check_collision()
        if self.y > config.HEIGHT or self.y < 0:
            del self
            return True
        return False
