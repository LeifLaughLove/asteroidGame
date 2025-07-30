import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS

class Shot(CircleShape):
    def __init__(self,x,y, radius, potential_damage):
        super().__init__(x,y, radius)

        self.potential_damage = potential_damage

    def draw(self, screen):
        return pygame.draw.circle(screen, (255,255,255), self.position, SHOT_RADIUS, 1)
    
    def update(self, dt, score=None, level=None):
        self.position += self.velocity * dt

    def position(self):
        return self.position