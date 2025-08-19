import pygame
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN, SCREEN_HEIGHT, SCREEN_WIDTH
from circleshape import CircleShape
from shot import Shot


# PLAYER.PY HANDLES THE PLAYER LOGIC AND MOVEMENT IN THE GAME ALSO UPDATES THE SHIP SPRITE WHEN THE SHIP IS MOVING 

class Player(CircleShape):
    containers = None
    def __init__(self, x, y, ship):


        super().__init__(x,y, PLAYER_RADIUS)

        self.image = pygame.image.load(ship.image_path).convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.rotation = 0
        self.timer = 0
        self.lives = 3
        self.respawn_timer = 0

        self.health = ship.health

        self.speed = ship.speed
        self.speed_power_up_status = False
        self.speed_power_up_timer = 0
        self.speed_power_up_duration = 5

        self.frames = ship.sprite
        self.frame_speed = 5
        self.tick_count = 0
        self.current_frame = 0

        self.gun1_damage = ship.gun1_damage

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0,-1).rotate(self.rotation)
        right = pygame.Vector2(0,-1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        #return pygame.draw.polygon(screen,"white",self.triangle(),2)
        rotated_image = pygame.transform.rotate(self.image, -self.rotation)
        rotated_rect = rotated_image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(rotated_image)
        self.rect = rotated_rect
        screen.blit(rotated_image, rotated_rect.topleft)
    
    def update(self, dt, score=None, level=None):
        self.rect.center = self.position
        if self.speed_power_up_status:
            self.speed_power_up_timer += dt
            if self.speed_power_up_timer >= self.speed_power_up_duration:
                self.speed = self.speed
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
            Player.shoot_gun_1(self)

        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
            spaceship_sprite_update(self, dt)
        else:
            self.image = self.original_image
            self.rect = self.image.get_rect(center=self.rect.center)
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        spaceship_sprite_update(self, dt)

    def move(self, dt):
        forward = pygame.Vector2(0,-1).rotate(self.rotation)
        self.position += forward * self.speed * dt
        spaceship_sprite_update(self, dt)

    def shoot_gun_1(self):
        if self.timer < 0:
            shot = Shot(self.position.x, self.position.y, self.radius, self.gun1_damage)
            shot.velocity = pygame.Vector2(0,-1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
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
    def got_hit(self, damage, game_state):

        self.health -= damage
        if self.health <= 0:
            game_state = "menu"
        
        return game_state
        
    def respawn(self, game_time, x, y):
        self.position = pygame.Vector2(x, y)
        self.rotation = 0
        self.speed = self.speed
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

def spaceship_sprite_update(self, dt):
    
    self.tick_count += 1

    if self.tick_count % self.frame_speed == 0:
        self.current_frame += 1
        
        if self.current_frame < len(self.frames):
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)
        
        else:
            self.current_frame = 0
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)