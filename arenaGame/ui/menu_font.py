import pygame
from settings import ASSET_DIR

class MenuFont():
    def __init__(self):
        self.letters = {}
        self._load_font()

    def _load_font(self):
        '''loads the letters upper alphabet & 0 - 9 into the self.letters dict'''
        # letters are 6x10px with 2px margin 
        letters_sheet = pygame.image.load(ASSET_DIR / "font/menu_font.png").convert_alpha()
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        for index, letter in enumerate(alphabet):
            self.letters[letter] = letters_sheet.subsurface(0 + index * 8, 0, 6, 10)
    
    def create_text_surface(self, text: str) -> pygame.Surface:
        '''creates a pygame Surface containg the Text written in the menu font, charsize 6x10 with 2px margin, renders in Upper case'''
        surface = pygame.Surface((len(text) * 8, 10), pygame.SRCALPHA)

        for index, char in enumerate(text.upper()):
            if char in self.letters:
                surface.blit(self.letters[char], (index * 8, 0))
        
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