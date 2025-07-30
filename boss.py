
import pygame
from circleshape import CircleShape

# STILL WORKING ON THIS
# A BOSS FIGURE THAT CAN BE USED IN GAME

class Boss(CircleShape):
    containers = None
    def __init__(self, x, y):
        super().__init__(x, y, radius=None)
        self.image = pygame.image.load("resources/Boss1.png")
        self.name = "JEFFREY"
        self.heatlh = 1000
        self.position = pygame.Vector2(0, 0)

    def draw(self, screen):
       # image = pygame.image.load("resources/life.png")
       # position = pygame.Vector2(0, 0)
        screen.blit(self.image, self.position)

    def updatable(self):
        self.position.x = 0
        self.position.y = 0