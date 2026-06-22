from player import Player

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
                pass #TODO implement item System
                
            self.applied = True