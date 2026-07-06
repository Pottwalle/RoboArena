import pygame
from settings import settings
from arena import Arena
from player import Player
from movement import Movement
from damage import Damage
from lifebar import Lifebar
from tile import load_tiles
from club import Club
from bow import Bow
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
from interactable import InteractableManager
from ui.death_menu import DeathMenu
from ui.level_menu import LevelSelectMenu
from ui.victory_menu import VictoryMenu
from ui.enemy_counter import EnemyCounter
from ui.intro_game import IntroScreen

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
arena = Arena(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.TILE_SIZE, "Level 3", "Easy")

# init Items dictionary sorted by item names contained in assets/data/items.json
menu_font = MenuFont("menu_font")
small_font = MenuFont("small_font", 4, 6, 1, 10, 4)
items = load_items(menu_font, small_font)

# Tilemap for movement
movement = Movement(arena.grid)

# create the player with its base stats
player = Player(
    arena.offset_x + arena.grid_width // 2,
    arena.offset_y + arena.grid_height // 2,
    10, 0, 100
)
player.setWeapon(Club(player))
# Gegner-Liste erstellen, getötete Gegner Zählen
#  x, y, r, alpha, base_speed, movement, speed_modifier=1, hp=10, damage=5, movementType="random"
enemies = []
overall_killed_enemies = 0

# create damage handler
damage = Damage(movement)

# create lifebar & Levelbar
lifebar = Lifebar(player)
levelbar = Levelbar(player, settings.UI_SCALE)
enemy_counter = EnemyCounter(settings.UI_SCALE, MenuFont("small_font", 4, 6, 1, 10, 4))

# create collision handler
collision = ObjectCollision(arena.grid)

# create interactables manager (hp packs, traps, ...), platzierbar von Spieler & Gegnern
interactables = InteractableManager()

# Beispiel: 3 Health Packs zufällig auf "dirt"-Tiles platzieren (z.B. beim Levelstart)
for spawn_pos in arena.get_random_tile_positions("dirt", count=3):
    interactables.spawn_health_pack(spawn_pos.x, spawn_pos.y)

# gameloop parameters, need init before set_quit()
clock = pygame.time.Clock()
running = True


# Game states
class GameState(Enum):
    MAIN_MENU = auto()
    INTRO = auto()
    PLAYING = auto()
    ESC_MENU = auto()
    SETTINGS = auto()
    INVENTORY = auto()
    DEATH_MENU = auto()
    SELECT_LEVEL_MENU = auto()
    VICTORY_MENU = auto()


state = GameState.MAIN_MENU
previous_state = GameState.MAIN_MENU


# callback functions to set Game states
def start_game(level=None, difficulty=None):
    """Baut Arena/Player/Enemies etc. neu auf und wechselt in den PLAYING-State.
    Wird NICHT direkt vom Menu aufgerufen, sondern erst nachdem die Intro durchgelaufen ist
    (siehe set_playing weiter unten)."""
    global state, previous_state, arena, movement, player, enemies, damage, lifebar, levelbar, collision, interactables, game_ui, inventory, overall_killed_enemies

    previous_state = state
    state = GameState.PLAYING

    # Default-Werte falls direkt aus MainMenu gestartet
    if level is None:
        level = "Level 1"
    if difficulty is None:
        difficulty = "Easy"

    print("Starting:", level, difficulty)

    # Arena NEU LADEN basierend auf Level
    arena = Arena(
        settings.SCREEN_WIDTH,
        settings.SCREEN_HEIGHT,
        settings.TILE_SIZE,
        level_path=level,
        difficulty=difficulty
    )

    # Movement neu erzeugen
    movement = Movement(arena.grid)

    # Player neu erzeugen
    player = Player(
        arena.offset_x + arena.grid_width // 2,
        arena.offset_y + arena.grid_height // 2,
        10, 0, 100
    )
    player.setWeapon(Club(player))

    # Gegner abhängig von Difficulty laden
    enemies = []

    overall_killed_enemies = 0
    arena.generate_enemy(enemies, movement, items)

    # Damage, UI, Collision, Interactables neu erzeugen
    damage = Damage(movement)
    lifebar = Lifebar(player)
    levelbar = Levelbar(player, settings.UI_SCALE)
    collision = ObjectCollision(arena.grid)
    interactables = InteractableManager()
    inventory = Inventory(player.inventory)

    # Health Packs spawnen
    for spawn_pos in arena.get_random_tile_positions("dirt", count=3):
        interactables.spawn_health_pack(spawn_pos.x, spawn_pos.y)

    game_ui = GameUI(lifebar, levelbar, small_font, menu_font, player, enemy_counter)

def set_playing(level=None, difficulty=None):
    """Wird vom MainMenu / LevelSelectMenu aufgerufen. Zeigt zuerst die Intro,
    start_game() wird erst aufgerufen, wenn die Intro fertig durchgeklickt wurde."""
    global state, previous_state
    previous_state = state
    state = GameState.INTRO
    intro_screen.reset()
    intro_screen.on_finished = lambda: start_game(level, difficulty)

def resume_game():
    """Wird vom EscMenu benutzt, um OHNE Intro und OHNE Reset einfach weiterzuspielen."""
    global state
    state = GameState.PLAYING

def set_settings():
    global state, previous_state
    previous_state = state
    state = GameState.SETTINGS


def set_select_level():
    global state, previous_state
    previous_state = state
    state = GameState.SELECT_LEVEL_MENU


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

def resume_game():
    global state
    state = GameState.PLAYING


# Intro content
INTRO_PAGES = [
    "Vor langer Zeit, als die Wikinger noch das Sagen hatten, war die Welt noch in Ordnung. "
    "Doch eines Tages kamen finstere Mächte ins Land, um die Welt an sich zu reißen. "
    "Die Monster schienen jede Schlacht zu gewinnen. Es gab keine Überlebenden – bis auf einen: "
    "Olaf, den ehemaligen Stammesführer der Wikinger.\n\n"
    "Er sah seine einzige Chance darin, sich in einen Cyborg zu verwandeln, und schwor Rache an denen, "
    "die sein geliebtes Land zerstört hatten.\n\n"
    "\"Deine Reise beginnt jetzt...\""
]

# Menus
intro_screen = IntroScreen(INTRO_PAGES)
main_menu = MainMenu(set_select_level, set_settings, set_quit)
settings_menu = SettingsMenu(menu_font, set_back_from_settings)
esc_menu = EscMenu(menu_font, resume_game, set_main_menu, set_settings)
game_ui = GameUI(lifebar, levelbar, small_font, menu_font, player, enemy_counter)
inventory = Inventory(player.inventory)
death_menu = DeathMenu(menu_font, set_main_menu)
level_select_menu = LevelSelectMenu(menu_font, set_main_menu, set_playing)
victory_menu = VictoryMenu(menu_font, set_main_menu)

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
                elif state == GameState.INVENTORY:
                    state = GameState.PLAYING
                elif state == GameState.DEATH_MENU:
                    state = GameState.MAIN_MENU
                elif state == GameState.SELECT_LEVEL_MENU:
                    state = GameState.MAIN_MENU
                elif state == GameState.VICTORY_MENU:
                    state = GameState.MAIN_MENU
            if event.key == pygame.K_i:
                if state == GameState.PLAYING:
                    state = GameState.INVENTORY
                    inventory.last_gamestate_bg = screen.copy()
                else:
                    state = GameState.PLAYING

        # only pass events to active menu
        if state == GameState.MAIN_MENU:
            main_menu.handle_event(event)
        elif state == GameState.INTRO:
            intro_screen.handle_event(event)
        elif state == GameState.SETTINGS:
            settings_menu.handle_event(event)
        elif state == GameState.ESC_MENU:
            esc_menu.handle_event(event)
        elif state == GameState.INVENTORY:
            inventory.handle_event(event)
        elif state == GameState.DEATH_MENU:
            death_menu.handle_event(event)
        elif state == GameState.SELECT_LEVEL_MENU:
            level_select_menu.handle_event(event)
        elif state == GameState.VICTORY_MENU:
            victory_menu.handle_event(event)

    # delta time (time elapsed since last frame)
    dt = clock.tick(settings.FPS) / 1000

    if state == GameState.PLAYING:
        # player camera, move the arena in the way that the player stays centered, represents the camera coordinates (center screen)
        camera = player.position - pygame.Vector2(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2)

        player.update(dt, movement, camera)
        if player.stats.hp <= 0 and dt > 0:
            state = GameState.DEATH_MENU
            death_menu = DeathMenu(menu_font, set_main_menu)

        for enemy in enemies:
            enemy.update(dt, player, clock)
            # Gegner mit places_traps=True legen automatisch in festen Abständen eine Falle
            if enemy.should_place_trap():
                interactables.spawn_at_entity("trap", enemy, owner="enemy")
            if enemy.weapon is not None:
                enemy.weapon.update(dt, [player])
            if enemy.weapon is None and enemy.movement_type == "passive":
                enemy.setWeapon(Bow(enemy))

        # apply weapon damage to enemies
        if player.weapon is not None:
            player.weapon.update(dt, enemies)

        # detect & resolve object collision
        collision.handle_player_enemy(player, enemies, damage_on_contact=True)
        collision.handle_enemy_enemy(enemies)

        # apply damage to player based on current tile
        damage.applyDamage(player, dt)

        # update interactables (health packs, traps, ...): wendet Effekte an
        # Berührung an und entfernt verbrauchte/abgelaufene Objekte
        interactables.update(dt, player, enemies, arena)

        # player camera, move the arena in the way that the player stays centered, represents the camera coordinates (center screen)
        camera = player.position - pygame.Vector2(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2)

        # draw Background
        screen.fill(background)
        # draw game map and player
        arena.draw_map(screen, camera)
        # draw interactables (health packs, traps, ...) unterhalb der Einheiten
        interactables.draw(screen, camera)
        player.draw(screen, camera)
        # draw weapon
        if player.weapon is not None:
            player.weapon.draw(screen, camera)

        for enemy in enemies:
            if enemy.weapon is not None:
                enemy.weapon.draw(screen, camera)

        # draw enemies
        for enemy in enemies:
            enemy.draw(screen, camera)

        # remove dead enemies & handle rewards
        killed_enemies = [enemy for enemy in enemies if enemy.hp <= 0]
        for enemy in killed_enemies:
            if hasattr(enemy, 'reward'):
                enemy.reward.apply_to_player(player)
                if enemy.reward.xp != 0 or enemy.reward.items != []: # spawns the reward at the players ground if it couldnt get applied
                    interactables.spawn_reward_at_player(player, enemy.reward)

        overall_killed_enemies += len(killed_enemies)
        enemy_counter.update_count(overall_killed_enemies)
        if overall_killed_enemies >= arena.get_kill_requirement():
            state = GameState.VICTORY_MENU
            victory_menu = VictoryMenu(menu_font, set_main_menu)

        enemies = [enemy for enemy in enemies if enemy.hp > 0]

        # generates enemies according to the number via difficulty in arena.py method 1 a loop, until the count is correct
        arena.generate_enemy(enemies, movement, items)

        # draw the whole game UI on top
        game_ui.draw(screen, clock)

    elif state == GameState.MAIN_MENU:
        # main_menu.handle_event(event)
        # main_menu.update(dt)
        main_menu.draw(screen)

    elif state == GameState.INTRO:
        intro_screen.update(dt)
        intro_screen.draw(screen)

    elif state == GameState.SETTINGS:
        settings_menu.draw(screen)
        # settings_menu.update(dt)

    elif state == GameState.ESC_MENU:
        esc_menu.draw(screen)
        esc_menu.update(dt)

    elif state == GameState.INVENTORY:
        inventory.draw(screen)
        inventory.update(dt)

    elif state == GameState.DEATH_MENU:
        death_menu.draw(screen)
        death_menu.update(dt)

    elif state == GameState.SELECT_LEVEL_MENU:
        level_select_menu.draw(screen)
        level_select_menu.update(dt)

    elif state == GameState.VICTORY_MENU:
        victory_menu.draw(screen)
        victory_menu.update(dt)

    pygame.display.update()