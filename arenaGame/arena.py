from tile import Tile

# map
MAP = [
    ["b", "b", "b", "b", "b", "b", "b", "b", "b", "b","b", "b"], 
    ["b", "n", "n", "n", "w", "n", "n", "n", "n", "n", "n", "b"],
    ["b", "n", "n", "n", "n", "n", "n", "n", "l", "l", "n", "b"],
    ["b","n", "n", "n", "n", "n", "n", "n", "l", "l", "n", "b"],
    ["b", "n", "j", "n", "n", "n", "n", "n", "n", "n", "n", "b"],
    ["b", "n", "j", "n", "n", "n", "n", "b", "n", "n", "n", "b"],
    ["b", "n", "j", "n", "n", "n", "n", "b", "n", "n", "n", "b"],
    ["b", "n", "n", "n", "n", "b", "n", "b", "n", "n", "n", "b"],
    ["b", "n", "n", "n", "n", "b", "b", "b", "n", "n", "n", "b"],
    ["b", "n", "n", "n", "n", "n", "n", "n", "n", "n", "n", "b"],
    ["b", "n", "n", "n", "n", "n", "n", "n", "n", "n", "n", "b"],
    ["b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"]
]

# type mapping
type_mapping = {
    "n": "dirt", 
    "w": "water", 
    "b": "brick", 
    "l": "lava",
    "j": "jungle"
    }

mapped_map = [[type_mapping[char] for char in row] for row in MAP]

class Arena:
    def __init__(self, screen_width, screen_height, tile_size):
        self.tile_size = tile_size
        self.screen_width = screen_width
        self.screen_height = screen_height

        # offset for map placement
        self.grid_width = len(MAP[0]) * self.tile_size
        self.grid_height = len(MAP) * self.tile_size
        self.offset_x = (self.screen_width - self.grid_width) // 2
        self.offset_y = (self.screen_height - self.grid_height) // 2

        self.grid = self.generate_grid(mapped_map)
    
    def generate_grid(self, mapped_map):
        grid = []

        for row_index, row in enumerate(MAP):
            tile_row = []
            for col_index, char in enumerate(row):
                tile_type = type_mapping[char]
                new_tile = Tile(
                    col_index, 
                    row_index, 
                    self.tile_size, 
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