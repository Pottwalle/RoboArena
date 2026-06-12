import pygame
from settings import ASSET_DIR
from player import Player

class Levelbar:
    def __init__(self, player: Player, scale):
        self.player = player

        self.scale = scale
        ui_elements = pygame.image.load(ASSET_DIR / "ui/ui_elements.png")
        # pos im stylesheet 0, 72, 138, 3px
        self.xp_bar_texture = pygame.transform.scale(ui_elements.subsurface((0, 72, 138, 3)).convert_alpha(), (138 * self.scale, 3 * self.scale))
        self.xp_bar_underlay = pygame.transform.scale(ui_elements.subsurface((0, 75, 138, 3)).convert_alpha(), (138 * self.scale, 3 * self.scale))
    
    def draw(self, surface: pygame.Surface):
        progress = self.player.get_level_prograss()

        surface.blit(self.xp_bar_underlay, (91 * self.scale, 176 * self.scale))
        surface.blit(self.xp_bar_texture, (91 * self.scale, 176 * self.scale), (0, 0, int(138 * self.scale * progress), self.xp_bar_texture.get_height()))
    
