from ui.ui_element import UIElement
from settings import settings

class Item():
    def __init__(self, name, icon, description = ""):
        '''Represents an Item in the Game
        
        Args:
            name: item name
            icon: unscaled pygame surface
            description: item description'''
        self.name = name
        self.icon = UIElement.scale_surface(icon, settings.UI_SCALE)
        self.description = description

class Consumable(Item):
    def __init__(self, name, icon, description="", heal_amount = 0):
        super().__init__(name, icon, description)
        self.heal_amount = heal_amount

    def use(self, player) -> bool:
        '''uses the item in the inventory, and applied its effects on the player'''
        player.hp = min(player.max_hp, player.hp + self.heal_amount)
        return True