from .ui_manager import UIManager
import pygame
from settings import settings
from .ui_element import UIElement
from inventory_manager import InventoryManager
from item import Item

inventory_x = 175
inventory_y = 7
slots_offset = {
    "helmet": (85, 10),
    "chestplate": (85, 32),
    "pants": (85, 54),
    "boots": (85, 76),
    "weapon": (63, 21),
    "ring": (107, 43),
    "amulet": (107, 21),
}

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
                    if isinstance(slot, str):
                        self.dragged_item = self.inventory.equipment_slots[slot]
                        self.dragged_slot = slot
                    else:
                        r, c = slot
                        self.dragged_item = self.inventory.get_item(r, c)
                        self.dragged_slot = (r, c)
            if event.button == 3:
                slot = self._get_slot_at_pos(event.pos)
                if slot:
                    if isinstance(slot, str):
                        item = self.inventory.equipment_slots[slot]
                        if item:
                            self.inventory.unequip_item(slot)
                    else:
                        r, c = slot
                        item = self.inventory.get_item(r, c)
                        if item:
                            self.inventory.equip_item(r, c)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragged_item:
                new_slot = self._get_slot_at_pos(event.pos)
                if new_slot:
                    if isinstance(new_slot, str):
                        if not isinstance(self.dragged_slot, str):
                            self.inventory.equip_item(self.dragged_slot[0], self.dragged_slot[1])
                    else:
                        nr, nc = new_slot
                        self.inventory.swap_slots(self.dragged_slot, nr, nc)
                self.dragged_item = None
                self.dragged_slot = None


    def draw(self, surface: pygame.Surface):
        surface.blit(self.last_gamestate_bg, (0, 0))
        surface.blit(self.inventory_bg, (inventory_x * self.scale, inventory_y * self.scale))
        for r in range(self.inventory.rows):
            for c in range(self.inventory.cols):
                item: Item = self.inventory.get_item(r, c)
                if item:
                    # inventory item start is at 5x97
                    pos_x = (inventory_x + 5) * self.scale + c * self.scale * settings.ITEM_SIZE
                    pos_y = (inventory_y + 97) * self.scale + r * self.scale * settings.ITEM_SIZE
                    surface.blit(item.icon, (pos_x, pos_y))
        
        for slot in self.inventory.equipment_slots:
            item = self.inventory.equipment_slots[slot]
            if item:
                offset = slots_offset[slot]
                surface.blit(item.icon, ((inventory_x + offset[0]) * self.scale, (inventory_y + offset[1]) * self.scale))
        self.ui.draw(surface)

        if self.dragged_item:
            surface.blit(self.dragged_item.icon, pygame.mouse.get_pos())

    def update(self, dt):
        pass
    
    def _get_slot_at_pos(self, mouse_pos) -> str | tuple[int, int]:
        mx, my = mouse_pos

        start_x = (175 + 5) * self.scale
        start_y = (7 + 97) * self.scale
        slot_size = self.scale * settings.ITEM_SIZE
        
        col = int((mx - start_x) / slot_size)
        row = int((my - start_y) / slot_size)

        if 0 <= row < self.inventory.rows and 0 <= col < self.inventory.cols:
            return (row, col)
        
        for slot in slots_offset: # look if the mouse collides with an equipment slot
            offset = slots_offset[slot]
            if (inventory_x + offset[0]) * self.scale <= mx <= (inventory_x + offset[0] + settings.ITEM_SIZE) * self.scale and (inventory_y + offset[1]) * self.scale <= my <= (inventory_y + offset[1] + settings.ITEM_SIZE) * self.scale:
                return slot
        return None