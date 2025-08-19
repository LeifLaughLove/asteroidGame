import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SOROB_RADIUS, SOROB_TURN_SPEED, SOROB_SPEED, SOROB_HEALTH, SOROB_SHOT_RADIUS, SOROB_SHOOT_SPEED, SOROB_SHOOT_SPEED, SOROB_SHOOT_COOLDOWN, SOROB_GUN1_DAMAGE 
import random
from enemyShip import EnemyShip

class EnemyShipField(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__(self.containers)
        self.spawn_timer = 0.0
        self.player = player


    def update(self, dt, score=None, level=None):
        self.spawn_timer += dt
        if self.spawn_timer > 10:
            self.spawn_timer = 0
            kind = "sorob"
            self.spawn(kind)

    def spawn(self, kind=None):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        if kind == "sorob":
            EnemyShip(x, y, "Sorob", "resources/sorob.png", SOROB_RADIUS, SOROB_SPEED, SOROB_HEALTH, SOROB_TURN_SPEED, SOROB_SHOOT_SPEED, SOROB_SHOOT_COOLDOWN, SOROB_GUN1_DAMAGE, None, self.player)