
# SHIP.PY INITIIALIZES THE SHIP CLASS WHICH IS USED TO CREATE SHIPS IN THE GAME.

class Ship:
    def __init__(self, name, image_path, radius, speed, health, turn_speed, shoot_speed, shoot_cooldown, gun_damage, ship_sprite):
        
        self.name = name
        self.image_path = image_path
        self.radius = radius
        self.speed = speed
        self.health = health
        self.turn_speed = turn_speed
        self.shoot_speed = shoot_speed
        self.shoot_cooldown = shoot_cooldown
        self.gun1_damage = gun_damage
        self.sprite = ship_sprite if ship_sprite else None