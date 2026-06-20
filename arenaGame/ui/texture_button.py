import pygame
from ui.menu_font import MenuFont
from ui.ui_element import UIElement

class TextureButton():
    def __init__(self, rect: pygame.rect.Rect, text: str, texture: pygame.Surface, hover_texture: pygame.Surface, scale: int, callback, text_button = False):
        '''Represents an UI element button with a texture, with the typical handle_event, update, draw functions
        
        Args:
            rect: (x, y, w, h) pygame rect tuple, buttons area !!unscaled!!
            text: the text displayed on the button, but never seen
            texture: the normal state texture when the button is unhovered
            hover_texture: overlayed texture when the button hets hovered, should have alpha chanel
            scale: scale at which the textures get scaled
            callback: function triggered on pressing the button'''
        self.rect = pygame.Rect((rect[0] * scale, rect[1] * scale, rect[2] * scale, rect[3] * scale))
        self.text = text
        self.scale = scale
        self.text_button = text_button
        self.callback = callback

        if text_button:
            self.texture = UIElement.scale_surface(MenuFont.create_text_surface(MenuFont(), text).convert_alpha(), scale)
        else:
            self.texture = UIElement.scale_surface(texture, scale)
        self.hover_texture = UIElement.scale_surface(hover_texture, scale)

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
        if self.text_button:
            surface.blit(self.texture, (self.rect[0]  + (4 * self.scale), self.rect[1] + (4 * self.scale)))
        else:
            surface.blit(self.texture, self.rect[:2])

        if self.hovered:
            surface.blit(self.hover_texture, self.rect[:2])