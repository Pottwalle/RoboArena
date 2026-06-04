# arenaGame/weapon.py
import math
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
        targets: Liste von Objekten mit .position und .health (z.B. Enemy)
        """
        self.time_since_last_attack += dt

        # Default: nichts tun – konkrete Waffen implementieren Logik
        # (MeleeWeapon wird das überschreiben)
        pass

    def draw(self, screen, camera: pygame.Vector2):
        """
        Optionale Visualisierung der Waffe.
        """
        pass
