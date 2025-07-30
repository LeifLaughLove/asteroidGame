import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from button import Button

#MENU SCREEN.. FIRST THING A PLAYER SEES WHEN THEY START THE GAME. HAS A PLAY BUTTON AND A LEADBERBOARD BUTTON.
#  ASTEEROIDS FLY IN THE BACKGROUND BECAUSE OF THE game.asteroid_update(dt, screen) CALL

class Menu():
    def __init__(self, screen, background):

        self.screen = screen
        self.background = background

        self.font = pygame.font.Font(None, 36)
        self.button_width, button_height = 200, 100
        self.menu_buttons_x = (SCREEN_WIDTH - self.button_width) // 2

        self.start_button_y = (SCREEN_HEIGHT - button_height) // 2
        self.start_button = Button("Start", (self.menu_buttons_x, self.start_button_y), (self.button_width, button_height), self.font, (100,128, 255), (255, 255, 255))

        self.leaderboard_button_y = self.start_button_y + 200
        self.leaderboard_button = Button("Leaderboard", (self.menu_buttons_x, self.leaderboard_button_y), (self.button_width, button_height), self.font, (100,128, 255), (255, 255, 255))


    
# -- MENU SCREEN - IS ACTIVE WHEN game_state = "menu" HAS IT'S OWN game.asteroid.update(dt, screen) call. THIS ALLOWS ASTEROIDS TO FLY IN MENU SCREEN--
    def menu_screen(self, screen, dt, game):
        screen.fill("black")
        screen.blit(self.background, (4,5))
        game.asteroid_update(dt, screen)

        self.start_button.draw(screen)
        self.leaderboard_button.draw(screen)

        changed_game_state = "menu"

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
                exit()
            if self.start_button.is_clicked(event):
                changed_game_state = "spaceship_select"
        return changed_game_state
    

            