import pygame

class Damage:
    def __init__(self, movement):
        self.movement = movement

    def applyDamage(self, player, dt):
        tile = self.movement.getCurrentTile(player.position, player.r)
        if tile:
            self.applyTileDamage(player, tile, dt)


    
    def applyTileDamage(self, player, tile, dt):
        '''applies the damage of the tile with current position onto the player'''
        if tile.dmg > 0:
            player.hp -= tile.dmg * dt
            print(f"Player takes {tile.dmg} damage from {tile.tile_type} tile")
