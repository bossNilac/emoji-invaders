
import config
import pygame


font = None
_global_score = 0
text_rect = None
text = None

def init():
    global font
    font = pygame.font.Font("freesansbold.ttf", 32)
    _render_text()

def _render_text():
    global text, text_rect, font
    if font is None:
        return
    text = font.render(f"Score: {_global_score}", True, config.WHITE)
    text_rect = text.get_rect(center=(config.SCORE_X, config.SCORE_Y))

def render_score(screen):
    if text is not None and text_rect is not None:
        screen.blit(text, text_rect)

def get_score():
    return _global_score

def update_score(score):
    global _global_score
    _global_score += score
    _render_text()

def reset():
    global _global_score
    _global_score = 0
    _render_text()
