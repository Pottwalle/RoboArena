# arenaGame/rangedWeapon.py
import pygame
from weapon import Weapon
from projectile import ProjectileManager


class RangedWeapon(Weapon):
    """Basisklasse für Fernkampfwaffen (Bögen, Pistolen, Blaster, ...).

    Analog zu MeleeWeapon: Subklassen (z.B. eine "Bow"-Klasse, siehe
    club.py als Vorbild für MeleeWeapon) können das Aussehen/die konkreten
    Werte festlegen, indem sie super().__init__(...) mit den passenden
    Parametern aufrufen und optional _perform_attack()/draw() erweitern.

    Sobald der Cooldown abgelaufen ist, wird bei update() automatisch ein
    Projektil in Richtung ``owner.attack_direction`` abgefeuert. Die
    Bewegung/Kollision aller abgefeuerten Projektile übernimmt intern ein
    eigener ProjectileManager (siehe projectile.py), sodass RangedWeapon
    von außen weiterhin nur über die von Weapon vorgegebenen Methoden
    ``update(dt, targets)`` und ``draw(screen, camera)`` angesprochen
    werden muss - genau wie in game.py bereits für player.weapon üblich.
    """

    def __init__(self, owner, damage = 100, projectile_speed = 100, cooldown = 2,
                 projectile_range: float = 1000, projectile_radius: float = 4,
                 pierce: bool = False, spawn_offset: float = None,
                 magazine_size: int = None, reload_time: float = None,
                 projectile_color=(255, 210, 60)):
        """
        owner: Objekt mit .position (Vector2) und .attack_direction (Vector2)
        damage: Schaden pro Projektiltreffer
        projectile_speed: Geschwindigkeit der Projektile in Pixel/Sekunde
        cooldown: Sekunden zwischen zwei Schüssen
        projectile_range: maximale Flugdistanz eines Projektils in Pixel
        projectile_radius: Kollisionsradius eines Projektils
        pierce: falls True durchschlagen Projektile mehrere Ziele
        spawn_offset: Abstand vom Mittelpunkt des owners, an dem Projektile
            entstehen (Default: owner.r, damit sie nicht in der eigenen
            Hitbox spawnen und sich sofort selbst treffen)
        magazine_size: optionale Magazingröße; None = unbegrenzt Munition
        reload_time: Sekunden Nachladezeit, sobald das Magazin leer ist
        projectile_color: Farbe, mit der die Projektile gezeichnet werden
        """
        super().__init__(owner, cooldown)
        self.damage = damage
        self.projectile_speed = projectile_speed
        self.projectile_range = projectile_range
        self.projectile_radius = projectile_radius
        self.pierce = pierce
        self.spawn_offset = spawn_offset
        self.projectile_color = projectile_color

        # Munition / Nachladen (optional, magazine_size=None -> unendlich Munition)
        self.magazine_size = magazine_size
        self.reload_time = reload_time
        self.ammo = magazine_size
        self.reloading = False
        self._reload_timer = 0.0

        # jede RangedWeapon verwaltet ihre eigenen Projektile selbst, damit
        # sie wie MeleeWeapon eigenständig per update()/draw() nutzbar ist
        self.projectiles = ProjectileManager()

        # optional per set_movement() gesetzt, damit Projektile an soliden
        # Wänden stoppen; ohne movement fliegen sie ungehindert durch Wände
        self.movement = None

    def set_movement(self, movement):
        """Verbindet die Waffe mit dem Tilemap-Movement-System (siehe
        movement.py), damit abgefeuerte Projektile an Wänden kollidieren.

        Beispiel in game.py: ``player.weapon.set_movement(movement)``
        """
        self.movement = movement

    def update(self, dt: float, targets: list):
        self.time_since_last_attack += dt

        if self.magazine_size is not None:
            self._update_reload(dt)

        # nur schießen, wenn Cooldown abgelaufen und (falls Magazin genutzt
        # wird) noch Munition vorhanden ist
        if self.time_since_last_attack >= self.cooldown and self._can_fire():
            self._perform_attack()
            self.time_since_last_attack = 0.0

        # bereits fliegende Projektile unabhängig vom eigenen Cooldown jeden
        # Frame weiterbewegen & gegen targets kollidieren lassen; die
        # eigentliche (performante) Sammel-Verarbeitung übernimmt der
        # ProjectileManager in einem Durchgang
        self.projectiles.update(dt, targets, self.movement)

    def _can_fire(self) -> bool:
        if self.magazine_size is None:
            return True
        return not self.reloading and self.ammo > 0

    def _update_reload(self, dt: float):
        if self.ammo <= 0 and not self.reloading:
            self.reloading = True
            self._reload_timer = self.reload_time or 0.0

        if self.reloading:
            self._reload_timer -= dt
            if self._reload_timer <= 0:
                self.ammo = self.magazine_size
                self.reloading = False

    def _perform_attack(self):
        """Erzeugt ein neues Projektil in Blickrichtung des owners.

        Kann von Subklassen überschrieben werden, z.B. um mehrere
        Projektile gleichzeitig abzufeuern (Schrotflinten-Streuung) -
        siehe Club._perform_attack() als Vorbild aus MeleeWeapon.
        """
        direction = self.owner.attack_direction
        if direction.length_squared() == 0:
            return

        direction = direction.normalize()
        offset = self.spawn_offset if self.spawn_offset is not None else getattr(self.owner, "r", 0)
        spawn_pos = self.owner.position + direction * offset

        self.projectiles.spawn(
            spawn_pos.x, spawn_pos.y, direction,
            speed=self.projectile_speed,
            damage=self.damage,
            r=self.projectile_radius,
            max_range=self.projectile_range,
            owner=self.owner,
            pierce=self.pierce,
            color=self.projectile_color,
        )

        if self.magazine_size is not None:
            self.ammo -= 1

    def draw(self, screen, camera: pygame.Vector2):
        self.projectiles.draw(screen, camera)