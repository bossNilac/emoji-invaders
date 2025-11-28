import pygame

from config import ASSETS_DIR, MEASURE_UNIT_SIZE


class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,type_emoji):
        super().__init__()
        self.image = (pygame.transform.scale
                      (pygame.image.load
                       (ASSETS_DIR+type_emoji+'.png').convert_alpha(),
                       (MEASURE_UNIT_SIZE, MEASURE_UNIT_SIZE)))
        self.rect = self.image.get_rect(midtop= (x,y))

    def die(self):
        self.kill()

    # def move(self):
