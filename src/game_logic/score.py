from pygame import font

import config

font = font.Font('freesansbold.ttf', 32)
text = font.render('GeeksForGeeks', True,config.WHITE)
textRect = text.get_rect()
textRect.center = (config.SCORE_X // 2, config.SCORE_Y // 2)
