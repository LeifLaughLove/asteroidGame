from circleshape import CircleShape
import pygame
from constants import PLAYER_SPEED

#POWERUP.PY HANDLES THE POWERUPS IN THE GAME
#ACTIVATE POWER UP OCCURS WHEN A PLAYER HITS A POWER UP, THIS LOGIC IS IN GAME.PY HANDLE_COLLISIONS FUNCTION
# THERE IS CURRENTLY ONLY ONE POWER UP... THE SPEED POWER UP ...


class PowerUp(CircleShape):
    def __init__(self, x, y, radius, kind="speed"):
        super().__init__(x, y, radius)

        self.kind = kind
        self.velocity = pygame.Vector2(0, 0)
        self.speed_power_up_status = False

        if self.kind == "speed":
            sheet = pygame.image.load("resources/SpeedPowerUp.png").convert_alpha()
            frame_width = 32
            frame_height = 32

            positions = [
                (0, 0),
                (32, 0),
                (0, 32)
            ]

            self.frames = [
                sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
                for x, y in positions
            ]

            self.current_frame = 0
            self.frame_timer = 0
            self.frame_duration = 0.15

        elif self.kind == "life":
            self.image = pygame.image.load("resources/Speed_UP.webp").convert_alpha()
            self.frames = [pygame.transform.scale(self.image, (radius * 2, radius * 2))]
            self.current_frame = 0
            self.frame_timer = 0
            self.frame_duration = 0

        else:
            self.frames = [pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)]
            self.frames[0].fill((255, 0, 255, 128))
            self.current_frame = 0
            self.frame_timer = 0
            self.frame_duration = 0

        # Set initial image, rect, and mask
        self.image = pygame.transform.scale(
            self.frames[self.current_frame],
            (self.radius * 3, self.radius * 3)
        )
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt, score=None, level=None):
        self.position += self.velocity * dt

        if len(self.frames) > 1:
            self.frame_timer += dt
            if self.frame_timer >= self.frame_duration:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                # Update image, rect, and mask when frame changes
                self.image = pygame.transform.scale(
                    self.frames[self.current_frame],
                    (self.radius * 3, self.radius * 3)
                )
                self.rect = self.image.get_rect(center=self.position)
                self.mask = pygame.mask.from_surface(self.image)
            else:
                # Always keep rect and mask in sync with position
                self.rect.center = self.position
        else:
            self.rect.center = self.position

    def draw(self, screen):
        # No need to rescale here, just use self.image and self.rect
        return screen.blit(self.image, self.rect)

    def activate_powerup(self, player):
        if self.kind == "speed" and not player.speed_power_up_status:
            player.speed *= 1.5
            player.speed_power_up_status = True
        elif self.kind == "life":
            player.lives += 1
