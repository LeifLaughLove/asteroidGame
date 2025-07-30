



import pygame
from button import Button
from constants import SCREEN_HEIGHT, SCREEN_WIDTH


class Shop():
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background



        self.popup_width = int(SCREEN_WIDTH * 0.6)
        self.popup_height = int(SCREEN_HEIGHT * 0.6)

        self.popup_surface = pygame.Surface((self.popup_width, self.popup_height), pygame.SRCALPHA)
        self.popup_surface.fill((0, 0, 0, 215))

        self.popup_rect = self.popup_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self.font = pygame.font.Font(None, 36)
        self.button_width, button_height = 100, 50
        self.select_buttons_y = (SCREEN_HEIGHT - button_height) // 1.75


        self.font = pygame.font.Font(None, 36)
        self.button_width, button_height = 100, 50

        self.continue_button_y = (SCREEN_HEIGHT - button_height) // 1.75
        self.continue_button_x = (SCREEN_WIDTH - self.button_width) // 3

        self.continue_button = Button("Continue", (self.continue_button_x, self.continue_button_y), (self.button_width, button_height), self.font, (100,128, 255), (255, 255, 255))

    def shop_screen(self):

        self.screen.fill("black")
        self.screen.blit(self.background, (4,5))

        self.screen.blit(self.popup_surface, self.popup_rect)

        self.continue_button.draw(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.continue_button.is_clicked(event):
                    return False    #Exits the shop screen when the continue button is clicked
        
        return True # Keeps the shop screen open until the continue Button is clicked