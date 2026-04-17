import random

import pygame

from config import ASSETS_DIR, MEASURE_UNIT_SIZE, SHOOTING_DELAY
import game_logic.score as score_module
from sprites import player
from sprites.Bullet import Bullet
from sprites.player import total_enemies_killed



def shoot_probability(i):
    if i == 4:
        return 1
    p_max = 0.1
    p = 2
    return p_max * (i / 3) ** p

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,type_emoji,importance,score=0):
        super().__init__()
        self.image = (pygame.transform.scale
                      (pygame.image.load
                       (ASSETS_DIR+type_emoji+'.png').convert_alpha(),
                       (MEASURE_UNIT_SIZE, MEASURE_UNIT_SIZE)))
        self.rect = self.image.get_rect(midtop= (x,y))
        self.going_left = False
        self.score = score
        self.shoot_tick = pygame.time.get_ticks()
        self.importance = importance
        self.shooter = random.random() < shoot_probability(importance)
        if self.shooter:
            self.bullet = None
        if self.shooter:
            print('object: ',self)

    def die(self):
        self.kill()
        if score_module.global_score is not None:
            score_module.global_score.update_score(self.score)
            player.total_enemies_killed += 1



    def shoot_back(self,p):
        now = pygame.time.get_ticks()
        if self.shooter and not self.bullet :
                if now - self.shoot_tick > SHOOTING_DELAY * self.importance / ((total_enemies_killed//2) +1):
                    self.bullet = Bullet(True,p,self.rect.x,self.rect.y)
                    self.shoot_tick = pygame.time.get_ticks()
                    return True
        return False

    def update_bullets(self,p,s):
        if self.shooter:
            self.shoot_back(p)
            if self.bullet:
                self.bullet.single_group.draw(s)
                if self.bullet.update():
                    self.bullet=None


    def drop_item(self):
        pass

