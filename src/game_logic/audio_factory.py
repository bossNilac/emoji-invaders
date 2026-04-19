from pygame import mixer

from config import ASSETS_DIR

_initialized = False
explosion = None
killed = None
music = None
shoot = None


def init_audio():
    global _initialized
    global explosion
    global killed
    global music
    global shoot

    if _initialized:
        return

    mixer.init()
    explosion = mixer.Sound(ASSETS_DIR + 'explosion.wav')
    killed = mixer.Sound(ASSETS_DIR + 'invaderkilled.wav')
    music = mixer.Sound(ASSETS_DIR + 'music.wav')
    shoot = mixer.Sound(ASSETS_DIR + 'shoot.wav')

    mixer.Channel(1).set_volume(0.5)
    mixer.Channel(2).set_volume(0.1)

    _initialized = True


def audio_loop():
    init_audio()
    if not mixer.Channel(0).get_busy():
        mixer.Channel(0).play(music, loops=-1)


def shooting_sound():
    init_audio()
    mixer.Channel(1).play(shoot)


def npc_die_sound():
    init_audio()
    mixer.Channel(2).play(killed)


def player_die_sound():
    init_audio()
    mixer.Channel(3).play(explosion)



