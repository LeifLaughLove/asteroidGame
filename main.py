import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField

from shot import Shot

def main(): 
    print(f"Starting Asteroids! \nScreen width: {SCREEN_WIDTH} \nScreen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock()
    dt = 0
    
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2


    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    player = Player(x,y)

    Asteroid.containers = (updatable, drawable, asteroids)

    AsteroidField.containers = (updatable)
    asteroidfield = AsteroidField()

    Shot.containers= (updatable, drawable, shots)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        for entity in drawable:
            entity.draw(screen)
        for asteroid in asteroids:
            for entity in drawable:
                if isinstance(entity, Player):
                    if asteroid.collision(entity):
                        print("game OVer")
                        pygame.quit()
                        return
                
        for asteroid in asteroids:
            for bullet in shots:
                if asteroid.collision(bullet):
                    bullet.kill()
                    asteroid.split()
                    break

        pygame.display.flip()
        dt = clock.tick(60) / 1000
        

if __name__ == "__main__":
    main()