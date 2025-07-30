import pygame
import assets

#EXPLOSION.PY ANIMATES EXPLOSIONS IN THE GAME, CURRENTLY JSUT THE SMALL EXPLOSION

class Explosion(pygame.sprite.Sprite):
    containers = ()
    def __init__(self, position, damage_amount):
        super().__init__()
        self.frames = assets.get_small_explosion_frames()
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=position)

        self.frame_speed = 5  # how many ticks between frames (lower = faster)
        self.tick_count = 0


        self.damage_amount = damage_amount
        self.font = pygame.font.Font(None, 24)  # or load your own font
        self.text_surface = self.font.render(f"-{damage_amount}", True, (255, 0, 0))
        self.text_position = [position[0], position[1] - 20]

        for group in self.containers:
            group.add(self)


    def update(self, dt, game_time, level=None):
        self.tick_count += 1
        
        if self.tick_count % self.frame_speed == 0:
            self.text_position[1] -= 1
            self.current_frame += 1

            if self.current_frame < len(self.frames):
                self.image = self.frames[self.current_frame]
                self.rect = self.image.get_rect(center=self.rect.center)

            else:
    
                self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, self.text_position)
