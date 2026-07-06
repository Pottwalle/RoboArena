import pygame
from settings import settings
from enum import Enum

class Colors(Enum):
    '''Colors used throughout the project in RGB values'''
    DARK_GOLD = (121, 95, 19) # dark base color of the font (basecolor small_font)
    GOLD = (156, 119, 11) # base light color of the normal font
    DARK_RED = (189, 5, 10)
    DARK_GREEN = (134, 149, 61)
    LIGHT_GOLD = (190, 145, 12)
    YELLOW = (251, 200, 83)
    ORANGE = (243, 174, 72)

class MenuFont():
    def __init__(self, filename: str, text_size=6, text_height=10, text_spacing=2, icon_size=10, icon_spacing=4):
        self.filename = filename

        self.icon_size = icon_size
        self.icon_spacing = icon_spacing
        self.text_size = text_size
        self.text_spacing = text_spacing
        self.space_width = self.text_size + self.text_spacing
        self.text_height = text_height

        self.letters = {}
        self.icons = {}
        self._load_font()
        self._load_icons()

    def _load_font(self):
        '''loads the letters upper alphabet & 0 - 9 into the self.letters dict'''
        # letters are 6x10px with 2px margin 
        letters_sheet = pygame.image.load(settings.ASSET_DIR / f"font/{self.filename}.png").convert_alpha()
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.+-/:"
        for index, letter in enumerate(alphabet):
            self.letters[letter] = letters_sheet.subsurface(0 + index * (self.text_size + self.text_spacing), 0, self.text_size, self.text_height)
    
    def _load_icons(self):
        '''loads the Symbols 10x10px into the self.icons dict'''
        symbols_sheet = pygame.image.load(settings.ASSET_DIR / "font/icons.png").convert_alpha()
        symbol_keys = ["[GRAPHICS]", "[AUDIO]", "[SETTINGS]", "[PLAY]", "[QUIT]", "[SAVE]", "[DISK]", "[LOAD]", "[BACK]", "[X]", "[COIN]", "[HELMET]", "[CHESTPLATE]", "[PANTS]", "[BOOTS]", "[WEAPON]", "[RING]", "[AMULET]"]
        for index, key in enumerate(symbol_keys):
            self.icons[key] = symbols_sheet.subsurface(0 + index * self.icon_size, 0, self.icon_size, self.icon_size) # letters are 10x10px with 0px margin
    
    def create_text_surface(self, text: str) -> pygame.Surface:
        '''creates a pygame Surface containg the Text written in the menu font, charsize 6x10 with 2px margin, Symbolsize 10x10px with 4px margin renders in Upper case
        
        Args:
            text: can contain A-Z, 0-9, Symbol descriptions from ["[GRAPHICS]", "[AUDIO]", "[SETTINGS]", "[PLAY]", "[QUIT]", "[SAVE]", "[DISK]", "[LOAD]", "[BACK]", "[X]", "[COIN]"], seperated by space'''
        text_length = 0
        i = 0

        while i < len(text):
            if text[i] == "[":
                end = text.find("]", i)
                if end != -1:
                    token = text[i: end + 1]
                    if token in self.icons:
                        text_length += self.icon_size + self.icon_spacing
                        i = end + 1
                        continue
            if text[i] == " ":
                text_length += self.space_width
            else:
                text_length += self.text_size
                if i < len(text) - 1 and text[i + 1] not in ["]"]:
                    text_length += self.text_spacing
            i += 1
        
        surface = pygame.Surface((text_length, self.text_height), pygame.SRCALPHA)

        i = 0
        x = 0
        while i < len(text):
            if text[i] == "[":
                end = text.find("]", i)
                if end != -1:
                    token = text[i: end + 1]
                    if token in self.icons:
                        surface.blit(self.icons[token], (x, 0))
                        x += self.icon_size + self.icon_spacing
                        i = end + 1
                        continue
            char = text[i]

            if char == " ":
                x += self.space_width
            else:
                if char.upper() in self.letters:
                    surface.blit(self.letters[char.upper()], (x, 0))
                
                x += self.text_size

                if i < len(text) - 1 and text[i + 1] not in ["]"]:
                    x += self.text_spacing
            i += 1
        
        return surface

    def render_text(self, surface: pygame.Surface, text: str, coordinates: tuple[int, int], scale: int):
        '''draws the letters of the text on the given Surface at given coordinates with the given scale
        
        Args:
            surface: normal pygame Surface where to draw on
            text: letters to be written on the surface
            coordinates: pygame Coordinate style (x, y) is the upper left corner of the text
            scale: the UI Scale at which the text is scaled to'''
        text_surface = self.create_text_surface(text)
        self.render_text_surface(surface, text_surface, coordinates, scale)
    
    def render_text_surface(self, surface: pygame.Surface, text_surface: pygame.Surface, coordinates: tuple[int, int], scale: int):
        text_surface_scaled = pygame.transform.scale(text_surface, (text_surface.get_width() * scale, self.text_height * scale))

        surface.blit(text_surface_scaled, (coordinates[0], coordinates[1]))

    def render_text_surface_unscaled(self, surface: pygame.Surface, text_surface: pygame.Surface, coordinates: tuple[int, int]):
        surface.blit(text_surface, (coordinates[0], coordinates[1]))

    def recolor_image(self, image: pygame.Surface, to_color: pygame.Color, from_color: pygame.Color = Colors.DARK_GOLD.value):
        '''recolors the pixels from a color to a color
        
        Args:
            image: the image where to replace the color at
            to_colot: destionation color, where the function replaces to (R, G, B)
            from_color: color which gets replaced by the new color, (R, G, B), default is dark gold'''
        pixels = pygame.PixelArray(image)

        pixels.replace(
            image.map_rgb(from_color),
            image.map_rgb(to_color)
        )
        del pixels
        return image