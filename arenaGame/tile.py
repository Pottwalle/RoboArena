import pygame
from settings import settings
import edges

tileset = None
tiles = {}
tile_edges = {}

def load_tiles():
    global tileset, tiles, tile_edges
    tileset = pygame.image.load(settings.ASSET_DIR / 'tiles' / 'tileset.png')

    tiles = {
        "dirt": tileset.subsurface((0, 0, settings.TILE_SIZE, settings.TILE_SIZE)).convert(),
        "lava": tileset.subsurface((32, 0, settings.TILE_SIZE, settings.TILE_SIZE)).convert(),
        "water": tileset.subsurface((64, 0, settings.TILE_SIZE, settings.TILE_SIZE)).convert(),
        "brick": tileset.subsurface((96, 0, settings.TILE_SIZE, settings.TILE_SIZE)).convert(),
        "jungle": tileset.subsurface((192, 0, settings.TILE_SIZE, settings.TILE_SIZE)).convert()
    }

    tile_edge_keys = ["water_dirt", "lava_dirt", "dirt_jungle"]
    directions = ["n", "e", "s", "w", "nw", "ne", "sw", "se"]

    tile_edges = {key: {} for key in tile_edge_keys}

    def load_edgeset_from_line(starting_line: int, tile_size: int):
        '''loads the edges into the tile_edges directory, key are the tile_edge_keys items, each index stores a subdirectory containing all the pictures of the sub edges for each direction
        
        Args:
            starting_line: line at wich the first row of edge tiles start, pixels / tile_size
            tile_size: normal tile size from settings'''
        for line_index, tile_edge_key in enumerate(tile_edge_keys):
            for index, direction in enumerate(directions):
                tile_edges[tile_edge_key][direction] = tileset.subsurface((index * tile_size, (starting_line + line_index) * tile_size, tile_size, tile_size)).convert_alpha()
        
    load_edgeset_from_line(1, settings.TILE_SIZE)

class Tile:
    def __init__(self, x, y, size, tile_mask: edges.Tile_Mask, tile_type="normal", solid=False, dmg=0, offset_x=0, offset_y=0):
        self.x = x
        self.y = y
        self.size = size

        # Weltkoordinaten inkl. offset
        world_x = offset_x + x * size
        world_y = offset_y + y * size

        # Rechteck für Kollision & Position
        self.rect = pygame.Rect(
            world_x,
            world_y,
            size,
            size
        )

        # Tile-Eigenschaften
        self.tile_type = tile_type
        self.solid = solid
        self.dmg = dmg
        self.tile_mask = tile_mask

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
            self.dmg = 5
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
            draws the given Tile type image on the given surface and additionaly the tile edges if enabeled
        '''
        pos = (offset_x + col * self.size, offset_y + row * self.size)
        surface.blit(tiles[self.tile_type], pos)

        if settings.EDGE_OVERLAYS:
            for overlay_key, direction in self.tile_mask.mask:
                surface.blit(tile_edges[overlay_key][direction], pos)
