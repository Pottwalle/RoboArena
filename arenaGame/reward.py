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
            for item in self.items:
                if isinstance(item, Item):
                    player.inventory.add_item(item)
                    # TODO drop item if inv is full
                
            self.applied = True