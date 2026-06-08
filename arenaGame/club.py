# club.py
import pygame
import math
from meleeWeapon import MeleeWeapon

class Club(MeleeWeapon):
    def __init__(self, owner):
        super().__init__(
            owner=owner,
            damage=2,
            attack_range=60,
            cone_angle_deg=60,
            cooldown=0.8,
        )
        self.show_cone = 0.0
        self.cone_visible_time = 0.12  # 120 ms sichtbar

    def _perform_attack(self, targets):
        super()._perform_attack(targets)
        self.show_cone = self.cone_visible_time

    def draw(self, screen, camera):
        if self.show_cone <= 0:
            return

        origin = self.owner.position - camera

        # Richtung bestimmen
        dir_vec = self.owner.direction
        if dir_vec.length_squared() == 0:
            rad = math.radians(self.owner.alpha)
            dir_vec = pygame.Vector2(math.cos(rad), -math.sin(rad))

        facing = dir_vec.normalize()

        # Kegel berechnen
        half_angle = self.cone_angle_rad / 2

        left_dir = facing.rotate_rad(-half_angle)
        right_dir = facing.rotate_rad(+half_angle)

        p0 = origin
        p1 = origin + left_dir * self.attack_range
        p2 = origin + right_dir * self.attack_range

        # Kegel zeichnen
        pygame.draw.polygon(
            screen,
            (255, 0, 0, 80),  # halbtransparent rot
            [p0, p1, p2]
        )
