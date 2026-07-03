from player import Player
from item import Item

class Reward():
    def __init__(self, xp = 0, items = None):
        self.xp = xp
        self.items = items if items else []
        self.applied = False
    
    def apply_to_player(self, player: Player):
        if not self.applied:
            if self.xp > 0:
                player.add_xp(self.xp)

            failed_items = []
            for item in self.items:
                if isinstance(item, Item):
                    if player.inventory.add_item(item):
                        print(f"Player received reward: {item.name}")
                    else:
                        failed_items.append(item)
                
            self.applied = len(failed_items) == 0
            if not self.applied:
                self.xp = 0
                self.items = failed_items