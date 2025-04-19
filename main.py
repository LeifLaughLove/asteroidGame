import pygame
pygame.font.init()
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from powerupfield import PowerUpField
from powerup import PowerUp
from button import Button
from shot import Shot


def main(): 
    print(f"Starting Asteroids! \nScreen width: {SCREEN_WIDTH} \nScreen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    background = pygame.image.load("resources/background.png").convert()


    #This is all for my button, I only have 1 right now and it's the start button when t he application is launched
    font = pygame.font.Font(None, 36)
    button_width, button_height = 200, 100
    start_button_x = (SCREEN_WIDTH - button_width) // 2
    start_button_y = (SCREEN_HEIGHT - button_height) // 2
    start_button = Button("Start", (start_button_x, start_button_y), (button_width, button_height), font, (100,128, 255), (255, 255, 255))


    score = 0
    game_state = "menu"
    running = True
    
    clock = pygame.time.Clock()
    dt = 0
    game_time = 0
    
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2


    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    player = Player(x,y)

    Asteroid.containers = (updatable, drawable, asteroids)

    AsteroidField.containers = (updatable)
    asteroidfield = AsteroidField()

    Shot.containers = (updatable, drawable, shots)

    PowerUp.containers = (updatable, drawable, powerups)
    
    PowerUpField.Containers = (updatable)
    powerupfield = PowerUpField()

    

    

        #-----MAIN LOOP----#

    while running:
        # -----------This first section of the code is a main menu. when game_state is returned as "playing" the game starts-------------

        # This for loop allows the player to exit the game 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if game_state == "menu" and start_button.is_clicked(event):
                game_state = "playing"
                for asteroid in asteroids:
                    asteroid.kill()
        if game_state =="menu":
            screen.fill("black")
            screen.blit(background, (4,5))
            asteroidfield.update(dt, score, game_state)  # manually update the field

            for asteroid in asteroids:
                asteroid.update(dt, score)   # update only asteroids
                asteroid.draw(screen)        # draw them before the button

            start_button.draw(screen)
            pygame.display.flip()
            dt = clock.tick(60) / 1000

            
        elif game_state == "playing":

        # --------------- This is the end of the menu section, below this line the game is started -------------------------------

            screen.fill("black")
            screen.blit(background, (4,5))
            updatable.update(dt, score)
            for entity in drawable:
                entity.draw(screen)

            # This section handles the score, score goes up as the player kills asteroids
            # score goes up the same every time a player hits an asteroid.
            # score is changed in the for loop where asteroids are handled when shot

            score_text = font.render(f"{score}", True, (255,255,255))
            text_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, 20))
            screen.blit(score_text, text_rect)
            

                #Checks if asteroid makes contact with the player
            for asteroid in asteroids:
                for entity in drawable:
                    if isinstance(entity, Player):
                        if asteroid.collision(entity) and (game_time - player.respawn_timer) > 2:
                            player.lives -= 1
                            if player.lives < 0:
                                print("Game Over")
                                running = False
                            else:
                                player.respawn( game_time, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)


                #Checks if a bulelt makes contact with an asteroid 
            for asteroid in asteroids:
                for bullet in shots:
                    if asteroid.collision(bullet):
                        score += 100
                        bullet.kill()
                        asteroid.split()
                        break


                #Checks if a player has come into contact with a power up
            for powerup in powerups:
                for entity in drawable:
                    if isinstance(entity, Player):
                        if powerup.collision(entity):
                            powerup.kill()
                            powerup.activate_powerup(player)
                            print("power up achieved")
            
            player.draw_lives(screen)

            pygame.display.flip()
            dt = clock.tick(60) / 1000
            game_time += dt
        
        

if __name__ == "__main__":
    main()