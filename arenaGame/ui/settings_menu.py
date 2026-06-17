from settings import ASSET_DIR, UI_SCALE, SCREEN_HEIGHT, SCREEN_WIDTH
from .ui_manager import UIManager
import pygame
from ui.menu_font import MenuFont
from .options_button import OptionsButton
from .texture_button import TextureButton

class SettingsMenu():
    def __init__(self, menu_font: MenuFont, on_back):
        self.ui = UIManager()
        self.scale = UI_SCALE
        self.menu_font = menu_font
        self.on_back = on_back

        self.ui_elements = pygame.image.load(ASSET_DIR / "ui/ui_elements.png")
        self.settings_bg = pygame.transform.scale(pygame.image.load(ASSET_DIR / "ui/settings_bg.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

        # coordinates of the buttons are measuren in the original UI site 320x180 and than scaled by factor in settings to fit the Window
        self.ui.add(OptionsButton(
            (31, 31, 79, 18),
            ["on", "off"],
            menu_font,
            self.scale,
            print
            ))
        
        # additional back button to return to the main menu
        back_tex = self.ui_elements.subsurface((0, 72, 79, 18)).convert_alpha()  
        back_hover_tex = self.ui_elements.subsurface((0, 90, 79, 18)).convert_alpha()
        self.ui.add(
            TextureButton(
                (31, 75, 79, 18),
                "back",
                back_tex,
                back_hover_tex,
                self.scale,
                self.on_back
            )
        )
    
    def handle_event(self, event):
        self.ui.handle_event(event)
    
    def update(self, dt):
        pass
    
    def draw(self, surface: pygame.Surface):
        surface.blit(self.settings_bg, (0, 0))
        self.menu_font.render_text(surface, "EDGE RENDERING", (50, 50), UI_SCALE)
        self.ui.draw(surface)