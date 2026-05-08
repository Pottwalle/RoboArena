import pygame
import random
import math
from tile import Tile
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE



pygame.init()

# Game Window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# set window title & icon
pygame.display.set_caption("Robot Arena")

#set Background
background = ("gray")

# draw
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

# grid gen
grid = []
grid_width = len(MAP[0]) * TILE_SIZE
grid_height = len(MAP) * TILE_SIZE

# offset for map placement
offset_x = (SCREEN_WIDTH - grid_width) // 2
offset_y = (SCREEN_HEIGHT - grid_height) //2

for row_index, row in enumerate(MAP):
    tile_row = []
    for col_index, char in enumerate(row):
        tile_type = type_mapping[char]
        new_tile = Tile(col_index, row_index, TILE_SIZE, tile_type=tile_type)
        tile_row.append(new_tile)
    grid.append(tile_row)

# basic game loop
running = True
while running:
    # draw Background
    screen.fill(background)
    #draw game map
    for row_index, tile_row in enumerate(grid):
        for col_index, tile in enumerate(tile_row):
            tile.draw(col_index, row_index, screen, offset_x, offset_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
# end game
            if event.key == pygame.K_SPACE:
                pygame.quit()

    pygame.display.update()