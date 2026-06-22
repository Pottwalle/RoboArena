from settings import settings
from .ui_manager import UIManager
import pygame
from ui.menu_font import MenuFont
from .options_button import OptionsButton
from .texture_button import TextureButton

class SettingsMenu():
    def __init__(self, menu_font: MenuFont, on_back):
        self.ui = UIManager()
        self.scale = settings.UI_SCALE
        self.menu_font = menu_font
        
        self.on_back = on_back
        self.settings = settings
        
        ui_elements = pygame.image.load(settings.ASSET_DIR / "ui/ui_elements.png")
        self.settings_bg = pygame.transform.scale(pygame.image.load(settings.ASSET_DIR / "ui/settings_bg.png").convert(), (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        # coordinates of the buttons are measuren in the original UI site 320x180 and than scaled by factor in settings to fit the Window
        self.ui.add(OptionsButton(
            (220, 15, 79, 18),
            ["off", "on"],
            menu_font,
            self.scale,
            self.on_edge_rendering_changed,
            selected=1 if self.settings.EDGE_OVERLAYS else 0
            ))
        
        # additional back button to return to the main menu
        hover_texture = ui_elements.subsurface((0, 54, 79, 18)).convert_alpha()
        self.ui.add(
            TextureButton(
                (15, 147, 79, 18),
                "back",
                None,
                hover_texture,
                self.scale,
                self.on_back,
                text_button=True
            )
        )
    
    def handle_event(self, event):
        self.ui.handle_event(event)
    
    def update(self, dt):
        pass
    
    def draw(self, surface: pygame.Surface):
        surface.blit(self.settings_bg, (0, 0))
        self.menu_font.render_text(surface, "EDGE RENDERING", (15 * self.scale, 15 * self.scale), settings.UI_SCALE)
        self.ui.draw(surface)

###################### changes of the actual global settings ######################
    def on_edge_rendering_changed(self, value: str):
        """gets called on change of the options button"""
        self.settings.EDGE_OVERLAYS = (value == "on")
        print(f"Edge Rendering: {self.settings.EDGE_OVERLAYS}")
