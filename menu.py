import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from button import Button

class Menu:
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background
        self.font = pygame.font.Font(None, 36)
        self.button_width, button_height = 200, 100
        self.menu_buttons_x = (SCREEN_WIDTH - self.button_width) // 2

        self.start_button_y = (SCREEN_HEIGHT - button_height) // 2
        self.start_button = Button(
            "Start",
            (self.menu_buttons_x, self.start_button_y),
            (self.button_width, button_height),
            self.font, (100,128,255), (255,255,255)
        )

        self.leaderboard_button_y = self.start_button_y + 200
        self.leaderboard_button = Button(
            "Leaderboard",
            (self.menu_buttons_x, self.leaderboard_button_y),
            (self.button_width, button_height),
            self.font, (100,128,255), (255,255,255)
        )

    def menu_screen(self, screen, dt, game, events, to_game):
        screen.fill("black")
        screen.blit(self.background, (4, 5))
        game.asteroid_update(dt, screen)

        self.start_button.draw(screen)
        self.leaderboard_button.draw(screen)

        changed_game_state = "menu"

        for event in events:
            # Left click?
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                gx, gy = to_game(event.pos)   # <-- convert window -> game coords
                if self.start_button.rect.collidepoint((gx, gy)):
                    changed_game_state = "spaceship_select"
                elif self.leaderboard_button.rect.collidepoint((gx, gy)):
                    changed_game_state = "leaderboard"  # or whatever your state key is

        return changed_game_state


            