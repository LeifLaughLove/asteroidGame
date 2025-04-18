import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS

class Shot(CircleShape):
    def __init__(self,x,y, radius):
        super().__init__(x,y, radius)

    def draw(self, screen):
        return pygame.draw.circle(screen, (255,255,255), self.position, SHOT_RADIUS, 1)
    
    def update(self, dt, score=None):
        self.position += self.velocity * dt