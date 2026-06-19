from tile import Tile
from edges import Tile_Mask

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
    
    def generate_grid(self, mapped_map):
        grid = []
        height = len(mapped_map)
        width = len(mapped_map[0])

        for row_index, row in enumerate(mapped_map):
            tile_row = []
            for col_index, tile_type in enumerate(row):
                top = mapped_map[row_index -1][col_index] if row_index > 0 else tile_type
                bottom = mapped_map[row_index +1][col_index] if row_index < height - 1 else tile_type
                left = mapped_map[row_index][col_index - 1] if col_index > 0 else tile_type
                right = mapped_map[row_index][col_index + 1] if col_index < width - 1 else tile_type

                tile_mask = Tile_Mask(top, bottom, left, right, tile_type) 

                new_tile = Tile(
                    col_index, 
                    row_index, 
                    self.tile_size, 
                    tile_mask = tile_mask,
                    tile_type=tile_type, 
                    offset_x=self.offset_x, 
                    offset_y=self.offset_y
                    )
                tile_row.append(new_tile)
            grid.append(tile_row)
        
        return grid
    
    #draw game map
    def draw_map(self, screen, camera):
        for row_index, tile_row in enumerate(self.grid):
            for col_index, tile in enumerate(tile_row):
                tile.draw(col_index, row_index, screen, self.offset_x - camera.x, self.offset_y - camera.y)