from circleshape import CircleShape
import pygame
from constants import PLAYER_SPEED

class PowerUp(CircleShape):
    def __init__(self,x,y,radius, kind="speed"):
        super(). __init__(x, y, radius)


        #this is the file lcation for the speed powerup----------------------------------------------
        self.speed_image = pygame.image.load("resources/Speed_UP.webp").convert_alpha()
        self.speed_image = pygame.transform.scale(self.speed_image,(self.radius * 2, self.radius *2))
        #--------------------------------------------------------------------------------------------


        #this is the file location for the extra life pwoerup----------------------------------------
        self.life_image = pygame.image.load("resources/Speed_UP.webp").convert_alpha()
        self.life_image = pygame.transform.scale(self.life_image,(self.radius * 2, self.radius *2))
        #--------------------------------------------------------------------------------------------


        self.kind = kind
        self.velocity = velocity = pygame.Vector2(0,0)
        self.speed_power_up_status = False

    def update(self, dt,score=None):
        self.position += self.velocity * dt
    
    def draw(self, screen):
        return screen.blit(self.speed_image, self.speed_image.get_rect(center=self.position))
    
        
    def activate_powerup(self, player):

        if self.kind == "speed" and player.speed_power_up_status == False:
            player.speed = player.speed *1.50
            player.speed_power_up_status = True

        if self.kind == "life":
            player.lives += 1
