import pygame

class EnemyCounter:
    def __init__(self, scale, menu_font):
        self.scale = scale
        self.killed_enemies = 0
        self.kill_requirement = 50
        self.font = menu_font
        self.bg_color = (193, 154, 107)
        self.padding_x = 6*self.scale
        self.padding_y = 3* self.scale

    def update_count(self, value, kill_requirement):
        self.killed_enemies = value
        self.kill_requirement = kill_requirement

    def draw(self, surface: pygame.Surface):
        text = f"Slain:{self.killed_enemies}/{self.kill_requirement}"
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
        y = 3 * self.scale

        # Slain zeichnen
        surface.blit(scaled_surface, (x, y))
