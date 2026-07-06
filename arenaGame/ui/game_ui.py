from .ui_manager import UIManager
from settings import settings
import pygame
from lifebar import Lifebar
from levelbar import Levelbar
from ui.menu_font import MenuFont
from player import Player

class GameUI():
    def __init__(self, lifebar: Lifebar, levelbar: Levelbar, small_font: MenuFont, menu_font: MenuFont, player: Player):
        self.ui = UIManager()
        self.scale = settings.UI_SCALE
        self.small_font = small_font
        self.menu_font = menu_font

        # ui elements
        self.lifebar = lifebar
        self.levelbar = levelbar
        self.player = player

        self.ui_texture = pygame.transform.scale(pygame.image.load(settings.ASSET_DIR / "ui/ui.png"), (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    
    def handle_event(self, event):
        self.ui.handle_event(event)
    
    def update(self, dt):
        self.ui.update(dt)

    def draw(self, surface: pygame.Surface, clock: pygame.time.Clock):
        self.draw_fps(surface, clock)
        self.lifebar.draw(surface, 10 * self.scale, 8 * self.scale, 80 * self.scale, 5 * self.scale)
        self.levelbar.draw(surface)
        surface.blit(self.ui_texture, (0, 0))
        # display current level
        level = str(self.player.level)
        level_surface = self.menu_font.create_text_surface(level)
        w = level_surface.get_width()
        h = level_surface.get_height()
        surface.blit(pygame.transform.scale(level_surface, (w * self.scale, h * self.scale)), ((317 - w) * self.scale, 168 * self.scale))

        self.ui.draw(surface)
    
    def draw_fps(self, surface: pygame.Surface, clock: pygame.time.Clock):
        if settings.SHOW_FPS:
            self.small_font.render_text(surface, str(clock.get_fps()), (308 * self.scale, 3 * self.scale), settings.UI_SCALE)