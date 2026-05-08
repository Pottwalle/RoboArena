import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE
from arena import Arena


pygame.init()

# Game Window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# set window title & icon
pygame.display.set_caption("Robot Arena")

#set Background
background = ("gray")

# Arena
arena = Arena(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE)

# basic game loop
running = True
while running:
    # draw Background
    screen.fill(background)
    #draw game map
    arena.draw_map(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
# end game
            if event.key == pygame.K_SPACE:
                pygame.quit()

    pygame.display.update()