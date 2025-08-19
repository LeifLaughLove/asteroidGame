import pygame
from assets import get_phazer_sprite
from button import Button
from ship import Ship
from constants import (
    PHAZER_RADIUS, PHAZER_SPEED, PHAZER_HEALTH, PHAZER_TURN_SPEED, PHAZER_SHOOT_SPEED,
    PHAZER_SHOOT_COOLDOWN, SCREEN_HEIGHT, SCREEN_WIDTH, PHAZER_GUN1_DAMAGE
)

# SHIPSELECT.PY handles the selection screen for choosing a ship

class ShipSelect:
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background

        # (Optional) example ship data (not strictly used here yet)
        self.phazer_def = Ship(
            "Phaser", "resources/phaser.png",
            PHAZER_RADIUS, PHAZER_SPEED, PHAZER_HEALTH, PHAZER_TURN_SPEED,
            PHAZER_SHOOT_SPEED, PHAZER_SHOOT_COOLDOWN,
            PHAZER_GUN1_DAMAGE, get_phazer_sprite()
        )

        # simple sprite animation setup
        self.tick_count = 0
        self.frame_speed = 3
        self.current_frame = 0

        self.phazer_frames = get_phazer_sprite()
        self.phazer_image = self.phazer_frames[self.current_frame]
        self.phazer_rect = self.phazer_image.get_rect(
            center=((SCREEN_WIDTH - PHAZER_RADIUS) // 3, int(SCREEN_HEIGHT / 2.25))
        )

        self.font = pygame.font.Font(None, 36)
        self.button_width, button_height = 100, 50
        self.select_buttons_y = int((SCREEN_HEIGHT - button_height) / 1.75)

        self.phazer_button_x = (SCREEN_WIDTH - self.button_width) // 3
        self.phazer_button = Button(
            "Select",
            (self.phazer_button_x, self.select_buttons_y),
            (self.button_width, button_height),
            self.font, (100, 128, 255), (255, 255, 255)
        )

    def draw(self):
        self.screen.blit(self.phazer_image, self.phazer_rect)

    def phazer_sprite_update(self):
        self.tick_count += 1
        if self.tick_count % self.frame_speed == 0:
            self.current_frame += 1
            if self.current_frame < len(self.phazer_frames):
                self.phazer_image = self.phazer_frames[self.current_frame]
            else:
                self.current_frame = 0
                self.phazer_image = self.phazer_frames[self.current_frame]
            # keep centered when frames differ in size
            self.phazer_rect = self.phazer_image.get_rect(center=self.phazer_rect.center)

    def selection_screen(self, screen, dt, game, events, to_game):
        """Draws the ship select screen.
        `events` is the list from pygame.event.get() (passed from main),
        `to_game` is a function that maps window coords -> game coords.
        """
        # backdrop & animated asteroids
        screen.fill("black")
        screen.blit(self.background, (4, 5))
        game.asteroid_update(dt, screen)

        # translucent popup
        popup_width = int(SCREEN_WIDTH * 0.6)
        popup_height = int(SCREEN_HEIGHT * 0.6)
        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        popup_surface.fill((0, 0, 0, 215))
        popup_rect = popup_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(popup_surface, popup_rect)

        # animate & draw
        self.phazer_sprite_update()
        self.draw()

        # buttons
        self.phazer_button.draw(screen)

        changed_game_state = "spaceship_select"

        # --- handle input (use game-space coords) ---
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                gx, gy = to_game(event.pos)  # convert from window -> 1920x1080 game coords
                if self.phazer_button.rect.collidepoint((gx, gy)):
                    # TODO: if you want to store the chosen ship, set it here on the Game or Player
                    # e.g., game.set_selected_ship(self.phazer_def)
                    game.reset()
                    changed_game_state = "playing"

        return changed_game_state