import pygame
from .ui_manager import UIManager
from .texture_button import TextureButton
from settings import settings
from ui.menu_font import MenuFont
from ui.ui_element import UIElement

class EscMenu:
    def __init__(self, menu_font: MenuFont, on_resume, on_main_menu, on_settings):
        self.ui = UIManager()
        self.menu_font = menu_font
        self.scale = settings.UI_SCALE

        self.bg = pygame.transform.scale(pygame.image.load(settings.ASSET_DIR / "ui/settings_bg.png").convert(), (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        ui_elements = pygame.image.load(settings.ASSET_DIR / "ui/ui_elements.png")

        hover_texture = ui_elements.subsurface((0,54, 79, 18)).convert_alpha()

        paused_text = menu_font.create_text_surface("PAUSED").convert_alpha()
        self.scaled_paused_text = UIElement.scale_surface(paused_text, self.scale)

        self.ui.add(TextureButton((31, 31, 79, 18), "resume",
                                  None, hover_texture, self.scale, on_resume, text_button=True))

        self.ui.add(TextureButton((31, 75, 79, 18), "settings",
                                  None, hover_texture, self.scale, on_settings, text_button=True))
        
        self.ui.add(TextureButton((31, 119, 79, 18), "main menu",
                                  None, hover_texture, self.scale, on_main_menu, text_button=True))

    def handle_event(self, event):
        self.ui.handle_event(event)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.bg, (0, 0))
        self.menu_font.render_text_surface_unscaled(surface, self.scaled_paused_text, (50, 50))
        self.ui.draw(surface)

    def update(self, dt):
        pass
