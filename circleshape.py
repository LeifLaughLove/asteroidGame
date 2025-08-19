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

    def collision(self, other):
        
        if not hasattr(self, "mask") or not hasattr(other, "mask"):
            raise AttributeError("Both objects must have a .mask attribute for pixel-perfect collision.")
        if not hasattr(self, "rect") or not hasattr(other, "rect"):
            raise AttributeError("Both objects must have a .rect attribute for pixel-perfect collision.")

        offset = (int(other.rect.left - self.rect.left), int(other.rect.top - self.rect.top))
        return self.mask.overlap(other.mask, offset) is not None
        

    def draw(self, screen):
        pass

    def update(self, dt, score=None):
        pass