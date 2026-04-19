import sys

import pygame

pygame.init()

import config
import game_logic.score as score_module
from config import FPS, HEIGHT, WIDTH, BLACK, WHITE, read_high_score, store_high_score
from game_logic.audio_factory import audio_loop
from game_logic.enemy_factory import update_enemies, render_enemies, on_game_reset
from sprites.player import Player

score_module.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Emoji Invaders")
icon= pygame.image.load(config.ASSETS_DIR + 'rocket.png').convert()
BG= pygame.image.load(config.ASSETS_DIR + 'BG.png').convert()
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

font = pygame.font.Font("freesansbold.ttf", 32)
font2 = pygame.font.Font("freesansbold.ttf", 48)

play_again_text = 'Play'

def main_loop():
    player = pygame.sprite.GroupSingle()
    player.add(Player(screen))
    global play_again_text
    run_game = True
    while run_game:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.NOEVENT:
                run_game = False
                on_game_reset()
                play_again_text = 'Play Again'
                store_high_score(score_module.get_score())
                score_module.reset()
                break
            if keys[pygame.K_ESCAPE]:
                run_game = False
                play_again_text = 'Continue'
                break
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(BG, (0, 0))
        audio_loop()
        score_module.render_score(screen)
        render_enemies(screen)
        player.draw(screen)
        player.update()
        update_enemies(player,screen)
        try:
            pygame.display.update()
        except pygame.error:
            pass
        clock.tick(FPS)

def start_menu():
        while True:
            screen.blit(BG, (0, 0))
            mouse = pygame.mouse.get_pos()

            play_text = font.render(play_again_text, True, BLACK)
            game_name = font2.render("Emoji Invaders", True, WHITE)
            quit_text = font.render("Quit", True, BLACK)
            high_score_text = font.render(f"High Score: {read_high_score()}", True, WHITE)

            play_button_width = max(140, play_text.get_width() + 40)
            play_button = pygame.Rect(0, 300, play_button_width, 50)
            play_button.centerx = WIDTH // 2

            quit_button = pygame.Rect(0, 380, 140, 50)
            quit_button.centerx = WIDTH // 2

            pygame.draw.rect(screen, WHITE, play_button)
            pygame.draw.rect(screen, WHITE, quit_button)

            screen.blit(play_text, play_text.get_rect(center=play_button.center))
            screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))
            screen.blit(game_name, game_name.get_rect(center=(WIDTH // 2, 250)))
            screen.blit(high_score_text, high_score_text.get_rect(center=(WIDTH // 2, 475)))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(mouse):
                        main_loop()
                    if quit_button.collidepoint(mouse):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()

start_menu()
