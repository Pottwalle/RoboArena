import pygame

class UIElement():
    
    @staticmethod
    def scale_surface(surface: pygame.Surface, scale: int) -> pygame.Surface:
        return pygame.transform.scale(surface, (surface.get_width() * scale, surface.get_height() * scale))