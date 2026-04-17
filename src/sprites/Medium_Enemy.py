from sprites.EnemySprite import Enemy


class MediumEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 'semi-angry',20)