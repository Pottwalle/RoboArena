from item import Item, Consumable

class InventoryManager():
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.slots = [[None for _ in range(cols)] for _ in range(rows)]
    
    def add_item(self, item: Item) -> bool:
        '''adds an item to the first free slot of the Inventory and returns if the Placement was sucessful'''
        for r in range(self.rows):
            for c in range(self.cols):
                if self.slots[r][c] is None:
                    self.slots[r][c] = item
                    return True
        return False
    
    def use_item_at(self, row, col, player) -> bool:
        '''uses the Consumable at the Place in the inventory on the player returns true if sucessfull, else false'''
        item: Consumable = self.slots[row][col]
        if item and hasattr(item, "use"):
            if item.use(player):
                self.slots[row][col] = None
                return True
        return False

    def get_item(self, row, col):
        '''returns item at given position'''
        return self.slots[row][col]
    
    def remove_item(self, row, col) -> Item | None:
        '''retuns the Item at the given position and removes the item from there'''
        item = self.slots[row][col]
        self.slots[row][col] = None
        return item
    
    def swap_slots(self, r1, c1, r2, c2):
        item1 = self.get_item(r1, c1)
        self.slots[r1][c1] = self.slots[r2][c2]
        self.slots[r2][c2] = item1