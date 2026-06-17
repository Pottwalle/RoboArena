import pygame
from .ui_manager import UIManager
from .texture_button import TextureButton
from settings import ASSET_DIR, UI_SCALE, SCREEN_WIDTH, SCREEN_HEIGHT
from ui.menu_font import MenuFont

class EscMenu:
    def __init__(self, menu_font: MenuFont, on_resume, on_main_menu, on_settings):
        self.ui = UIManager()
        self.menu_font = menu_font
        self.scale = UI_SCALE

        self.bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg.set_alpha(180)
        self.bg.fill((0, 0, 0))

        ui_elements = pygame.image.load(ASSET_DIR / "ui/ui_elements.png")

        resume_tex = ui_elements.subsurface((0, 0, 79, 18)).convert_alpha()
        resume_hover = ui_elements.subsurface((0, 18, 79, 18)).convert_alpha()

        settings_tex = ui_elements.subsurface((0, 36, 79, 18)).convert_alpha()
        settings_hover = ui_elements.subsurface((0, 54, 79, 18)).convert_alpha()

        main_tex = ui_elements.subsurface((0, 72, 79, 18)).convert_alpha()
        main_hover = ui_elements.subsurface((0, 90, 79, 18)).convert_alpha()

        self.ui.add(TextureButton((31, 31, 79, 18), "resume",
                                  resume_tex, resume_hover, self.scale, on_resume))

        self.ui.add(TextureButton((31, 75, 79, 18), "settings",
                                  settings_tex, settings_hover, self.scale, on_settings))
        
        self.ui.add(TextureButton((31, 119, 79, 18), "main menu",
                                  main_tex, main_hover, self.scale, on_main_menu))

    def handle_event(self, event):
        self.ui.handle_event(event)

    def draw(self, surface):
        surface.blit(self.bg, (0, 0))
        self.menu_font.render_text(surface, "PAUSED", (50, 20), self.scale)
        self.ui.draw(surface)

    def update(self, dt):
        pass
