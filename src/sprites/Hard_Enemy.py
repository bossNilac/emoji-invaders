import pygame

from config import ASSETS_DIR
from sprites.EnemySprite import Enemy


class HardEnemy(Enemy):
    def __init__(self,x,y):
        super().__init__(x,y,'angry')