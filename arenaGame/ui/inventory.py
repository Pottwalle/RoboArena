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

        self.dragged_item: Item = None
        self.dragged_slot = None
        self.context_menu = None

        inventory_bg = pygame.image.load(settings.ASSET_DIR / "ui/inventory.png")
        self.inventory_bg = UIElement.scale_surface(inventory_bg, self.scale)
        self.last_gamestate_bg = None


    def handle_event(self, event: pygame.event.Event):
        self.ui.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN: # drag and drop logic
            if event.button == 1:
                slot = self._get_slot_at_pos(event.pos)
                if slot:
                    r, c = slot
                    self.dragged_item = self.inventory.get_item(r, c)
                    self.dragged_slot = (r, c)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragged_item:
                new_slot = self._get_slot_at_pos(event.pos)
                if new_slot:
                    nr, nc = new_slot
                    self.inventory.swap_slots(self.dragged_slot[0], self.dragged_slot[1], nr, nc)
                self.dragged_item = None
                self.dragged_slot = None


    def draw(self, surface: pygame.Surface):
        surface.blit(self.last_gamestate_bg, (0, 0))
        surface.blit(self.inventory_bg, (175 * self.scale, 7 * self.scale))
        for r in range(self.inventory.rows):
            for c in range(self.inventory.cols):
                item: Item = self.inventory.get_item(r, c)
                if item:
                    # inventory item start is at 5x97
                    pos_x = (175 + 5) * settings.UI_SCALE + c * settings.UI_SCALE * settings.ITEM_SIZE
                    pos_y = (7 + 97) * settings.UI_SCALE + r * settings.UI_SCALE * settings.ITEM_SIZE
                    surface.blit(item.icon, (pos_x, pos_y))
        self.ui.draw(surface)

        if self.dragged_item:
            surface.blit(self.dragged_item.icon, pygame.mouse.get_pos())

    def update(self, dt):
        pass
    
    def _get_slot_at_pos(self, mouse_pos):
        mx, my = mouse_pos

        start_x = (175 + 5) * self.scale
        start_y = (7 + 97) * self.scale
        slot_size = self.scale * settings.ITEM_SIZE

        if my < start_y or mx < start_x:
            return None
        
        col = int((mx - start_x) / slot_size)
        row = int((my - start_y) / slot_size)

        if 0 <= row < self.inventory.rows and 0 <= col < self.inventory.cols:
            return (row, col)
        
        return None