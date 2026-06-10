import pygame

class TextureButton():
    def __init__(self, rect: pygame.rect.Rect, text: str, texture: pygame.Surface, hover_texture: pygame.Surface, scale: int, callback):
        '''Represents an UI element button with a texture, with the typical handle_event, update, draw functions
        
        Args:
            rect: (x, y, w, h) pygame recct tuple, buttons area
            text: the text displayed on the button, but never seen
            texture: the normal state texture when the button is unhovered
            hover_texture: overlayed texture when the button hets hovered, should have alpha chanel
            scale: scale at which the textures get scaled
            callback: function triggered on pressing the button'''
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback

        self.texture = pygame.transform.scale(texture, (texture.get_width() * scale, texture.get_height() * scale))
        self.hover_texture = pygame.transform.scale(hover_texture, (hover_texture.get_width() * scale, hover_texture.get_height() * scale))

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
        surface.blit(self.texture, self.rect[:2])

        if self.hovered:
            surface.blit(self.hover_texture, self.rect[:2])