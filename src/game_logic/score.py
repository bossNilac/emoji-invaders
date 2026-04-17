
import config
import pygame


class Score:
    def __init__(self, score):
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.score = score
        self._render_text()

    def _render_text(self):
        self.text = self.font.render(f"Score: {self.score}", True, config.WHITE)
        self.text_rect = self.text.get_rect(center=(config.SCORE_X, config.SCORE_Y))

    def render_score(self, screen):
        screen.blit(self.text, self.text_rect)

    def update_score(self, score):
        self.score += score
        self._render_text()

    def reset(self):
        self.score = 0
        self._render_text()


global_score = None
