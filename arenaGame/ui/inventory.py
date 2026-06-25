from .ui_manager import UIManager
import pygame
from settings import settings
from .ui_element import UIElement
from inventory_manager import InventoryManager
from item import Item

class Inventory():
    def __init__(self, inventory_manager: InventoryManager):
        
        self.inventory = inventory_manager
        self.ui = UIManager()
        self.scale = settings.UI_SCALE

        inventory_bg = pygame.image.load(settings.ASSET_DIR / "ui/inventory.png")
        self.inventory_bg = UIElement.scale_surface(inventory_bg, self.scale)


    def handle_event(self, event):
        self.ui.handle_event(event)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.inventory_bg, (175 * self.scale, 7 * self.scale))
        for r in range(self.inventory.rows):
            for c in range(self.inventory.cols):
                item: Item = self.inventory.get_item(r, c)
                if item:
                    # inventory item start is at 5x97
                    pos_x = 5 * settings.UI_SCALE + c * settings.UI_SCALE * settings.ITEM_SIZE
                    pos_y = 97 * settings.UI_SCALE + r * settings.UI_SCALE * settings.ITEM_SIZE
                    surface.blit(item.icon, (pos_x, pos_y))
        self.ui.draw(surface)

    def update(self, dt):
        pass