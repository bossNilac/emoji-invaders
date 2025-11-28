import pygame
from pygame.sprite import Sprite

from config import ASSETS_DIR


class Bullet(Sprite):
    def __init__(self,Player):
        super(Bullet,self).__init__()
        self.image = (pygame.transform.scale
                  (pygame.image.load
                   (ASSETS_DIR + 'bullet.png').convert_alpha(), (10, 10)))
        self.rect = self.image.get_rect()
        self.player_rect = Player.rect
        self.start_x = Player.rect.midtop[0]
        self.start_y = Player.rect.midtop[1]
        self.y = self.start_y

    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def move(self):
        self.y -= 10
        self.rect.midtop = (self.start_x, self.y)

    def update(self):
        self.move()