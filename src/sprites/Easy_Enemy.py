import pygame

from sprites.EnemySprite import Enemy


class EasyEnemy(Enemy):
        def __init__(self, x, y):
            super().__init__(x, y, 'neutral')