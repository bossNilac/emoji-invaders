from sprites.EnemySprite import Enemy


class Ufo_Enemy(Enemy):
    def __init__(self,x,y):
        super().__init__(x,y,'ufo',4,50)