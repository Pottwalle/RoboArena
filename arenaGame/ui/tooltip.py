from item import Item, Equipment
from ui.menu_font import MenuFont
import pygame
from .ui_element import UIElement

class Tooltip:
    def __init__(self, item: Item, menu_font: MenuFont, small_font: MenuFont, scale: int):
        self.item = item
        self.menu_font = menu_font
        self.small_font = small_font
        self.scale = scale

    def create_tooltip_surface(self):
        stats_surfaces: list[pygame.Surface] = []
        if isinstance(self.item, Equipment):
            name_surface = self.menu_font.create_text_surface(f"[{self.item.type.upper()}]" + self.item.name)
            for stat, value in self.item.stats.items():
                sign = "+" if value >= 0 else "-"
                stats_surfaces.append(self.small_font.create_text_surface(f"{sign}{value} {self.format_name(stat)}"))
        else:
            name_surface = self.menu_font.create_text_surface(self.item.name)
        
        max_len = max([surface.get_width() for surface in stats_surfaces] + [name_surface.get_width()])

        x_offset = 3
        y_offset = 3
        tooltip_bg = pygame.Surface((max_len + x_offset*2, self.menu_font.text_height + 3*y_offset + (self.small_font.text_height + y_offset) * len(stats_surfaces)))
        tooltip_bg.blit(name_surface, (x_offset, y_offset))

        for i, surface in enumerate(stats_surfaces):
            tooltip_bg.blit(surface, (x_offset, self.menu_font.text_height + 3*y_offset + i * (surface.get_height() + y_offset)))

        return UIElement.scale_surface(tooltip_bg, self.scale)
    
    def format_name(self, text: str) -> str:
        return text.replace("_", " ").title()