import pygame

from config import ASSETS_DIR, MEASURE_UNIT_SIZE


class Shield(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = (pygame.transform.scale
                      (pygame.image.load
                       (ASSETS_DIR + 'shield.png').convert_alpha(),
                       (MEASURE_UNIT_SIZE, MEASURE_UNIT_SIZE)))
        self.rect = self.image.get_rect(midtop=(x, y))
