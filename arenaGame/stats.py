
class Stats:
    def __init__(self, base_stats: dict, inventory_manager=None):
        self.base_stats = base_stats
        self.inventory_manager = inventory_manager

        self.modifiers = {} # saves modifiers in format {"speed": [50, 20]}
        self.hp = base_stats.get("max_hp", 100)

    def get(self, stat: str) -> float:
        '''gets the total value of the stat, from base + equipment + modifiers'''
        base = self.base_stats.get(stat, 0)

        equipment_bonus = 0
        if self.inventory_manager and hasattr(self.inventory_manager, "get_stat_bonus"):
            equipment_bonus = self.inventory_manager.get_stat_bonus(stat)
        
        modifiers = sum(self.modifiers.get(stat, []))
        return base + equipment_bonus + modifiers
    
    def add_modifier(self, stat: str, amount: float):
        '''adds an temporary stat modifier (buff / debuff) to a stat like -50 speed'''
        if stat not in self.modifiers:
            self.modifiers[stat] = []
        
        self.modifiers[stat].append(amount)
    
    def remove_modifier(self, stat: str, amount: float):
        '''removes an active modifier, opf the given stat, if it exists'''
        if stat in self.modifiers and amount in self.modifiers[stat]:
            self.modifiers[stat].remove(amount)
    
    def heal(self, amount: float):
        self.hp = max(0, min(self.get("max_hp"), self.hp + amount))