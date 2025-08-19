import pygame
from circleshape import CircleShape
from energybeam import EnergyBeam

HP_BACK    = (60, 24, 32)
HP_FILL    = (220, 70, 90)

TXT        = (220, 220, 230)

UI_BORDER  = (70, 70, 90)

def _draw_bar(surf, pos, size, value, max_value, back_col, fill_col, border_col=UI_BORDER):
    x, y = pos; w, h = size
    pygame.draw.rect(surf, back_col, (x, y, w, h))
    ratio = 0 if max_value <= 0 else max(0.0, min(1.0, value / max_value))
    fw = int(w * ratio)
    if fw > 0:
        pygame.draw.rect(surf, fill_col, (x, y, fw, h))
    pygame.draw.rect(surf, border_col, (x, y, w, h), 1)

def _label(surf, font, text, pos, color=TXT, center=False):
    img = font.render(text, True, color)
    r = img.get_rect()
    if center:
        r.center = pos
    else:
        r.topleft = pos
    surf.blit(img, r)

class EnemyShip(CircleShape):
    def __init__(self, x, y, name, image_path, radius, speed, health, turn_speed, shoot_speed, shoot_cooldown, gun_damage, ship_sprite, player):
        super().__init__(x, y, radius)

        self.name = name
        self.image_path = image_path
        self.radius = radius
        self.speed = speed
        self.max_health = health
        self.health = health
        self.turn_speed = turn_speed
        self.shoot_speed = shoot_speed
        self.shoot_cooldown = shoot_cooldown
        self.gun1_damage = gun_damage
        self.sprite = ship_sprite if ship_sprite else None

        
        self.font = pygame.font.Font(None, 24)

        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.rotation = 0
        self.player = player

        self.shoot_cooldown_timer = 0


        self.hp_size = (100, radius)
        self.x, self.y = x, y 
    
    def update(self, dt, score=None, level=None):
        # Calculate forward direction from rotation
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        # Move forward at self.speed
        self.rect.center = self.position

        self.shoot_cooldown_timer -= dt
        

        # Vector to player
        to_player = self.player.position - self.position
        if to_player.length() > 0:
            to_player = to_player.normalize()
            angle_to_player = forward.angle_to(to_player)
            if angle_to_player > 180:
                angle_to_player -= 360
            elif angle_to_player < -180:
                angle_to_player += 360
            # Rotate toward player
            if abs(angle_to_player) > 2:
                if angle_to_player > 0:
                    self.rotation += self.turn_speed * dt
                else:
                    self.rotation -= self.turn_speed * dt
                
            if abs(angle_to_player) < 20 and self.shoot_cooldown_timer <= 0:
                print("shooting")
                beam_image = pygame.image.load("resources/BEAM.png").convert_alpha()
                EnergyBeam(self.position, forward, beam_image)
                self.shoot_cooldown_timer = self.shoot_cooldown
            self.rotation %= 360
        self.rect.center = self.position



    def rotate(self, dt):
        self.rotation += self.turn_speed * dt



        

    
    def draw(self, screen):
        
        rotated_image = pygame.transform.rotate(self.image, -self.rotation)
        rotated_rect = rotated_image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(rotated_image)
        self.rect = rotated_rect
        
        screen.blit(rotated_image, self.rect)

        hp_x, hp_y = self.x, self.y - 100

        max_hp = getattr(self, "max_health", 100)
        hp     = getattr(self, "health", max_hp)

        _draw_bar(screen, (hp_x, hp_y), self.hp_size, hp, max_hp, HP_BACK, HP_FILL)

        _label(screen, self.font, f"{self.name}", (hp_x + 6, hp_y - 20))


    def got_hit(self, damage):

        self.health -= damage
        print(self.health)
        if self.health <= 0:
            self.kill()