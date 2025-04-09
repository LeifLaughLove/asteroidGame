import pygame 
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, velocity=None):
        super().__init__(x, y, radius)
        if velocity is not None:
            self.velocity = velocity

    def draw(self, screen):
        return pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        rand_angle = random.randint(20, 50)
        vector1 = pygame.Vector2(1,0).rotate(rand_angle)
        vector2 = pygame.Vector2(1,0).rotate(-rand_angle)
        speed = self.velocity.length() or 100
        vector1 *= speed
        vector2 *= speed
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius, vector1*1.2)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius, vector2*1.2)