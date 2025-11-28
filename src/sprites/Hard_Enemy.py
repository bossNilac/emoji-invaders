import pygame

from config import ASSETS_DIR


class HardEnemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = (pygame.transform.scale
                      (pygame.image.load
                       (ASSETS_DIR+'angry.png').convert_alpha(),(50, 50)))
        self.rect = self.image.get_rect(midtop= (x,y))

    def die(self):
        self.kill()