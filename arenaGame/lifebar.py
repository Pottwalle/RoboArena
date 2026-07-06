import pygame

class Lifebar:
    def __init__(self, player):
        self.player = player

    def draw(self, screen, x, y, width, height):
        # calculate current health/max health ratio and draw the lifebar
        ratio = self.player.stats.hp / self.player.stats.get("max_hp")
        pygame.draw.rect(screen, (0,0,0), (x, y, width, height))
        pygame.draw.rect(screen, (255,0,0), (x, y, width * ratio, height))