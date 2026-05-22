import pygame
import math


class Movement:
    def __init__(self, tilemap):
        self.tilemap = tilemap

    # moves the player based on the input direction, speed and delta time, 
    # with respect to the tile properties of the current tile the player is on.
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
    
    # checks if the player collides with any solid tile, returns true if so.
    def handleCollision(self, pos, radius):
        # checks for each tile in the tilemap, if the player is currently on it.
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
    
    # checks whether the tile the player is currently on has a speed modifier.
    def handleMoveSpeed(self, pos, radius):
        # checks for each tile in the tilemap, if the player is currently on it
        for row in self.tilemap:
            for tile in row:
                if tile.rect.collidepoint(pos.x, pos.y):
                    # returns speed modifier for the current tile, the player is on.
                    return tile.speed_modifier
        return 1.0