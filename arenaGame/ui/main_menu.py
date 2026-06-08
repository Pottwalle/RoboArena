import pygame
from .ui_manager import UIManager
from .button import Button

class MainMenu():
    def __init__(self, set_playing):
        self.font = pygame.font.Font("freesansbold.ttf", 32)

        self.ui = UIManager()

        self.ui.add(Button(
            (300, 250, 200, 60),
            "start",
            self.font,
            set_playing
        ))
    
    def handle_event(self, event):
        self.ui.handle_event(event)
    
    def update(self, dt):
        self.ui.update(dt)

    def draw(self, surface: pygame.Surface):
        surface.fill((20, 20, 30))
        self.ui.draw(surface)