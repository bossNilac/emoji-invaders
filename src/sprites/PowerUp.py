import pygame

import config
from config import ASSETS_DIR

POWER_UP_IMAGES = {}


def get_power_up_image(power_up_type):
    if power_up_type not in POWER_UP_IMAGES:
        image_name = "fast.png" if power_up_type == "fast" else power_up_type + ".png"
        POWER_UP_IMAGES[power_up_type] = (pygame.transform.scale
                                          (pygame.image.load
                                           (ASSETS_DIR + image_name).convert_alpha(), (25, 25)))
    return POWER_UP_IMAGES[power_up_type]


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, power_up_type, player_group, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.power_up_type = power_up_type
        self.image = get_power_up_image(power_up_type)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.player_group = player_group
        self.x = x
        self.y = y

    def move(self):
        self.y += 3
        self.rect.midbottom = (self.x, self.y)

    def check_collision(self):
        if self.player_group is not None and self.player_group.sprite is not None:
            if self.rect.colliderect(self.player_group.sprite.rect):
                self.player_group.sprite.apply_power_up(self.power_up_type)
                self.kill()

    def update(self):
        self.move()
        self.check_collision()
        if self.y > config.HEIGHT:
            self.kill()
