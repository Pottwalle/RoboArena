import random
import pygame
from tile import Tile
import edges


class Arena:
    def __init__(self, screen_width, screen_height, tile_size, level_path):
        self.map = self.load_level(level_path)
        self.mapped_map = self.build_mapped_map(self.map)
        self.tile_size = tile_size
        self.screen_width = screen_width
        self.screen_height = screen_height

        # offset for map placement
        self.grid_width = len(self.map[0]) * self.tile_size
        self.grid_height = len(self.map) * self.tile_size
        self.offset_x = (self.screen_width - self.grid_width) // 2
        self.offset_y = (self.screen_height - self.grid_height) // 2

        self.grid = self.generate_grid(self.mapped_map)

    def load_level(self, level_path):
        with open(level_path, 'r') as file:
            lines = file.read().splitlines()
        return [list(line) for line in lines]

    def build_mapped_map(self, raw_map):
        type_mapping = {
            "n": "dirt",
            "w": "water",
            "b": "brick",
            "l": "lava",
            "j": "jungle"
        }
        return [[type_mapping[char] for char in row] for row in raw_map]

    def get_tile(self, map: list[list[str]], row: int, col: int):
        '''
        Returns the tile Type at the position row, col in the map with None if out of bounds
        Args:
            map (2D list): game map
            row: row index for the tile if in bounds
            col: collumn index for the tile if in bounds
        '''
        if 0 <= row < len(map) and 0 <= col < len(map[0]):
            return map[row][col]
        return None

    def generate_grid(self, mapped_map):
        grid = []

        for row_index, row in enumerate(mapped_map):
            tile_row = []
            for col_index, tile_type in enumerate(row):
                new_tile = Tile(
                    col_index,
                    row_index,
                    self.tile_size,
                    tile_type=tile_type,
                    offset_x=self.offset_x,
                    offset_y=self.offset_y,
                    tile_mask=edges.Tile_Mask(
                        top=self.get_tile(mapped_map, row_index - 1, col_index),
                        bottom=self.get_tile(mapped_map, row_index + 1, col_index),
                        left=self.get_tile(mapped_map, row_index, col_index - 1),
                        right=self.get_tile(mapped_map, row_index, col_index + 1),
                        tile_type=tile_type)
                )
                tile_row.append(new_tile)
            grid.append(tile_row)

        return grid

    # draw game map
    def draw_map(self, screen, camera):
        for row_index, tile_row in enumerate(self.grid):
            for col_index, tile in enumerate(tile_row):
                tile.draw(col_index, row_index, screen, self.offset_x - camera.x, self.offset_y - camera.y)

    def get_tiles_by_type(self, tile_type: str, exclude_solid: bool = True) -> list[Tile]:
        '''Gibt alle Tiles des angegebenen Typs zurück (z.B. "dirt", "water", ...).

        Args:
            tile_type: gewünschter Tile-Typ, siehe type_mapping in build_mapped_map
            exclude_solid: wenn True, werden solide Tiles (z.B. brick) ausgeschlossen,
                auch falls sie zufällig denselben tile_type-String hätten

        Returns:
            list[Tile]: alle passenden Tiles in der Arena (leer, falls keine gefunden wurden)
        '''
        matches = []
        for row in self.grid:
            for tile in row:
                if tile.tile_type == tile_type and not (exclude_solid and tile.solid):
                    matches.append(tile)
        return matches

    def get_random_tile_position(self, tile_type: str = "dirt", exclude_solid: bool = True):
        '''Wählt ein zufälliges Tile des angegebenen Typs aus und gibt dessen
        Weltmittelpunkt zurück, geeignet zum direkten Spawnen von Objekten
        (Player, Enemy, Interactables, ...).

        Args:
            tile_type: gewünschter Tile-Typ, Standard "dirt"
            exclude_solid: siehe get_tiles_by_type

        Returns:
            pygame.Vector2 mit der Mittelpunkt-Weltposition des gewählten Tiles,
            oder None, falls kein Tile dieses Typs existiert.
        '''
        candidates = self.get_tiles_by_type(tile_type, exclude_solid=exclude_solid)
        if not candidates:
            return None

        tile = random.choice(candidates)
        return pygame.Vector2(tile.rect.centerx, tile.rect.centery)

    def get_random_tile_positions(self, tile_type: str = "dirt", count: int = 1,
                                  exclude_solid: bool = True, unique: bool = True) -> list[pygame.Vector2]:
        '''Wie get_random_tile_position, liefert aber mehrere Positionen auf einmal.

        Args:
            tile_type: gewünschter Tile-Typ
            count: Anzahl gewünschter Positionen
            exclude_solid: siehe get_tiles_by_type
            unique: wenn True, wird jedes Tile höchstens einmal verwendet
                (sample ohne Zurücklegen); bei zu wenig Kandidaten werden
                entsprechend weniger Positionen zurückgegeben. Wenn False,
                können sich Positionen wiederholen (sample mit Zurücklegen).

        Returns:
            list[pygame.Vector2]: bis zu ``count`` Weltpositionen (leer, falls
            keine Tiles dieses Typs existieren)
        '''
        candidates = self.get_tiles_by_type(tile_type, exclude_solid=exclude_solid)
        if not candidates:
            return []

        if unique:
            chosen = random.sample(candidates, k=min(count, len(candidates)))
        else:
            chosen = random.choices(candidates, k=count)

        return [pygame.Vector2(tile.rect.centerx, tile.rect.centery) for tile in chosen]