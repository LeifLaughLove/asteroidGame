import pygame

# CIRCLESHAPE.PY HANDLES THE BASIC CIRCLESHAPE FOR HITBOXES IN THE GAME

class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        
        if hasattr(self.__class__, "containers"):
            super().__init__(*self.__class__.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def collision(self, object):
        distance = self.position.distance_to(object.position)
        return distance < (self.radius + object.radius)
        

    def draw(self, screen):
        pass

    def update(self, dt, score=None):
        pass