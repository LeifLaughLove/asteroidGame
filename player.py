import pygame
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN, SCREEN_HEIGHT, SCREEN_WIDTH
from circleshape import CircleShape
from shot import Shot


class Player(CircleShape):
    containers = None
    def __init__(self, x, y):
        super().__init__(x,y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.lives = 3
        self.respawn_timer = 0


        # these variables are for speed, powerUp deals with the speed power up and only allows it to last
        # for 5 seconds
        self.speed = PLAYER_SPEED
        self.speed_power_up_status = False
        self.speed_power_up_timer = 0
        self.speed_power_up_duration = 5

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        return pygame.draw.polygon(screen,"white",self.triangle(),2)
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt, score=None):

        if self.speed_power_up_status:
            self.speed_power_up_timer += dt
            if self.speed_power_up_timer >= self.speed_power_up_duration:
                self.speed = PLAYER_SPEED
                self.speed_power_up_status = False
                self.speed_power_up_timer = 0
        self.timer -= dt
        keys = pygame.key.get_pressed()
        

#-------This section ensures that the player stays within the scren boundaries--------
        if self.position.x < 0:
            self.position.x = 0
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = SCREEN_WIDTH

        if self.position.y < 0:
            self.position.y = 0
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = SCREEN_HEIGHT
#   ----------------------------------------

        if keys[pygame.K_a] :
            Player.rotate(self, -dt)

        if keys[pygame.K_d] :
            Player.rotate(self, dt)
        
        if keys[pygame.K_w] :
            Player.move(self, dt)
        
        if keys[pygame.K_s] :
            Player.move(self, -dt)

        if keys[pygame.K_SPACE]:
            Player.shoot(self)
    

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * self.speed * dt

    def shoot(self):
        if self.timer < 0:
            shot = Shot(self.position.x, self.position.y, self.radius)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            self.timer = PLAYER_SHOOT_COOLDOWN
    

    #draw lives uses the players triangle function to draw the extra lives in the corner of the screen
    def draw_lives(self, screen):
        saved_pos = self.position
        saved_rot = self.rotation

        for i in range(self.lives):
            self.position = pygame.Vector2(20 + i * 30, 30)
            self.rotation = 180
            pygame.draw.polygon(screen, (255,255,255), self.triangle(), 1)
        
        self.position = saved_pos
        self.rotation = saved_rot

    #handles the player's lives to either respawn or end game
    def got_shot(self):

        if self.lives == 0:
            print("game OVer")
            return False
        
        elif self.lives > 0:
            print(self.lives)
            self.lives -= 1
            print(self.lives)
            return True
        
    def respawn(self, game_time, x, y):
        self.position = pygame.Vector2(x, y)
        self.rotation = 0
        self.speed = PLAYER_SPEED
        self.respawn_timer = game_time



    
def get_player_name(screen):
    font = pygame.font.Font(None, 48)
    name = ""
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        screen.fill((0, 0, 0))
        text = font.render(f"Enter Name: {name}", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))
        pygame.display.flip()

    return name