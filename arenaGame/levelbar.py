import pygame
from settings import ASSET_DIR
from player import Player

class Levelbar:
    def __init__(self, player: Player, scale):
        self.player = player
        # summed up xp needed per level
        self.xp_per_level = [0, 50, 100, 180, 300, 500, 750, 1200]

        self.scale = scale
        ui_elements = pygame.image.load(ASSET_DIR / "ui/ui_elements.png")
        # pos im stylesheet 0, 72, 138, 3
        self.xp_bar_texture = pygame.transform.scale(ui_elements.subsurface((0, 72, 138, 3)).convert_alpha(), (138 * self.scale, 3 * self.scale))
        self.xp_bar_underlay = pygame.transform.scale(ui_elements.subsurface((0, 75, 138, 3)).convert_alpha(), (138 * self.scale, 3 * self.scale))
    
    def draw(self, surface: pygame.Surface):
        surface.blit(self.xp_bar_underlay, (91 * self.scale, 176 * self.scale))
        surface.blit(self.xp_bar_texture, (91 * self.scale, 176 * self.scale), (0, 0, int(138 * self.scale * self._calculate_level_prograss()), self.xp_bar_texture.get_height()))
    
    def _calculate_level_prograss(self) -> float:
        current_lvl = self.player.level
        current_lvl_xp = self.xp_per_level[current_lvl]
        next_lvl_xp = self.xp_per_level[current_lvl + 1]

        return (self.player.xp - current_lvl_xp) / (next_lvl_xp - current_lvl_xp)