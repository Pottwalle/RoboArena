# arenaGame/projectile.py
import pygame


class Projectile:
    """Repräsentiert ein einzelnes Projektil (Pfeil, Kugel, Energieblitz, ...).

    Bewegt sich geradlinig mit konstanter Geschwindigkeit in eine feste
    Richtung. Verhält sich wie Player/Enemy/Interactable als Kreis-Hitbox
    (``.position`` als pygame.Vector2 und ``.r`` als Radius), damit es sich
    z.B. auch mit ObjectCollision kombinieren ließe.

    Attributes:
        position: aktuelle Weltposition (pygame.Vector2)
        direction: normalisierte Flugrichtung (pygame.Vector2)
        speed: Geschwindigkeit in Pixel/Sekunde
        damage: Schaden, der bei einem Treffer abgezogen wird
        r: Kollisionsradius des Projektils
        max_range: maximale Flugdistanz in Pixel, danach verschwindet es
        owner: Objekt, das das Projektil abgefeuert hat (verhindert Self-Hit)
        pierce: falls True durchschlägt das Projektil mehrere Ziele, statt
            nach dem ersten Treffer zu verschwinden
        active: solange True wird das Projektil bewegt/gezeichnet/geprüft
    """

    def __init__(self, x, y, direction: pygame.Vector2, speed: float, damage: float,
                 r: float = 4, max_range: float = 600, owner=None,
                 pierce: bool = False, color="red"):
        self.position = pygame.Vector2(x, y)

        # Richtung normalisieren, damit "speed" wirklich in px/s der Flugbahn
        # entspricht, egal wie der Richtungsvektor übergeben wurde
        if direction.length_squared() > 0:
            self.direction = pygame.Vector2(direction).normalize()
        else:
            self.direction = pygame.Vector2(1, 0)

        self.speed = speed
        self.damage = damage
        self.r = r
        self.max_range = max_range
        self.owner = owner
        self.pierce = pierce
        self.color = color

        self.active = True
        self._traveled = 0.0  # bereits zurückgelegte Distanz, für max_range

    def update(self, dt: float, movement=None):
        """Bewegt das Projektil einen Frame weiter.

        Args:
            dt: delta time
            movement: optionales Movement-Objekt (siehe movement.py), um
                Kollision mit soliden Tiles (Wänden) zu prüfen. Ohne movement
                fliegt das Projektil ungehindert durch Wände.
        """
        if not self.active:
            return

        step = self.speed * dt
        self.position += self.direction * step
        self._traveled += step

        if self._traveled >= self.max_range:
            self.active = False
            return

        # an einer soliden Wand einschlagen und verschwinden
        if movement is not None and movement.handleCollision(self.position, self.r):
            self.active = False

    def try_hit(self, target) -> bool:
        """Prüft per Kreis-Distanz, ob das Projektil ``target`` trifft, und
        wendet bei einem Treffer sofort Schaden an.

        Nutzt bewusst ``length_squared()`` statt ``length()``, um die teure
        Wurzelberechnung zu sparen (wichtig bei vielen gleichzeitig aktiven
        Projektilen/Zielen).

        Args:
            target: Objekt mit ``.position`` (Vector2) und optional ``.r``,
                sowie ``.health`` (Enemy) oder ``.hp / .stats.take_damage`` (Player)

        Returns:
            bool: True, wenn ein Treffer stattgefunden hat.
        """
        if not self.active or target is self.owner:
            return False

        to_target = target.position - self.position
        min_dist = self.r + getattr(target, "r", 0)

        if to_target.length_squared() > min_dist ** 2:
            return False

        if hasattr(target, "stats"):
            target.stats.take_damage(self.damage)
        elif hasattr(target, "health"):
            target.health -= self.damage
        elif hasattr(target, "hp"):
            target.hp -= self.damage
        else:
            return False

        if not self.pierce:
            self.active = False

        return True

    def draw(self, screen, camera: pygame.Vector2):
        if not self.active:
            return
        screen_position = self.position - camera
        pygame.draw.circle(screen, self.color, screen_position, self.r)
        pygame.draw.circle(screen, (0, 0, 0), screen_position, self.r, 1)


class ProjectileManager:
    """Verwaltet alle aktiven Projektile einer Waffe (oder global der Arena).

    Übernimmt das Erzeugen neuer Projektile (``spawn``) sowie das performante
    Aktualisieren/Kollidieren/Zeichnen einer potenziell großen Anzahl
    gleichzeitig aktiver Projektile in jeweils einem Durchgang.

    Analog zu InteractableManager gedacht, z.B.::

        projectiles = ProjectileManager()
        projectiles.spawn(x, y, direction, speed=500, damage=8, owner=player)
        ...
        projectiles.update(dt, enemies, movement)
        projectiles.draw(screen, camera)
    """

    def __init__(self):
        self.projectiles: list[Projectile] = []

    def spawn(self, x, y, direction: pygame.Vector2, speed: float, damage: float,
               r: float = 4, max_range: float = 600, owner=None,
               pierce: bool = False, color=(255, 210, 60)) -> Projectile:
        """Erzeugt ein neues Projektil und fügt es der Verwaltung hinzu."""
        projectile = Projectile(
            x, y, direction, speed, damage,
            r=r, max_range=max_range, owner=owner, pierce=pierce, color=color,
        )
        self.projectiles.append(projectile)
        return projectile

    def update(self, dt: float, targets: list, movement=None):
        """Bewegt & kollidiert alle aktiven Projektile in einem Durchgang und
        entfernt anschließend alle inaktiv gewordenen (abgelaufen / an Wand
        eingeschlagen / getroffen) Projektile.

        Args:
            dt: delta time
            targets: Liste möglicher Treffer-Ziele (z.B. enemies oder [player])
            movement: optionales Movement-Objekt für Wand-Kollision
        """
        if not self.projectiles:
            return

        for projectile in self.projectiles:
            if not projectile.active:
                continue

            projectile.update(dt, movement)

            if not projectile.active:
                continue

            for target in targets:
                if projectile.try_hit(target) and not projectile.pierce:
                    break  # Projektil ist jetzt inaktiv, weitere Ziele lohnen nicht

        # inaktive Projektile in einem Rutsch entfernen; bei vielen
        # kurzlebigen Projektilen schneller als einzelne remove()-Aufrufe
        self.projectiles = [p for p in self.projectiles if p.active]

    def draw(self, screen, camera: pygame.Vector2):
        for projectile in self.projectiles:
            projectile.draw(screen, camera)

    def clear(self):
        """Entfernt alle aktuell aktiven Projektile (z.B. bei Levelwechsel)."""
        self.projectiles.clear()

    def __len__(self):
        return len(self.projectiles)