from .ui_manager import UIManager
import pygame
from settings import settings
from .ui_element import UIElement

class Inventory():
    def __init__(self, inventory):
        
        self.inventory = inventory
        self.ui = UIManager()
        self.scale = settings.UI_SCALE

        inventory_bg = pygame.image.load(settings.ASSET_DIR / "ui/inventory.png")
        self.inventory_bg = UIElement.scale_surface(inventory_bg, self.scale)


    def handle_event(self, event):
        self.ui.handle_event(event)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.inventory_bg, (175 * self.scale, 7 * self.scale))
        self.ui.draw(surface)

    def update(self, dt):
        pass