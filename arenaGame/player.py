import pygame
import math
from weapon import Weapon
from inventory_manager import InventoryManager
# Roboter Klasse mit Attributen, Position, Radius und Richtung
class Player:
    def __init__(self, x, y, r, alpha, base_speed, speed_modifier = 1, hp=100, max_hp=100):
        '''Represents the Player in the game holding the position, handling the movement and drawing of the player

        Attributes:
            x: players x position
            y: players y position
            r: player radius #WIP
            alpha: direction of the player facing
            base_speed: the bas movement speed of the player
            speed_modifier: the multiplier of the base speed, initially 1
            hp: the health points of the player, initially 100
            max_hp: the maximum health points of the player, initially 100
        '''

        self.position = pygame.Vector2(x, y)
        self.r = r
        self.alpha = alpha
        self.direction = pygame.Vector2()
        self.attack_direction = pygame.Vector2()
        self.hp = hp
        self.max_hp = max_hp

        self.xp = 0
        self.level = 0
        self.xp_breakpoints = [0, 50, 100, 180, 300, 500, 750, 1200, 922337203685477580] # summed up xp needed per level

        self.base_speed = base_speed
        self.speed_modifier = speed_modifier

        # --- movement Erweiterung ---
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 800
        self.max_speed = 300
        self.friction = 0.90

        self.weapon: Weapon = None

        self.inventory = InventoryManager(3, 8)

        '''handles the updating of all player related methods changing the coordinates accordingly'''
    
    def update(self, dt, movement, camera):
        self.input(camera)
        self.alpha = math.degrees(math.atan2(-self.attack_direction.y, self.attack_direction.x))
        self.position = movement.move(self, dt)



    def draw(self, screen, camera):
        screen_position = self.position - camera
        # Zeichnet den blauen Kreis
        pygame.draw.circle(screen, (173, 216, 230), (screen_position.x, screen_position.y), self.r)
        # Zeichnet den schwarzen Rand
        pygame.draw.circle(screen, (0, 0, 0), (screen_position.x, screen_position.y), self.r, 2)

        # Berechnung der Blickrichtung
        rad = math.radians(self.alpha)
        end_x = screen_position.x + math.cos(rad) * self.r
        end_y = screen_position.y - math.sin(rad) * self.r

        # zeichnen Richtungslinie
        pygame.draw.line(screen, (0, 0, 0), (screen_position.x, screen_position.y), (int(end_x), int(end_y)), 2)

    def input(self, camera):
        '''handles the inputs for the player movement and sets the direction value accordingly

        sets the direction y to w = -1, s = 1, and x to a = -1, d = 1'''
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_w]:
            self.direction.y = -1
        if keys[pygame.K_s]:
            self.direction.y = 1
        if keys[pygame.K_a]:
            self.direction.x = -1
        if keys[pygame.K_d]:
            self.direction.x = 1

        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_world_pos = mouse_pos + camera
        to_mouse = mouse_world_pos - self.position

        if to_mouse.length() > 0:
            self.attack_direction = to_mouse.normalize()
        else:
            self.attack_direction = pygame.Vector2(1, 0)

    def setWeapon(self, weapon):
        self.weapon = weapon

    def add_xp(self, amount):
        '''adds amount of xp to the players current level, needs to be >= 0 and checks if the players level needs to be updated'''
        if amount >= 0:
            self.xp += amount
            self.update_level()

    def update_level(self):
        '''increases the players level by 1 level if he has more xp than required for the next level'''
        if self.xp >= self.xp_breakpoints[self.level + 1]:
            self.level += 1
            self.update_level() # in case more xp than 1 level is gained

    def get_level_progress(self) -> float:
        '''returns the percentage of the way of the players level to the next level, clamped between 0 and 1'''
        current_lvl = self.level
        current_lvl_xp = self.xp_breakpoints[current_lvl]
        next_lvl_xp = self.xp_breakpoints[current_lvl + 1]

        return max(0.0, min(1.0, (self.xp - current_lvl_xp) / max(1, (next_lvl_xp - current_lvl_xp))))