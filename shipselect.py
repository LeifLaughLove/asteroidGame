from assets import get_phazer_sprite
from button import Button
from ship import Ship
from constants import PLAYER_RADIUS, PLAYER_SPEED, PLAYER_TURN_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN, SCREEN_HEIGHT, SCREEN_WIDTH, PHAZER_GUN1_DAMAGE
import pygame

#SHIPSELECT.PY HANDLES THE SELECTION DECISION THAT THE USER MAKES WHEN CHOOSING A SHIP TO PLAY WITH

class ShipSelect():
    def __init__(self, screen, background):

        self.screen = screen
        self.background = background

        phazer = Ship("Phaser", "resources/phaser.png", PLAYER_RADIUS, PLAYER_SPEED, PLAYER_TURN_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN, PHAZER_GUN1_DAMAGE, get_phazer_sprite())


        self.tick_count = 0
        self.frame_speed = 3
        self.current_frame = 0

        self.phazer_frames = get_phazer_sprite()
        self.phazer_image = self.phazer_frames[self.current_frame]
        self.phazer_rect = self.phazer_image.get_rect(center=((SCREEN_WIDTH - PLAYER_RADIUS ) // 3, SCREEN_HEIGHT // 2.25))

        self.font = pygame.font.Font(None, 36)
        self.button_width, button_height = 100, 50
        self.select_buttons_y = (SCREEN_HEIGHT - button_height) // 1.75

        self.phazer_button_x = (SCREEN_WIDTH - self.button_width) // 3
        self.phazer_button = Button("Select", (self.phazer_button_x, self.select_buttons_y), (self.button_width, button_height), self.font, (100,128, 255), (255, 255, 255))


    def draw(self):
        self.screen.blit(self.phazer_image, self.phazer_rect)


    def phazer_sprite_update(self):
        self.tick_count += 1

        if self.tick_count % self.frame_speed == 0:
            self.current_frame += 1
            
            if self.current_frame < len(self.phazer_frames):
                self.phazer_image = self.phazer_frames[self.current_frame]
                self.phazer_rect = self.phazer_image.get_rect(center=self.phazer_rect.center)
            
            else:
                self.current_frame = 0
                self.phazer_image = self.phazer_frames[self.current_frame]
                self.phazer_rect = self.phazer_image.get_rect(center=self.phazer_rect.center)
    
    def selection_screen(self, screen, dt, game):

        popup_width = int(SCREEN_WIDTH * 0.6)
        popup_height = int(SCREEN_HEIGHT * 0.6)

        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        popup_surface.fill((0, 0, 0, 215))

        popup_rect = popup_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        screen.fill("black")
        screen.blit(self.background, (4,5))
        game.asteroid_update(dt, screen)
        screen.blit(popup_surface, popup_rect)
        self.phazer_sprite_update()

        self.phazer_button.draw(screen)

        self.draw()
        changed_game_state = "spaceship_select"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if self.phazer_button.is_clicked(event):
                changed_game_state = "playing"
                game.reset()

        return changed_game_state
