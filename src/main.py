import sys
from sys import exit

import pygame

import config
from config import FPS, HEIGHT, WIDTH, BLACK, WHITE
from game_logic.enemy_factory import update_enemies, render_enemies, on_game_reset
import game_logic.score as score_module
from game_logic.score import global_score
from sprites.player import Player

pygame.init()
score_module.global_score = score_module.Score(0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Emoji Invaders")
icon= pygame.image.load(config.ASSETS_DIR + 'rocket.png').convert()
BG= pygame.image.load(config.ASSETS_DIR + 'BG.png').convert()
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

font = pygame.font.Font("freesansbold.ttf", 32)
font2 = pygame.font.Font("freesansbold.ttf", 48)

def main_loop():
    player = pygame.sprite.GroupSingle()
    player.add(Player(screen))
    run_game = True
    while run_game:
        for event in pygame.event.get():
            if event.type == pygame.NOEVENT:
                run_game = False
                on_game_reset()
                score_module.global_score.reset()
                break
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        score_module.global_score.render_score(screen)
        render_enemies(screen)
        player.draw(screen)
        player.update()
        update_enemies(player,screen)
        try:
            pygame.display.update()
        except pygame.error:
            print("Game Over")
        clock.tick(FPS)

def start_menu(play_again = False):
        while True:
            screen.blit(BG, (0, 0))
            mouse = pygame.mouse.get_pos()

            play_button = pygame.Rect(330, 300, 140, 50)
            quit_button = pygame.Rect(330, 380, 140, 50)

            pygame.draw.rect(screen, WHITE, play_button)
            pygame.draw.rect(screen, WHITE, quit_button)

            play_text = font.render("Play Again" if play_again else "Play", True, BLACK)
            game_name = font2.render("Emoji Invaders", True, WHITE)
            quit_text = font.render("Quit", True, BLACK)
            screen.blit(play_text, (365, 305))
            screen.blit(quit_text, (365, 385))
            screen.blit(game_name, (235, 225))

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
