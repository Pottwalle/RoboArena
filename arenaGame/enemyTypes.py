import pygame
import enemy
from weapon import Weapon
from rangedWeapon import RangedWeapon

class MeleeEnemy(enemy.Enemy):
    def __init__(self,x, y, movement,
                 r = 10,
                 alpha = 0,
                 base_speed = 20,
                 speed_modifier=1,
                 hp=10,
                 damage= 5,
                 movementType="aggressive",
                 xp_reward = 10, item_reward = [],
                 places_traps=False, trap_cooldown=4.0):
        super().__init__( x, y, r, alpha, base_speed, movement, speed_modifier, hp, damage, movementType, xp_reward, item_reward,
                 places_traps, trap_cooldown)


class RangedEnemy(enemy.Enemy):
    def __init__(self,x, y, movement,
                 r = 10,
                 alpha = 0,
                 base_speed = 60,
                 speed_modifier=1,
                 hp=5,
                 damage= 5,
                 movementType="passive",
                 xp_reward = 10, item_reward = [],
                 places_traps=False, trap_cooldown=4.0):
        super().__init__( x, y, r, alpha, base_speed, movement, speed_modifier, hp, damage, movementType, xp_reward, item_reward,
                 places_traps, trap_cooldown)

class TrapperEnemy(enemy.Enemy):
    def __init__(self,x, y, movement,
                 r = 10,
                 alpha = 0,
                 base_speed = 40,
                 speed_modifier=1,
                 hp=10,
                 damage= 5,
                 movementType="random",
                 xp_reward = 10, item_reward = [],
                 places_traps=True, trap_cooldown=4.0):
        super().__init__( x, y, r, alpha, base_speed, movement, speed_modifier, hp, damage, movementType, xp_reward, item_reward,
                 places_traps, trap_cooldown)