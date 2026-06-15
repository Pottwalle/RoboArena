import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, FPS, UI_SCALE
from arena import Arena
from player import Player
from movement import Movement
from damage import Damage
from lifebar import Lifebar
from enemy import Enemy
from tile import load_tiles
from club import Club
from enum import Enum, auto
from ui.main_menu import MainMenu
from ui.game_ui import GameUI
from levelbar import Levelbar
from ui.menu_font import MenuFont
from ui.settings_menu import SettingsMenu


pygame.init()

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
enemies = [
    Enemy(arena.offset_x + 100, arena.offset_y + 100, 10, 0, 60, movement, movementType="aggressive"),
    Enemy(arena.offset_x + 200, arena.offset_y + 150, 10, 0, 40, movement, movementType="random"),
    Enemy(arena.offset_x + 300, arena.offset_y + 200, 10, 0, 20, movement, movementType="passive"),
]

# create damage handler
damage = Damage(movement)
# create lifebar & Levelbar
lifebar = Lifebar(player)
levelbar = Levelbar(player, UI_SCALE)

# gameloop parameters, need init before set_quit()
clock = pygame.time.Clock()
running = True

# Game states
class GameState(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    ESC_MENU = auto()
    SETTINGS = auto()

state = GameState.MAIN_MENU

# callback functions to set Game states
def set_playing():
    global state
    state = GameState.PLAYING
def set_settings():
    global state
    state = GameState.SETTINGS
def set_quit():
    global running
    running = False

# Menus
menu_font = MenuFont()
main_menu = MainMenu(set_playing, set_settings, set_quit)
settings_menu = SettingsMenu(menu_font)
game_ui = GameUI(lifebar, levelbar)

# basic game loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if state == GameState.ESC_MENU:
                    state = GameState.PLAYING
                else:
                    state = GameState.ESC_MENU
        
        main_menu.handle_event(event)

    # delta time (time elapsed since last frame)
    dt = clock.tick(FPS) / 1000
    # print("FPS: ", clock.get_fps())

    if state == GameState.PLAYING:
        player.update(dt, movement)

        for enemy in enemies:
            enemy.update(dt, player, clock)

        # apply weapon damage to enemies
        if player.weapon is not None:
            player.weapon.update(dt, enemies)

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
        # draw the whole game UI on top
        game_ui.draw(screen)

    elif state == GameState.MAIN_MENU:
        # main_menu.handle_event(event)
        main_menu.update(dt)
        main_menu.draw(screen)
    
    elif state == GameState.SETTINGS:
        settings_menu.draw(screen)

    elif state == GameState.ESC_MENU:
        pass
    
    pygame.display.update()
    