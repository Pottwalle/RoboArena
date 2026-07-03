import pygame
from ui.ui_element import UIElement
from .ui_manager import UIManager
from .texture_button import TextureButton
from settings import settings
from ui.menu_font import MenuFont

class DeathMenu:
    ''' Death menu UI class'''
    def __init__(self, menu_font: MenuFont, on_main_menu):
        self.ui = UIManager()
        self.menu_font = menu_font
        self.scale = settings.UI_SCALE

        self.bg = pygame.transform.scale(pygame.image.load(settings.ASSET_DIR/"ui/settings_bg.png").convert(), (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        ui_elements = pygame.image.load(settings.ASSET_DIR/"ui/ui_elements.png")

        hover_texture = ui_elements.subsurface((0,54, 79, 18)).convert_alpha()
        normal_texture = ui_elements.subsurface((0,72, 79, 18)).convert_alpha()
        
        death_text = menu_font.create_text_surface("YOU DIED").convert_alpha()
        self.scaled_death_text = UIElement.scale_surface(death_text, self.scale)


        
        self.ui.add(TextureButton((31, 119, 79, 18), "main menu",
                                  normal_texture, hover_texture, self.scale, on_main_menu, text_button=True))
        
    def handle_event(self, event):
        self.ui.handle_event(event)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.bg, (0,0))
        self.menu_font.render_text_surface_unscaled(surface, self.scaled_death_text, (settings.SCREEN_WIDTH // 2 - self.scaled_death_text.get_width() // 2, 50))
        self.ui.draw(surface)

    def update(self, dt):
        self.ui.update(dt)