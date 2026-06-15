import pygame
from settings import ASSET_DIR

class MenuFont():
    def __init__(self):
        self.letters = {}
        self.load_font()

    def load_font(self):
        # letters are 6x10px with 2px margin 
        letters_sheet = pygame.image.load(ASSET_DIR / "font/menu_font.png").convert_alpha()
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        for index, letter in enumerate(alphabet):
            self.letters[letter] = letters_sheet.subsurface(0 + index * 8, 0, 6, 10)
    
    def create_text_surface(self, text: str) -> pygame.Surface:
        surface = pygame.Surface((len(text) * 8, 10), pygame.SRCALPHA)

        for index, char in enumerate(text.upper()):
            if char in self.letters:
                surface.blit(self.letters[char], (index * 8, 0))
        
        return surface

    def render_text(self, surface: pygame.Surface, text: str, coordinates: tuple[int, int], scale: int):
        text_surface = self.create_text_surface(text)
        text_surface = pygame.transform.scale(text_surface, (len(text) * 8 * scale, 10 * scale))

        surface.blit(text_surface, (coordinates[0], coordinates[1]))