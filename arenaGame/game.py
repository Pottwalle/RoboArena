import pygame
import random
import math



pygame.init()

# Game Window
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
# set window title & icon
pygame.display.set_caption("Robot Arena")

#set Background
background = ("gray")


# Tile
class Tile:
    def __init__(self, x, y, size, type="normal"):
        self.rect = pygame.Rect(x * size, y * size, size, size)
        self.type = type
        self.color = (200, 200, 200)

        # Effekte basierend auf dem Typ zuweisen
        if self.type == "wasser":
            self.color = (0, 0, 255)
            self.speed_modifier = 0.5
        else:
            self.speed_modifier = 1.0

# draw
    def draw(self, col, row, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(
            offset_x + col * TILE_SIZE,
            offset_y + row * TILE_SIZE,
            self.rect.width,
            self.rect.height
        ))
        pygame.draw.rect(surface, (50, 50, 50), pygame.Rect(
            offset_x + col * TILE_SIZE,
            offset_y + row * TILE_SIZE,
            self.rect.width,
            self.rect.height
        ), 1)
# map
TILE_SIZE = 50
MAP = [
    ["n", "n", "n", "w", "n", "n", "n", "n", "n", "n"],
    ["n", "n", "n", "n", "n", "n", "n", "n", "n", "n"],
    ["n", "n", "n", "n", "n", "n", "n", "n", "n", "n"],
    ["n", "n", "n", "n", "n", "n", "n", "n", "n", "n"],
    ["n", "n", "n", "n", "n", "n", "n", "n", "n", "n"],
    ["n", "n", "n", "n", "n", "n", "n", "n", "n", "n"],
    ["n", "n", "n", "n", "n", "n", "n", "n", "n", "n"],
    ["n", "n", "n", "n", "n", "n", "n", "n", "n", "n"],
    ["n", "n", "n", "n", "n", "n", "n", "n", "n", "n"],
    ["n", "n", "n", "n", "n", "n", "n", "n", "n", "n"]
]

# type mapping
type_mapping = {"n" : "normal", "w": "wasser"}

# grid gen
grid = []
grid_width = len(MAP[0]) * TILE_SIZE
grid_height = len(MAP) * TILE_SIZE
for row_index, row in enumerate(MAP):
    tile_row = []
    for col_index, char in enumerate(row):
        tile_type = type_mapping[char]
        new_tile = Tile(col_index, row_index, TILE_SIZE, tile_type)
        tile_row.append(new_tile)
    grid.append(tile_row)

# offset for map placement
offset_x = (screen_width - grid_width) // 2
offset_y = (screen_height - grid_height) // 2

# basic game loop
running = True
while running:
    # draw Background
    screen.fill(background)
    #draw game map
    for row_index, tile_row in enumerate(grid):
        for col_index, tile in enumerate(tile_row):
            tile.draw(col_index, row_index, screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
# end game
            if event.key == pygame.K_SPACE:
                pygame.quit()

    pygame.display.update()