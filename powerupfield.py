import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, POWER_UP_RADIUS
import random
from powerup import PowerUp

class PowerUpField(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(self.Containers)
        self.spawn_timer = 0.0

    def update(self, dt,score=None):
        self.spawn_timer += dt
        if self.spawn_timer > 10:
            self.spawn_timer = 0
            kind = "speed"
            self.spawn(kind)
    
    def spawn(self, kind=None):
        x = random.randint(0,SCREEN_WIDTH)
        y = random.randint(0,SCREEN_HEIGHT)
        PowerUp( x, y, POWER_UP_RADIUS, kind)