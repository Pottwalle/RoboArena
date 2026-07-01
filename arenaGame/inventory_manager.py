from item import Item, Consumable, Equipment

class InventoryManager():
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.slots = [[None for _ in range(cols)] for _ in range(rows)]
        self.equipment_slots = {
            "helmet": None,
            "chestplate": None,
            "pants": None,
            "boots": None,
            "weapon": None,
            "ring": None,
            "amulet": None
        }

    
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
        '''swaps items at the given inventory slots'''
        item1 = self.get_item(r1, c1)
        self.slots[r1][c1] = self.slots[r2][c2]
        self.slots[r2][c2] = item1
    
    def equip_item(self, row, col) -> bool:
        '''equips the item at the given row, col position in the inventory'''
        item = self.slots[row][col]

        if isinstance(item, Equipment):
            type = item.type

            if type in self.equipment_slots:
                old_item = self.equipment_slots[type]

                self.equipment_slots[type] = item
                self.slots[row][col] = None

                if old_item:
                    self.slots[row][col] = old_item
                return True
        return False
    
    def unequip_item(self, slot_name: str) -> bool:
        '''unequips the item from the given equipment slot and returns it to the inventory'''
        item = self.equipment_slots[slot_name]

        if item:
            if self.add_item(item):
                self.equipment_slots[slot_name] = None
                return True
        return False
    
    def get_stat_bonus(self, stat: str) -> float:
        '''gets the stat bonus of the given stat from the whole equipment
        
        Args:
            stat: stat name in the format like max_hp, damage, ...'''
        total_bonus = 0
        for slot, item in self.equipment_slots.items():
            if item and stat in item.stats:
                total_bonus += item.stats[stat]
        return total_bonus