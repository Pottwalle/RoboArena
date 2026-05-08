from tile import Tile

# map
MAP = [
    ["n", "n", "n", "w", "n", "n", "n", "n", "n", "n"],
    ["n", "n", "n", "n", "n", "n", "n", "l", "l", "n"],
    ["n", "n", "n", "n", "n", "n", "n", "l", "l", "n"],
    ["n", "j", "n", "n", "n", "n", "n", "n", "n", "n"],
    ["n", "j", "n", "n", "b", "n", "b", "n", "n", "n"],
    ["n", "j", "n", "n", "b", "n", "b", "n", "n", "n"],
    ["n", "n", "n", "n", "b", "n", "b", "n", "n", "n"],
    ["n", "n", "n", "n", "b", "b", "b", "n", "n", "n"],
    ["n", "n", "n", "n", "n", "n", "n", "n", "n", "n"],
    ["n", "n", "n", "n", "n", "n", "n", "n", "n", "n"]
]

# type mapping
type_mapping = {
    "n": "normal", 
    "w": "wasser", 
    "b": "brick", 
    "l": "lava",
    "j": "jungle"
    }

class Arena:
    def __init__(self, screen_width, screen_height, tile_size):
        self.tile_size = tile_size
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.grid = self.generate_grid()
        # offset for map placement
        self.grid_width = len(MAP[0]) * self.tile_size
        self.grid_height = len(MAP) * self.tile_size
        self.offset_x = (self.screen_width - self.grid_width) // 2
        self.offset_y = (self.screen_height - self.grid_height) // 2
    
    def generate_grid(self):
        grid = []

        for row_index, row in enumerate(MAP):
            tile_row = []
            for col_index, char in enumerate(row):
                tile_type = type_mapping[char]
                new_tile = Tile(col_index, row_index, self.tile_size, tile_type=tile_type)
                tile_row.append(new_tile)
            grid.append(tile_row)
        
        return grid
    
    #draw game map
    def draw_map(self, screen):
        for row_index, tile_row in enumerate(self.grid):
            for col_index, tile in enumerate(tile_row):
                tile.draw(col_index, row_index, screen, self.offset_x, self.offset_y)