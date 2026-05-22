import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, FPS
from arena import Arena
from player import Player
from tile import load_tiles


pygame.init()

# Game Window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# set window title & icon
pygame.display.set_caption("Robot Arena")

#set Background
background = ("gray")
load_tiles()

# Arena
arena = Arena(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE)
# create the player with its base stats
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, 0, 100)

# basic game loop
clock = pygame.time.Clock()
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # delta time (time elapsed since last frame)
    dt = clock.tick(FPS) / 1000
    print("FPS: ", clock.get_fps())

    player.update(dt)

    # player camera, move the arena in the way that the player stays centered, represents the camera coordinates (center screen)
    camera = player.position - pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # draw Background
    screen.fill(background)
    #draw game map and player
    arena.draw_map(screen, camera)
    player.draw(screen, camera)
    pygame.display.update()