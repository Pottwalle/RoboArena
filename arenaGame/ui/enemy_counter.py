import pygame

class EnemyCounter:
    def __init__(self, scale, menu_font):
        self.scale = scale
        self.killed_enemies = 0
        self.font = menu_font
        self.bg_color = (193, 154, 107)
        self.padding_x = 6*self.scale
        self.padding_y = 3* self.scale

    def update_count(self, value):
        self.killed_enemies = value

    def draw(self, surface: pygame.Surface):
        text = f"Slain: {self.killed_enemies}"
        text_surface = self.font.create_text_surface(text).convert_alpha()

        # Text skalieren
        scaled_surface = pygame.transform.scale(
            text_surface,
            (
                int(text_surface.get_width() * self.scale),
                int(text_surface.get_height() * self.scale)
            )
        )

        # Oben mittig positionieren
        screen_width = surface.get_width()
        x = screen_width // 2 - scaled_surface.get_width() // 2
        y = 10 * self.scale

        # Hintergrund-Rechteck berechnen
        bg_rect = pygame.Rect(
            x - self.padding_x,
            y - self.padding_y,
            scaled_surface.get_width() + self.padding_x * 2,
            scaled_surface.get_height() + self.padding_y * 2
        )

        # Hintergrund zeichnen
        pygame.draw.rect(surface, self.bg_color, bg_rect)

        # Slain zeichnen
        surface.blit(scaled_surface, (x, y))
