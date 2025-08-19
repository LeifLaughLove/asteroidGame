import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS

class Shot(CircleShape):
    def __init__(self,x,y, radius, potential_damage):
        super().__init__(x,y, radius)

        self.potential_damage = potential_damage
        self.image = pygame.image.load("resources/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (radius * 2, radius * 2))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def update(self, dt, score=None, level=None):
        self.position += self.velocity * dt
        self.rect.center = self.position

    def position(self):
        return self.position