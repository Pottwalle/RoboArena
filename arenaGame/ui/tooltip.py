from ui.menu_font import MenuFont, Colors
import pygame
from .ui_element import UIElement

color_mapping = {
    "damage": Colors.DARK_RED.value,
    "attack_range": Colors.LIGHT_GOLD.value,
    "cooldown": Colors.YELLOW.value,
    "max_hp": Colors.DARK_GREEN.value,
    "defence": Colors.ORANGE.value
}

class Tooltip:
    def __init__(self, item, menu_font: MenuFont, small_font: MenuFont, scale: int):
        self.item = item
        self.menu_font = menu_font
        self.small_font = small_font
        self.scale = scale

    def create_tooltip_surface(self):
        stats_surfaces: list[pygame.Surface] = []
        if hasattr(self.item, "stats"):
            name_surface = self.menu_font.create_text_surface(f"[{self.item.type.upper()}]" + self.item.name)
            for stat, value in self.item.stats.items():
                sign = "+" if value >= 0 else ""
                text_surface = self.small_font.create_text_surface(f"{sign}{value} {self.format_name(stat)}")
                
                if stat in color_mapping:
                    self.small_font.recolor_image(text_surface, color_mapping[stat])
                stats_surfaces.append(text_surface)
        else:
            name_surface = self.menu_font.create_text_surface(self.item.name)
        
        max_len = max([surface.get_width() for surface in stats_surfaces] + [name_surface.get_width()])

        x_offset = 3
        y_offset = 3
        end_row = 1 if len(stats_surfaces) > 0 else 0
        tooltip_bg = pygame.Surface((max_len + x_offset*2, self.menu_font.text_height + 2*y_offset + (self.small_font.text_height + y_offset) * len(stats_surfaces) + end_row * y_offset))
        tooltip_bg.blit(name_surface, (x_offset, y_offset))

        for i, surface in enumerate(stats_surfaces):
            tooltip_bg.blit(surface, (x_offset, self.menu_font.text_height + 3*y_offset + i * (surface.get_height() + y_offset)))

        return UIElement.scale_surface(tooltip_bg, self.scale)
    
    def format_name(self, text: str) -> str:
        return text.replace("_", " ").title()