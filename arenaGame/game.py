import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, FPS
from arena import Arena
from player import Player
from movement import Movement
from damage import Damage
from lifebar import Lifebar
from enemy import Enemy
from tile import load_tiles
from club import Club
from musik_manager import spiele_hintergrundmusik
from ObjectCollision import ObjectCollision

pygame.init()

# hintergrundmusik
spiele_hintergrundmusik()

# Game Window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# set window title & icon
pygame.display.set_caption("Robot Arena")

# set Background
background = ("gray")

load_tiles()
# Arena
arena = Arena(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE)
# Tilemap for movement
movement = Movement(arena.grid)
# create the player with its base stats
player = Player(
    arena.offset_x + arena.grid_width // 2,
    arena.offset_y + arena.grid_height // 2,
    10, 0, 100
)
player.setWeapon(Club(player))
# Gegner-Liste erstellen
#  x, y, r, alpha, base_speed, movement, speed_modifier=1, health=10, damage=5, movementType="random"
enemies = [
    Enemy(arena.offset_x + 100, arena.offset_y + 100, 10, 0, 10, movement, movementType="aggressive"),
    Enemy(arena.offset_x + 200, arena.offset_y + 150, 10, 0, 10, movement, movementType="random"),
    Enemy(arena.offset_x + 300, arena.offset_y + 200, 10, 0, 10, movement, movementType="passive"),
]

# create damage handler
damage = Damage(movement)
#create collision handler
collision = ObjectCollision()
# create lifebar
lifebar = Lifebar(player, screen)

# basic game loop
clock = pygame.time.Clock()
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # delta time (time elapsed since last frame)
    dt = clock.tick(FPS) / 1000
    # print("FPS: ", clock.get_fps())

    player.update(dt, movement)

    for enemy in enemies:
        enemy.update(dt, player, clock)

    # apply weapon damage to enemies
    if player.weapon is not None:
        player.weapon.update(dt, enemies)

    #detect & resolve object collision
    collision.handle_player_enemy(player, enemies, damage_on_contact=True)
    collision.handle_enemy_enemy(enemies)


    # apply damage to player based on current tile
    damage.applyDamage(player, dt)

    # player camera, move the arena in the way that the player stays centered, represents the camera coordinates (center screen)
    camera = player.position - pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # draw Background
    screen.fill(background)
    # draw game map and player
    arena.draw_map(screen, camera)
    player.draw(screen, camera)
    # draw weapon 
    if player.weapon is not None:
        player.weapon.draw(screen, camera)
    #draw enemies
    for enemy in enemies:
        enemy.draw(screen, camera)

    # remove dead enemies
    enemies = [enemy for enemy in enemies if enemy.health > 0]
    # draw lifebar on top of everything
    lifebar.draw()
    pygame.display.update()
    