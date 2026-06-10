from .ui_manager import UIManager
from settings import UI_SCALE, ASSET_DIR, SCREEN_HEIGHT, SCREEN_WIDTH
import pygame
from lifebar import Lifebar

class GameUI():
    def __init__(self, lifebar: Lifebar):
        self.ui = UIManager()
        self.scale = UI_SCALE

        # ui elements
        self.lifebar = lifebar

        self.ui_texture = pygame.transform.scale(pygame.image.load(ASSET_DIR / "ui/ui.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    def handle_event(self, event):
        self.ui.handle_event(event)
    
    def update(self, dt):
        self.ui.update(dt)

    def draw(self, surface: pygame.Surface):
        self.lifebar.draw(surface, 10 * self.scale, 8 * self.scale, 80 * self.scale, 5 * self.scale)
        surface.blit(self.ui_texture, (0, 0))
        self.ui.draw(surface)