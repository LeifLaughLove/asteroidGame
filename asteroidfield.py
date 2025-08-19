import pygame
import random
from asteroid import Asteroid
from constants import *

# ASTEROIDFIELD.PY HANDLES THE SPAWNING OF ASTEROIDS IN TEH GAME 

class AsteroidField(pygame.sprite.Sprite):
    print("hello")
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.spawn_rate = ASTEROID_SPAWN_RATE

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius, velocity, 20)


    def update(self, dt, score, level):
        self.spawn_timer += dt

        #This section causes more asteroids to spawn depending on the player's score
        if score > 1000:
            self.spawn_rate = 0.075
        if score > 5000:
            self.spawn_rate = 0.2
        if score > 1000:
            self.spawn_rate = 0.3
        if self.spawn_timer > self.spawn_rate:
            self.spawn_timer = 0
        #---------------------------------------------------------------------------

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40,100)
            if score > 10 or level == 2:
                speed = random.randint(100, 200)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
            self.spawn_rate = 0.8

    def menu_asteroids(self, dt):
        self.spawn_timer += dt
        self.spawn_rate = 0.5

        if self.spawn_timer > self.spawn_rate:
            self.spawn_timer = 0

            edge = random.choice(self.edges)
            speed = random.randint(100,200)
        
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
