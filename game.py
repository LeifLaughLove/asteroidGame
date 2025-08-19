import pygame
from assets import get_phazer_sprite
from explosion import Explosion
from player import Player, get_player_name
from asteroidfield import AsteroidField
from asteroid import Asteroid
from powerupfield import PowerUpField
from powerup import PowerUp
from enemyShipField import EnemyShipField
from enemyShip import EnemyShip
from ship import Ship
from shot import Shot
from energybeam import EnergyBeam
from constants import PHAZER_GUN1_DAMAGE, PHAZER_RADIUS, PHAZER_SHOOT_COOLDOWN, PHAZER_SHOOT_SPEED, PHAZER_SPEED, PHAZER_HEALTH, PHAZER_TURN_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT 
from leaderboard_client import get_leaderboard, post_score

# GAME.PY HANDLES THE GAME LOGIC AND UPDATES, SPRITE GROUPS, AND COLLSIONS
# IT IS THE MAIN GAME LOOP AND IS CALLED FROM THE MAIN.PY FILE


class Game():
    def __init__(self, screen):

        self.screen = screen
        self.game_time = 0
        self.score = 0

        # Initialize sprite groups
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()

        self.shots = pygame.sprite.Group()
        self.energybeams = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.enemyShips = pygame.sprite.Group()


        # Set up containers for different game entities
        Player.containers = (self.updatable, self.drawable)

        Asteroid.containers = (self.updatable, self.drawable, self.asteroids)
        AsteroidField.containers = (self.updatable,)

        Shot.containers = (self.updatable, self.drawable, self.shots)
        EnergyBeam.containers = (self.updatable, self.drawable, self.energybeams)
        Explosion.containers = (self.updatable, self.drawable)

        PowerUp.containers = (self.updatable, self.drawable, self.powerups)
        PowerUpField.containers = (self.updatable,)

        EnemyShip.containers = (self.updatable, self.drawable, self.enemyShips)
        EnemyShipField.containers = (self.updatable,)


        # DIFFERENT SHIPS
        #engineer = Ship("Engineer", "resources/engineerShip2.png", PLAYER_RADIUS, PLAYER_SPEED, PLAYER_TURN_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN, 10, None)
        phazer = Ship("Phaser", "resources/phaser.png", PHAZER_RADIUS, PHAZER_SPEED, PHAZER_HEALTH, PHAZER_TURN_SPEED, PHAZER_SHOOT_SPEED, PHAZER_SHOOT_COOLDOWN, PHAZER_GUN1_DAMAGE, get_phazer_sprite())   

        # Initialize game entities, ship is selected here
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, phazer)
        self.asteroidfield = AsteroidField()
        self.powerupfield = PowerUpField()
        self.enemyshipfield = EnemyShipField(self.player)
        self.top_scores = get_leaderboard()


    def update(self, dt, level):
        self.updatable.update(dt,self.score, level)
        self.game_time += dt

        # ASTEROID UPDATE - this function is only used in the menu. it is called in menu.py
    def asteroid_update(self, dt, screen):
        self.asteroidfield.menu_asteroids(dt)
        self.asteroids.update(dt, self.score)
        for asteroid in self.asteroids:
             asteroid.draw(screen)
    
    def draw(self):
        priority = {
            EnergyBeam: 0,     # draw first (under)
            Asteroid: 10,
            Shot: 15,
            PowerUp: 20,
            EnemyShip: 30,
            Player: 40,        # draw after beam (on top)
            Explosion: 50
        }
        for sprite in sorted(self.drawable.sprites(),
                            key=lambda s: priority.get(type(s), 100)):
            sprite.draw(self.screen)

    def clear_entities(self):
        for asteroid in self.asteroids:
             asteroid.kill()
        for enemy in self.enemyShips:
             enemy.kill()
        for powerup in self.powerups:
             powerup.kill()
        for shot in self.shots:
             shot.kill()

    def reset(self):
        self.clear_entities()
        #self.player.kill()
        self.score = 0         



    def handle_collisions(self, score, game_state):
        
        for asteroid in self.asteroids:
                if asteroid.state == "normal" and asteroid.collision(self.player):
                    asteroid.ship_collision()
                    #self.player.lives -= 1
                    game_state = self.player.got_hit(asteroid.damage, game_state)
                    if self.player.health <= 0:
                        #self.reset()
                        game_state = "menu"
                        #name = get_player_name(self.screen)
                        #post_score(name, self.score)
                        #top_scores = get_leaderboard()

        for asteroid in self.asteroids:
                for bullet in self.shots:
                    if asteroid.collision(bullet):
                        score += 100
                        explosion = Explosion(bullet.position, bullet.potential_damage)
                        bullet.kill()
                        asteroid.damaged(bullet.potential_damage)
                        break
        
        for powerup in self.powerups:
                for entity in self.drawable:
                    if isinstance(entity, Player):
                        if powerup.collision(entity):
                            powerup.kill()
                            powerup.activate_powerup(self.player)
                            print("power up achieved")

        for enemy in self.enemyShips:
            if enemy.collision(self.player):
                self.player.lives -= 1
                if self.player.lives < 0:
                    print("Game Over")
                    game_state = "menu"
                    name = get_player_name(self.screen)
                    post_score(name, self.score)
                else:
                    self.player.respawn(self.game_time, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            for bullet in self.shots:
                 if enemy.collision(bullet):
                      
                    explosion = Explosion(bullet.position, bullet.potential_damage)
                    bullet.kill()
                    enemy.got_hit(self.player.gun1_damage)
                      
        return score, game_state