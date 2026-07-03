import pygame
from ui.options_button import OptionsButton
from settings import settings
from ui.ui_element import UIElement
from ui.menu_font import MenuFont

class Setting():
    def __init__(self, coordinates: tuple[int, int], label: str, options: list[str], menu_font: MenuFont, callback, selected: int = 0):
        '''represents a setting in the settings menu, containing a label & options
        
        Args:
            coordinates: x and y position in unscaled
            label: string, the name of the setting
            options: list of strings, representing the different options
            menu_font: font the label is drawn with
            callback: callback function that changes the setting
            selected: defaultly selected option, default 0'''
        self.coordinates = coordinates
        self.scale = settings.UI_SCALE
        self.label = label
        self.label_texture_scaled = UIElement.scale_surface(menu_font.create_text_surface(label), self.scale)
        self.options = OptionsButton(
            (coordinates[0] + 208, coordinates[1], 80, 10), # base coord on unscaled scale + 208 makes the back of the button align with the end of the line
            options,
            menu_font,
            self.scale,
            callback,
            selected=selected
            )
    
    def handle_event(self, event):
        self.options.handle_event(event)
    
    def update(self, dt):
        pass
    
    def draw(self, surface: pygame.Surface):
        self.options.draw(surface)
        surface.blit(self.label_texture_scaled, (self.coordinates[0] * self.scale, self.coordinates[1] * self.scale))