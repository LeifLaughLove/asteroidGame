import pygame 
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_HEALTH
import random

# ASTEROID.PY IS EACH INSTANCE OF AN ASTEROID IN THE GAME
# IT IS A CIRCLESHAPE THAT CAN BE DAMAGED AND SPLIT INTO SMALLER ASTEROIDS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, velocity=None):
        super().__init__(x, y, radius)

        self.PNG = pygame.image.load("resources/rock.png").convert_alpha()
        self.visual_radius = self.radius 
        self.image = pygame.transform.scale(self.PNG,(self.visual_radius * 2, self.visual_radius *2))
        self.rect = self.image.get_rect(center=(x,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.asteroid_health = ASTEROID_HEALTH

        if velocity is not None:
            self.velocity = velocity

    def draw(self, screen):
        return screen.blit(self.image, self.image.get_rect(center=self.position))

    def update(self, dt, score=None, level=None):
        self.position += self.velocity * dt
    
    def damaged(self, potential_damage):
        self.asteroid_health -= potential_damage
        if self.asteroid_health == 0:
            self.split()
    
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