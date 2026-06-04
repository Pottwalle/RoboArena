# arenaGame/weapon.py
import pygame


class Weapon:
    def __init__(self, owner, cooldown: float):
        """
        owner: Objekt mit .position (Vector2) und .direction (Vector2)
        cooldown: Sekunden zwischen zwei Angriffen
        """
        self.owner = owner
        self.cooldown = cooldown
        self.time_since_last_attack = cooldown  # direkt bereit

    def update(self, dt: float, targets: list):
        """
        dt: delta time
        targets: list of enemmies to hit 
        """
        self.time_since_last_attack += dt

        # Default: specialised weapon implement update, here is nothing more
        # (MeleeWeapon wird das überschreiben)
        pass

    def draw(self, screen, camera: pygame.Vector2):
        """
        optional visualisiation of the weapon
        """
        pass
