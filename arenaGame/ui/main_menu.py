import pygame
from .ui_manager import UIManager
from .button import Button
from .texture_button import TextureButton
from settings import UI_SCALE, ASSET_DIR

class MainMenu():
    def __init__(self, set_playing):
        self.font = pygame.font.Font("freesansbold.ttf", 32)

        self.ui = UIManager()
        self.scale = UI_SCALE
        
        # load textures, size in pixels is 79 x 18 px
        self.ui_elements = pygame.image.load(ASSET_DIR / "ui/ui_elements.png")
        self.play_texture = self.ui_elements.subsurface((0, 18, 79, 18)).convert_alpha()
        self.hover_texture = self.ui_elements.subsurface((0, 54, 79, 18)).convert_alpha()

        self.ui.add(Button(
            (300, 250, 200, 60),
            "start",
            self.font,
            set_playing
            ))

        self.ui.add(TextureButton(
            (300, 500, 79 * self.scale, 18 * self.scale),
            "play",
            self.play_texture,
            self.hover_texture,
            self.scale,
            set_playing
            ))
    
    def handle_event(self, event):
        self.ui.handle_event(event)
    
    def update(self, dt):
        self.ui.update(dt)

    def draw(self, surface: pygame.Surface):
        surface.fill((20, 20, 30))
        self.ui.draw(surface)