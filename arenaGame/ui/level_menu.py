import pygame
from ui.ui_element import UIElement
from .ui_manager import UIManager
from .texture_button import TextureButton
from settings import settings
from ui.menu_font import MenuFont

class LevelSelectMenu:
    ''' Level select menu UI class'''
    def __init__(self, menu_font: MenuFont, on_main_menu, on_start):
        self.ui = UIManager()
        self.menu_font = menu_font
        self.scale = settings.UI_SCALE

        self.bg = pygame.transform.scale(pygame.image.load(settings.ASSET_DIR/"ui/settings_bg.png").convert(), (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        ui_elements = pygame.image.load(settings.ASSET_DIR/"ui/ui_elements.png")

        hover_texture = ui_elements.subsurface((0,54, 79, 18)).convert_alpha()
        normal_texture = ui_elements.subsurface((0,72, 79, 18)).convert_alpha()

        menu_text = menu_font.create_text_surface("SELECT LEVEL AND DIFFICULTY!").convert_alpha()
        self.scaled_menu_text = UIElement.scale_surface(menu_text, self.scale)

        self.levels = ["Level 1", "Level 2", "Level 3"]
        self.difficulties = ["Easy", "Medium", "Hard"]

        self.level_index = 0
        self.diff_index = 0

        button_w = 79
        button_h = 18

        center_x = 180
        top_y = 27
        bottom_y = 55

        '''Arrows for selection'''
        self.ui.add(TextureButton((center_x - 100, top_y, 79, 18), "PREV", normal_texture, hover_texture, self.scale, self.prev_level, text_button=True))
        self.ui.add(TextureButton((center_x + 20, top_y, 79, 18), "NEXT", normal_texture, hover_texture, self.scale, self.next_level, text_button=True))
        self.ui.add(TextureButton((center_x - 100, bottom_y, 79, 18), "PREV", normal_texture, hover_texture, self.scale, self.prev_diff, text_button=True))
        self.ui.add(TextureButton((center_x + 20, bottom_y, 79, 18), "NEXT", normal_texture, hover_texture, self.scale, self.next_diff, text_button=True))

        '''Start and Main Menu buttons'''
        self.ui.add(TextureButton(
            (center_x, 150, button_w, button_h), 
            "START", 
            normal_texture, 
            hover_texture, 
            self.scale, 
            lambda: on_start(self.levels[self.level_index], self.difficulties[self.diff_index]),
            text_button=True
            ))
        
        self.ui.add(TextureButton(
            (center_x - 150, 150, 79, 18),
            "MAIN MENU",
            normal_texture,
            hover_texture,
            self.scale,
            on_main_menu,
            text_button=True
        ))

    '''choosing logic'''
    def prev_level(self):
        self.level_index = (self.level_index - 1) % len(self.levels)

    def next_level(self):
        self.level_index = (self.level_index + 1) % len(self.levels)

    def prev_diff(self):
        self.diff_index = (self.diff_index - 1) % len(self.difficulties)

    def next_diff(self):
        self.diff_index = (self.diff_index + 1) % len(self.difficulties)

    '''Event handling and drawing'''
    def handle_event(self, event):
        self.ui.handle_event(event)

    def draw(self, surface):
        surface.blit(self.bg, (0, 0))
        self.menu_font.render_text_surface_unscaled(surface, self.scaled_menu_text, (settings.SCREEN_WIDTH // 2 - self.scaled_menu_text.get_width() // 2, 50))
        level_text = self.menu_font.create_text_surface(self.levels[self.level_index])
        level_text_scaled = UIElement.scale_surface(level_text, self.scale)
        surface.blit(level_text_scaled, (settings.SCREEN_WIDTH//2 - level_text_scaled.get_width()//2, 120))

        diff_text = self.menu_font.create_text_surface(self.difficulties[self.diff_index])
        diff_text_scaled = UIElement.scale_surface(diff_text, self.scale)
        surface.blit(diff_text_scaled, (settings.SCREEN_WIDTH//2 - diff_text_scaled.get_width()//2, 240))

        self.ui.draw(surface)

    def update(self, dt):
        self.ui.update(dt)