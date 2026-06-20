import pygame
from settings import settings
from .texture_button import TextureButton
from .menu_font import MenuFont

class OptionsButton():
    def __init__(self, rect: pygame.rect.Rect, options: list[str], menu_font: MenuFont, scale: int, callback, selected=0):
        '''Represents a button which can cycle through multiple given options

        Args:
            rect: unscaled coordinates and with height of the button size, make shure that the with is at least 14px (only button width + additional space for text) and height should be 10px
            options: list of strings where the you can cycle through with left / right arrow
            menu_font: text style with which the middle text (current option) is displayed as
            scale: Menu UI sclae used for scaling buttons / text
            callback: function to change the state at the confirmation of the menu #TODO
            selected: current selected option, should be inside the list
        '''
        self.rect = pygame.Rect(rect)
        self.rect.width = max(14, rect[2]) # ensure that both left and right button have space
        self.rect.height = max(10, rect[3])
        self.scale = scale

        self.options = options
        self.callback = callback
        self.selected = selected
        self.menu_font = menu_font

        ui_elements = pygame.image.load(settings.ASSET_DIR / "ui/ui_elements.png")
        # scale of the arrows buttons is 7x10 px
        arrow_w = 7
        arrow_h = 10
        left_arrow_texture = ui_elements.subsurface((0, 81, arrow_w, arrow_h)).convert_alpha() # unscaled yet
        right_arrow_texture = ui_elements.subsurface((9, 81, arrow_w, arrow_h)).convert_alpha() # unscaled yet
        left_arrow_hover_texture = ui_elements.subsurface((18, 81, arrow_w, arrow_h)).convert_alpha() # unscaled yet
        right_arrow_hover_texture = ui_elements.subsurface((27, 81, arrow_w, arrow_h)).convert_alpha() # unscaled yet

        self.left_arrow = TextureButton((rect[0], rect[1], arrow_w, arrow_h), "", left_arrow_texture, left_arrow_hover_texture, scale, self.option_left)
        self.right_arrow = TextureButton((rect[0] + rect[2] - arrow_w, rect[1], arrow_w, arrow_h), "", right_arrow_texture, right_arrow_hover_texture, scale, self.option_right)

        self.options_surface_scaled: list[pygame.Surface] = []
        for i in range(len(options)):
            text_surface = menu_font.create_text_surface(options[i])
            scaled_text_surface = pygame.transform.scale(text_surface, (text_surface.get_width() * self.scale, 10 * self.scale)) # already scale here so we dont have to every game loop
            self.options_surface_scaled.append(scaled_text_surface)

    def handle_event(self, event: pygame.event.Event):
        self.left_arrow.handle_event(event)
        self.right_arrow.handle_event(event)
    
    def update(self, dt):
        pass
    
    def draw(self, surface: pygame.Surface):
        self.left_arrow.draw(surface)
        self.right_arrow.draw(surface)

        # scaled button width - text width already scaled
        text_x = self.rect[2] * self.scale // 2 - self.options_surface_scaled[self.selected].get_width() // 2
        self.menu_font.render_text_surface_unscaled(surface, self.options_surface_scaled[self.selected], (self.rect[0] * self.scale + text_x, self.rect[1] * self.scale))
    
    def option_right(self):
        '''sets the selection to the next item and calls the callback function with the currently selected string'''
        self.selected = (self.selected + 1) % len(self.options)
        self.callback(self.options[self.selected]) # transfers the new value to the callback function
    
    def option_left(self):
        '''sets the selection to the previous item  and calls the callback function with the currently selected string'''
        self.selected = (self.selected - 1) % len(self.options)
        self.callback(self.options[self.selected]) # transfers the new value to the callback function