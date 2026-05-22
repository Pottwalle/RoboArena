import pygame
import math


class Movement:
    def __init__(self, tilemap):
        self.tilemap = tilemap
    
    def move(self, pos, direction, speed, dt, radius):
        # get the speed modifier of current tile the player is on
        speed_mod = self.handleMoveSpeed(pos, radius)
        # get actual movement speed for current tile
        effective_speed = speed * speed_mod
        # new position based on current tile speed modifier
        new_pos = pos + direction * effective_speed * dt
        if self.handleCollision(new_pos, radius):
            return pos
        return new_pos
    
    def handleCollision(self, pos, radius):
        
        for row in self.tilemap:
            for tile in row:
                player_rect = pygame.Rect(
                pos.x - radius,
                pos.y - radius,
                radius * 2,
                radius * 2
)
                if tile.solid and tile.rect.colliderect(player_rect):
                    print("Kollision mit:", tile.rect)
                    return True
        return False
    
    def handleMoveSpeed(self, pos, radius):
        for row in self.tilemap:
            for tile in row:
                if tile.rect.collidepoint(pos.x, pos.y):
                    return tile.speed_modifier
        return 1.0