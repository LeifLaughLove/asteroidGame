import pygame
from game import Game
from menu import Menu
from shipselect import ShipSelect
from levelmanager import LevelManager
from shop import Shop
pygame.font.init()
from boss import Boss
from constants import *
from player import Player, get_player_name
from asteroid import Asteroid
from asteroidfield import AsteroidField
from powerupfield import PowerUpField
from powerup import PowerUp
from button import Button
from shot import Shot
from leaderboard import draw_leaderboard_panel, save_score
from leaderboard_client import post_score, get_leaderboard
import time

    #                                              ---- My Asteroid Game ----
    #                         still being updated, so far there's a main menu with one button, 
    #                         when the start button is clicked the game begins with your spaceship 
    #                         in the center of the screen. Asteroids start coming in at a slower pace. 
    #                         Every 10 seconds a speed power up spawns in. The game gets progressively 
    #                         more difficult in 3 stages, casuing more asteroids to spawn at a higher rate.


def main(): 
    print(f"Starting Asteroids! \nScreen width: {SCREEN_WIDTH} \nScreen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    background = pygame.image.load("resources/background.png").convert()


    #This is all for my button, I only have 1 right now and it's the start button when the application is launched
    font = pygame.font.Font(None, 36)
    
    #--------------------------------------------------------------------------------------------------------------------------------------

    # The players score is set to 0, allowing running to be True
    #     and game_state set to menu i include it in my loop so 
    #     the asteroids can move across too
    score = 0
    game_state = "menu"
    open_shop = False
    running = True
    
    #clock 
    clock = pygame.time.Clock()
    dt = 0
    game_time = 0
    
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    game = Game(screen)
    menu = Menu(screen, background)
    shipselect = ShipSelect(screen, background)
    levelmanager = LevelManager()
    shop = Shop(screen, background)
    #--------------------------------------


    try:
        top_scores = get_leaderboard()
    except Exception as e:
        print(f"Warning: Could not connect to leaderboard server — {e}")
        top_scores = []



        #-----MAIN LOOP----#
    while running:
#                              -:MAIN MENU:-
        if game_state =="menu":
            game_state = menu.menu_screen(screen, dt, game)

        elif game_state == "spaceship_select":
            game_state = shipselect.selection_screen(screen, dt, game)

        elif open_shop:
            open_shop = shop.shop_screen()

        elif game_state == "playing":
#                              -:GAME PLAYING:-

            screen.fill("black")
            screen.blit(background, (4,5))

            # FOR STATEMENT ALLOWS PLAYER INPUTS TO BE RECEIVED
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            current_level, open_shop = levelmanager.update(dt, game)

            game.update(dt, current_level)
            game.draw()


            score_text = font.render(f"{score}", True, (255,255,255))
            text_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, 20))
            screen.blit(score_text, text_rect)
            
            score, game_state = game.handle_collisions(score, game_state)

            game_time += dt

        pygame.display.flip()
        dt = clock.tick(60) / 1000
        
 #         -:GAME OVER:-       

if __name__ == "__main__":
    main()