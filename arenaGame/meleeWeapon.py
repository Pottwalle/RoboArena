# arenaGame/melee_weapon.py
import math
from weapon import Weapon


class MeleeWeapon(Weapon):
    def __init__(self, owner, damage: float, attack_range: float,
                 cone_angle_deg: float, cooldown: float):
        super().__init__(owner, cooldown)
        self.damage = damage
        self.damage_bonus = 0
        self.attack_range = attack_range
        self.attack_range_bonus = 0
        self.cone_angle_rad = math.radians(cone_angle_deg)
        self.cone_angle_rad_bonus = 0

        # Precompute cos of half the cone angle for efficient hit detection
        self._cos_half_cone = math.cos(self.cone_angle_rad / 2)

    def update(self, dt: float, targets: list):
        self.time_since_last_attack += dt
        self.show_cone = max(0, self.show_cone -dt)

        # attack only if cooldown is ready
        if self.time_since_last_attack >= self.cooldown + self.cooldown_reduction:
            self._perform_attack(targets)
            self.time_since_last_attack = 0.0
    
    def update_stats(self):
        '''updates the weapon stats according to the equipment'''
        self.damage_bonus = self.owner.stats.get("damage")
        self.attack_range_bonus = self.owner.stats.get("attack_range")
        self.cone_angle_rad_bonus = math.radians(self.owner.stats.get("cone_angle_deg"))
        super().update_stats()

    def _perform_attack(self, targets: list):
        origin = self.owner.position
        dir_vec = self.owner.attack_direction

        if dir_vec.length_squared() == 0:
            return

        facing = dir_vec.normalize()

        for target in targets:
            # prevent self-hit
            if target is self.owner:
                continue

            to_target = target.position - origin
            dist_sq = to_target.length_squared()

            if dist_sq > (self.attack_range + self.attack_range_bonus) ** 2:
                continue

            if dist_sq == 0:
                continue

            to_target_norm = to_target.normalize()
            dot = facing.dot(to_target_norm)

            # compare directly with cos
            if dot >= self._cos_half_cone:
                # Treffer
                if hasattr(target, "hp"):
                    target.hp -= (self.damage + self.damage_bonus)
                    # Optional: Debug
                    # print(f"Hit {target} for {self.damage} damage")
