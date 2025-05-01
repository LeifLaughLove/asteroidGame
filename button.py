import pygame


class Button:
    def __init__(self, text, pos, size, font, bg_color, text_color):
        self.rect = pygame.Rect(pos, size)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.text_surf = font.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)


    def draw(self, screen):
        print("draw")
        pygame.draw.rect(screen, self.bg_color, self.rect)
        screen.blit(self.text_surf,self.text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
            
