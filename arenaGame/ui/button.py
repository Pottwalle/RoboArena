import pygame

class Button():
    def __init__(self, rect, text, font, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback

        self.normal_color = (60, 60, 60)
        self.hover_color = (100, 100, 100)
        self.text_color = (255, 255, 255)

        self.hovered = False

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.callback()
    
    def update(self, dt):
        pass
    
    def draw(self, surface: pygame.Surface):
        color = self.hover_color if self.hovered else self.normal_color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)