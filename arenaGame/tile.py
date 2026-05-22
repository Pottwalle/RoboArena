import pygame
from settings import ASSET_DIR, TILE_SIZE, EDGE_OVERLAYS

tileset = None
tiles = None
tile_edges = None

def load_tiles():
    global tileset, tiles, tile_edges
    tileset = pygame.image.load(ASSET_DIR / 'tiles' / 'tileset.png')

    tiles = {
        "dirt": tileset.subsurface((0, 0, TILE_SIZE, TILE_SIZE)).convert(),
        "lava": tileset.subsurface((32, 0, TILE_SIZE, TILE_SIZE)).convert(),
        "water": tileset.subsurface((64, 0, TILE_SIZE, TILE_SIZE)).convert(),
        "brick": tileset.subsurface((96, 0, TILE_SIZE, TILE_SIZE)).convert(),
        "jungle": tileset.subsurface((192, 0, TILE_SIZE, TILE_SIZE)).convert()
    }

    tile_edges = {

    }

class Tile_Mask:
    def __init__(self, top, bottom, left, right, tile_type):
        '''
        stores the 
        Args:
            top, bottom, left, right, tile_type: tile types according to type_mapping in arena.py
        '''
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.tile_type = tile_type
    
    def generate_mask(self):
        if self.tile_type == "water":
            if self.tile_type != self.top:
                pass

class Tile:
    def __init__(self, x, y, size, mask: Tile_Mask, tile_type="normal", solid=False, dmg=0):
        self.x = x
        self.y = y
        self.size = size

        # Maske um übergänge zeichnen zu können
        self.mask = mask

        # Rechteck für Kollision & Position
        self.rect = pygame.Rect(x * size, y * size, size, size)

        # Tile-Eigenschaften
        self.tile_type = tile_type
        self.solid = solid
        self.dmg = dmg

        # Standardwerte
        self.speed_modifier = 1.0

        # Typ-spezifische Eigenschaften
        if tile_type == "wasser":
            self.speed_modifier = 0.5

        elif tile_type == "brick":
            self.solid = True
            self.speed_modifier = 1.0

        elif tile_type == "lava":
            self.speed_modifier = 0.7
            self.dmg = 1
        
        elif tile_type == "jungle":
            self.speed_modifier = 0.8

    def draw(self, col: int, row: int, surface: pygame.Surface, offset_x, offset_y):
        '''
        Draws the given tile image from the tile_type on the given surface at the given position

        Args:
            col: collumn in the given Map to draw the tiles from
            row: row in the given Map to draw the tiles from
            surface (pygame.Surface): Surface on which the tile should be drawn at
            offset_x: camera offset, tile gets offset by the given value on the given axis
            offset_y: camera offset, tile gets offset by the given value on the given axis
        Sideeffects:
            reads the global EDGE_OVERLAYS variable and draws the Edges if True else no edges are shown
            draws the given Tile type image on the given surface
        '''
        pos = (offset_x + col * self.size, offset_y + row * self.size)
        surface.blit(tiles[self.tile_type], pos)

        if EDGE_OVERLAYS:
            if self.mask.top == "water":
                surface.blit(tile_edges[0], pos) #TODO