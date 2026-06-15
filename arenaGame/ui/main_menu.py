import pygame
from .ui_manager import UIManager
from .texture_button import TextureButton
from settings import UI_SCALE, ASSET_DIR, SCREEN_WIDTH, SCREEN_HEIGHT

class MainMenu():
    def __init__(self, set_playing, set_settings, set_quit):

        self.ui = UIManager()
        self.scale = UI_SCALE
        
        # load textures, size in pixels is 79 x 18 px
        self.ui_elements = pygame.image.load(ASSET_DIR / "ui/ui_elements.png")
        self.bg_texture = pygame.transform.scale(pygame.image.load(ASSET_DIR / "ui/main_menu_bg.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.play_texture = self.ui_elements.subsurface((0, 18, 79, 18)).convert_alpha()
        self.settings_texture = self.ui_elements.subsurface((0, 0, 79, 18)).convert_alpha()
        self.quit_texture = self.ui_elements.subsurface((0, 36, 79, 18)).convert_alpha()
        self.hover_texture = self.ui_elements.subsurface((0, 54, 79, 18)).convert_alpha()

        # coordinates of the buttons are measuren in the original UI site 320x180 and than scaled by factor in settings to fit the Window
        self.ui.add(TextureButton(
            (31, 31, 79, 18),
            "play",
            self.play_texture,
            self.hover_texture,
            self.scale,
            set_playing
            ))
        
        self.ui.add(TextureButton(
            (31, 53, 79, 18),
            "settings",
            self.settings_texture,
            self.hover_texture,
            self.scale,
            set_settings
            ))
        
        self.ui.add(TextureButton(
            (31, 75, 79, 18),
            "play",
            self.quit_texture,
            self.hover_texture,
            self.scale,
            set_quit
            ))
        
    
    def handle_event(self, event):
        self.ui.handle_event(event)
    
    def update(self, dt):
        self.ui.update(dt)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.bg_texture, (0, 0))
        self.ui.draw(surface)