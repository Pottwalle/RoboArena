import pygame
from settings import settings
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
from ui.esc_menu import EscMenu
from ui.inventory import Inventory
from musik_manager import spiele_hintergrundmusik
from ObjectCollision import ObjectCollision
from item_loader import load_items


pygame.init()

# hintergrundmusik
spiele_hintergrundmusik()

# Game Window
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
# set window title & icon
pygame.display.set_caption("Robot Arena")

# set Background
background = ("gray")

load_tiles()
# Arena
arena = Arena(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.TILE_SIZE, "arenaGame/level3.txt")

# init Items dictionary sorted by item names contained in assets/data/items.json
items = load_items()

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
    Enemy(arena.offset_x + 100, arena.offset_y + 100, 10, 0, 60, movement, movementType="aggressive", xp_reward=25, item_reward=[items["barbarian_helmet"]]),
    Enemy(arena.offset_x + 200, arena.offset_y + 150, 10, 0, 40, movement, movementType="random", xp_reward=15, item_reward=[items["barbarian_helmet"], items["barbarian_chestplate"]]),
    Enemy(arena.offset_x + 300, arena.offset_y + 200, 10, 0, 20, movement, movementType="passive", xp_reward=10, item_reward=[items["barbarian_sword"]]),
]

# create damage handler
damage = Damage(movement)

# create lifebar & Levelbar
lifebar = Lifebar(player)
levelbar = Levelbar(player, settings.UI_SCALE)

#create collision handler
collision = ObjectCollision()

# gameloop parameters, need init before set_quit()
clock = pygame.time.Clock()
running = True

# Game states
class GameState(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    ESC_MENU = auto()
    SETTINGS = auto()
    INVENTORY = auto()

state = GameState.MAIN_MENU
previous_state = GameState.MAIN_MENU

# callback functions to set Game states
def set_playing():
    global state, previous_state
    previous_state = state
    state = GameState.PLAYING
def set_settings():
    global state, previous_state
    previous_state = state
    state = GameState.SETTINGS
def set_back_from_settings():
    global state, previous_state
    state = previous_state
def set_quit():
    global running
    running = False
def set_main_menu():
    global state, previous_state
    previous_state = state
    state = GameState.MAIN_MENU

# Menus
menu_font = MenuFont()
main_menu = MainMenu(set_playing, set_settings, set_quit)
settings_menu = SettingsMenu(menu_font, set_back_from_settings)
esc_menu = EscMenu(menu_font, set_playing, set_main_menu, set_settings)
game_ui = GameUI(lifebar, levelbar)
inventory = Inventory(player.inventory)

# basic game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if state == GameState.PLAYING:
                    state = GameState.ESC_MENU
                elif state == GameState.ESC_MENU:
                    state = GameState.PLAYING
                elif state == GameState.SETTINGS:
                    state = GameState.MAIN_MENU
            if event.key == pygame.K_i:
                if state == GameState.PLAYING:
                    state = GameState.INVENTORY
                    inventory.last_gamestate_bg = screen
                else:
                    state = GameState.PLAYING
            
        # only pass events to active menu
        if state == GameState.MAIN_MENU:
            main_menu.handle_event(event)
        elif state == GameState.SETTINGS:
            settings_menu.handle_event(event)
        elif state == GameState.ESC_MENU:
            esc_menu.handle_event(event)
        elif state == GameState.INVENTORY:
            inventory.handle_event(event)
    

    # delta time (time elapsed since last frame)
    dt = clock.tick(settings.FPS) / 1000
    # print("FPS: ", clock.get_fps())

    if state == GameState.PLAYING:
        # player camera, move the arena in the way that the player stays centered, represents the camera coordinates (center screen)
        camera = player.position - pygame.Vector2(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2)

        player.update(dt, movement, camera)

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

        # remove dead enemies & handle rewards
        killed_enemies = [enemy for enemy in enemies if enemy.health <= 0]
        for enemy in killed_enemies:
            if hasattr(enemy, 'reward'):
                enemy.reward.apply_to_player(player)
        
        enemies = [enemy for enemy in enemies if enemy.health > 0]
        # draw the whole game UI on top
        game_ui.draw(screen)

    elif state == GameState.MAIN_MENU:
        # main_menu.handle_event(event)
        # main_menu.update(dt)
        main_menu.draw(screen)
    
    elif state == GameState.SETTINGS:
        settings_menu.draw(screen)
        # settings_menu.update(dt)

    elif state == GameState.ESC_MENU:
        esc_menu.draw(screen)
        # esc_menu.update(dt)
    
    elif state == GameState.INVENTORY:
        inventory.draw(screen)
        # inventory.update(dt)
    
    pygame.display.update()
    