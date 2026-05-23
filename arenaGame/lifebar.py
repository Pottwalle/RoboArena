import pygame

class Lifebar:
    def __init__(self, player, screen):
        self.player = player
        self.screen = screen

    def draw(self):
        # calculate current health/max health ratio and draw the lifebar
        ratio = self.player.hp/self.player.max_hp
        pygame.draw.rect(self.screen, (0,0,0), (10,10, 200, 20))
        pygame.draw.rect(self.screen, (255,0,0), (10,10,200*ratio,20))