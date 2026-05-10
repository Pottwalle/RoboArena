import pygame


class Tile:
    def __init__(self, x, y, size, tile_type="normal", solid=False, dmg=0):
        self.x = x
        self.y = y
        self.size = size

        # Rechteck für Kollision & Position
        self.rect = pygame.Rect(x * size, y * size, size, size)

        # Tile-Eigenschaften
        self.tile_type = tile_type
        self.solid = solid
        self.dmg = dmg

        # Standardwerte
        self.color = (200, 200, 200)
        self.speed_modifier = 1.0

        # Typ-spezifische Eigenschaften
        if tile_type == "wasser":
            self.color = (0, 0, 255)
            self.speed_modifier = 0.5

        elif tile_type == "brick":
            self.color = (156, 102, 31)
            self.solid = True
            self.speed_modifier = 1.0

        elif tile_type == "lava":
            self.color = (255, 80, 0)
            self.speed_modifier = 0.7
            self.dmg = 1
        elif tile_type == "jungle":
            self.color = (144, 238, 144)

    def draw(self, col, row, surface, offset_x, offset_y):
        # Hauptfläche
        pygame.draw.rect(
            surface,
            self.color,
            pygame.Rect(
                offset_x + col * self.size,
                offset_y + row * self.size,
                self.size,
                self.size
            )
        )

        # Rahmen
        pygame.draw.rect(
            surface,
            (50, 50, 50),
            pygame.Rect(
                offset_x + col * self.size,
                offset_y + row * self.size,
                self.size,
                self.size
            ),
            1
        )
