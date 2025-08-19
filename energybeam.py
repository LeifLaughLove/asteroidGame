import pygame
from circleshape import CircleShape
from explosion import Explosion

class EnergyBeam(CircleShape):
    def __init__(self, start_pos, direction, beam_image, segment_length=32, max_segments=20, max_range_px=350):
        super().__init__(start_pos.x, start_pos.y, 8)
        self.start_pos = pygame.Vector2(start_pos)        
        self.position  = pygame.Vector2(start_pos)        
        self.direction = pygame.Vector2(direction).normalize()
        self.beam_image = beam_image
        self.segment_length = segment_length
        self.max_segments = max_segments
        self.max_range_px = max_range_px                  
        self.segments = []
        self.segment_ages = []
        self.segment_lifetime = 0.2
        
        self.segment_count = 0 

    def update(self, dt, *args, **kwargs):

        self.segment_ages = [age + dt for age in self.segment_ages]
        while self.segment_ages and self.segment_ages[0] > self.segment_lifetime:
            self.segments.pop(0)
            self.segment_ages.pop(0)

        if len(self.segments) == 1:
            print("FIRST")
            seg_pos = self.segments[0]
            if (seg_pos - self.position).length() > self.segment_length:
                print("SECOND")
                explosion = Explosion(seg_pos, 0)
                self.kill()


        tip_offset = len(self.segments) * (self.segment_length - 4)
        if tip_offset < self.max_range_px and len(self.segments) < self.max_segments and self.segment_count < self.max_segments:
            self.segment_count += 1
            pos = self.position + self.direction * tip_offset
            self.segments.append(pos)
            self.segment_ages.append(0.0)


    def draw(self, screen):
        angle = self.direction.angle_to(pygame.Vector2(0, -1))
        rotated_beam = pygame.transform.rotate(self.beam_image, angle)
        for pos in self.segments:
            rect = rotated_beam.get_rect(center=pos)
            screen.blit(rotated_beam, rect)