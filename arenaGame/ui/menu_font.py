import pygame
from settings import settings

class MenuFont():
    def __init__(self):
        self.letters = {}
        self.icons = {}
        self._load_font()
        self._load_icons()

    def _load_font(self):
        '''loads the letters upper alphabet & 0 - 9 into the self.letters dict'''
        # letters are 6x10px with 2px margin 
        letters_sheet = pygame.image.load(settings.ASSET_DIR / "font/menu_font.png").convert_alpha()
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        for index, letter in enumerate(alphabet):
            self.letters[letter] = letters_sheet.subsurface(0 + index * 8, 0, 6, 10)
    
    def _load_icons(self):
        '''loads the Symbols 10x10px into the self.icons dict'''
        symbols_sheet = pygame.image.load(settings.ASSET_DIR / "font/icons.png").convert_alpha()
        symbol_keys = ["[GRAPHICS]", "[AUDIO]", "[SETTINGS]", "[PLAY]", "[QUIT]", "[SAVE]", "[DISK]", "[LOAD]", "[BACK]", "[X]", "[COIN]"]
        for index, key in enumerate(symbol_keys):
            self.icons[key] = symbols_sheet.subsurface(0 + index * 10, 0, 10, 10) # letters are 10x10px with 0px margin
    
    def create_text_surface(self, text: str) -> pygame.Surface:
        '''creates a pygame Surface containg the Text written in the menu font, charsize 6x10 with 2px margin, Symbolsize 10x10px with 4px margin renders in Upper case
        
        Args:
            text: can contain A-Z, 0-9, Symbol descriptions from ["[GRAPHICS]", "[AUDIO]", "[SETTINGS]", "[PLAY]", "[QUIT]", "[SAVE]", "[DISK]", "[LOAD]", "[BACK]", "[X]", "[COIN]"], seperated by space'''
        icon_size = 10
        icon_spacing = 4
        text_size = 6
        text_spacing = 2
        space_width = text_size + text_spacing
        
        text_length = 0
        i = 0

        while i < len(text):
            if text[i] == "[":
                end = text.find("]", i)
                if end != -1:
                    token = text[i: end + 1]
                    if token in self.icons:
                        text_length += icon_size + icon_spacing
                        i = end + 1
                        continue
            if text[i] == " ":
                text_length += space_width
            else:
                text_length += text_size
                if i < len(text) - 1 and text[i + 1] not in ["]"]:
                    text_length += text_spacing
            i += 1
        
        surface = pygame.Surface((text_length, 10), pygame.SRCALPHA)

        i = 0
        x = 0
        while i < len(text):
            if text[i] == "[":
                end = text.find("]", i)
                if end != -1:
                    token = text[i: end + 1]
                    if token in self.icons:
                        surface.blit(self.icons[token], (x, 0))
                        x += icon_size + icon_spacing
                        i = end + 1
                        continue
            char = text[i]

            if char == " ":
                x += space_width
            else:
                if char.upper() in self.letters:
                    surface.blit(self.letters[char.upper()], (x, 0))
                
                x += text_size

                if i < len(text) - 1 and text[i + 1] not in ["]"]:
                    x += text_spacing
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
        text_surface_scaled = pygame.transform.scale(text_surface, (text_surface.get_width() * scale, 10 * scale))

        surface.blit(text_surface_scaled, (coordinates[0], coordinates[1]))

    def render_text_surface_unscaled(self, surface: pygame.Surface, text_surface: pygame.Surface, coordinates: tuple[int, int]):
        surface.blit(text_surface, (coordinates[0], coordinates[1]))