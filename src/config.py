import configparser
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets\\")
HIGHSCORE_FILE = os.path.join(ASSETS_DIR, "highscore.emoji")
SHOOTING_DELAY = 750
WIDTH = 800
HEIGHT = 600
MEASURE_UNIT_SPACE = 50
MEASURE_UNIT_SIZE = 40
FPS = 60
ENEMY_MOVE_SPEED=1
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCORE_X=700
SCORE_Y=50
TOTAL_ENEMIES_COUNT=60
UFO_SPAWN_CHANCE = 0.1


def read_high_score():
    parser = configparser.ConfigParser()
    if not os.path.exists(HIGHSCORE_FILE):
        return 0

    parser.read(HIGHSCORE_FILE)
    return parser.getint("score", "high_score", fallback=0)


def store_high_score(score):
    if score > read_high_score():
        parser = configparser.ConfigParser()
        parser["score"] = {"high_score": str(score)}
        with open(HIGHSCORE_FILE, "w") as high_score_file:
            parser.write(high_score_file)

