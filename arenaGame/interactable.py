import pygame
import math
import random

class Interactable:
    """Basisklasse für alle interagierbaren Objekte in der Arena (z.B. Health Packs, Fallen).

    Ein Interactable verhält sich wie Player/Enemy als Kreis-Hitbox
    (``.position`` als pygame.Vector2 und ``.r`` als Radius), damit es direkt
    mit ``ObjectCollision`` bzw. einfachen Kreis-Überlappungs-Checks kompatibel ist.

    Sowohl der Spieler als auch Gegner können Interactables zur Laufzeit
    platzieren, siehe :class:`InteractableManager`.

    Attributes:
        position: Weltposition des Objekts (pygame.Vector2)
        r: Radius der Kollisions-/Trigger-Fläche
        active: solange True wird das Objekt aktualisiert/gezeichnet/kollidiert
        lifetime: optionale Lebensdauer in Sekunden (None = unbegrenzt haltbar)
        owner: wer das Objekt platziert hat ("player", "enemy", None, ...),
            nützlich um z.B. Freundschaftliches-Feuer-Regeln umzusetzen
    """

    def __init__(self, x, y, r=12, lifetime=None, owner=None):
        self.position = pygame.Vector2(x, y)
        self.r = r
        self.active = True
        self.lifetime = lifetime
        self._age = 0.0
        self.owner = owner

    def update(self, dt, player, enemies):
        """Aktualisiert das Objekt; wertet Lebensdauer aus und kann von
        Subklassen erweitert werden (z.B. Trigger-Logik)."""
        if self.lifetime is not None:
            self._age += dt
            if self._age >= self.lifetime:
                self.active = False

    def draw(self, screen, camera):
        """Optionale Visualisierung, wird von Subklassen überschrieben."""
        pass

    def try_interact(self, entity) -> bool:
        """Wird aufgerufen, wenn ``entity`` (Player oder Enemy) das Objekt berührt.

        Args:
            entity: Objekt mit ``.position`` und ``.r`` (z.B. Player oder Enemy)

        Returns:
            bool: True, wenn das Objekt danach entfernt werden soll
        """
        return False

    def is_colliding_with(self, entity) -> bool:
        """Prüft per Kreis-Distanz, ob ``entity`` das Interactable berührt."""
        distance_sq = (self.position - entity.position).length_squared()
        min_distance = self.r + getattr(entity, "r", 0)
        return distance_sq < min_distance ** 2


class HealthPack(Interactable):
    """Heilt die berührende Einheit einmalig und wird danach entfernt.

    Kann sowohl vom Spieler für sich selbst, als auch (theoretisch) von
    Gegnern zur Selbstheilung platziert werden.
    """

    def __init__(self, x, y, heal_amount=25, lifetime=None, owner=None):
        super().__init__(x, y, r=10, lifetime=lifetime, owner=owner)
        self.heal_amount = heal_amount

    def try_interact(self, entity) -> bool:
        if not self.is_colliding_with(entity):
            return False

        # heilt nur Einheiten mit hp/max_hp (Player) oder health/max_health (Enemy);
        # bei vollen Lebenspunkten bleibt das Pack liegen, statt wirkungslos zu verschwinden
        if hasattr(entity, "hp") and hasattr(entity, "max_hp"):
            if entity.hp >= entity.max_hp:
                return False
            entity.hp = min(entity.max_hp, entity.hp + self.heal_amount)
            return True
        if hasattr(entity, "health") and hasattr(entity, "max_health"):
            if entity.health >= entity.max_health:
                return False
            entity.health = min(entity.max_health, entity.health + self.heal_amount)
            return True
        return False

    def draw(self, screen, camera):
        if not self.active:
            return
        screen_position = self.position - camera

        # weißer Kreis mit grünem Kreuz als Health-Pack-Symbol
        pygame.draw.circle(screen, (255, 255, 255), screen_position, self.r)
        pygame.draw.circle(screen, (40, 160, 40), screen_position, self.r, 2)

        cross_half = self.r * 0.5
        x, y = screen_position.x, screen_position.y
        pygame.draw.line(screen, (40, 160, 40), (x - cross_half, y), (x + cross_half, y), 3)
        pygame.draw.line(screen, (40, 160, 40), (x, y - cross_half), (x, y + cross_half), 3)


class Trap(Interactable):
    """Fügt der berührenden Einheit Schaden zu.

    Standardmäßig nur einmal auslösbar (``single_use=True``); kann alternativ
    mit einem Trigger-Cooldown wiederverwendbar gemacht werden, z.B. um
    dauerhafte Gefahrenzonen zu bauen.
    """

    def __init__(self, x, y, damage=15, lifetime=None, owner=None,
                 single_use=True, trigger_cooldown=1.0, friendly_fire=False):
        super().__init__(x, y, r=14, lifetime=lifetime, owner=owner)
        self.damage = damage
        self.single_use = single_use
        self.trigger_cooldown = trigger_cooldown
        self._cooldown_remaining = 0.0
        # falls False, löst die Falle bei der gleichen "Seite" (z.B. eine von
        # einem Gegner gelegte Falle bei einem anderen Gegner) nicht aus
        self.friendly_fire = friendly_fire

    def update(self, dt, player, enemies):
        super().update(dt, player, enemies)
        if self._cooldown_remaining > 0:
            self._cooldown_remaining -= dt

    def _is_friendly(self, entity) -> bool:
        """True, wenn ``entity`` zur selben 'Seite' gehört wie der Falleneigner
        und friendly_fire deaktiviert ist (Falle löst dann nicht aus)."""
        if self.friendly_fire or self.owner is None:
            return False
        entity_side = "player" if entity.__class__.__name__ == "Player" else "enemy"
        return entity_side == self.owner

    def try_interact(self, entity) -> bool:
        if self._is_friendly(entity):
            return False
        if not self.is_colliding_with(entity):
            return False
        if self._cooldown_remaining > 0:
            return False

        # Schaden anwenden: Player nutzt hp, Enemy nutzt health
        applied = False
        if hasattr(entity, "hp"):
            entity.hp -= self.damage
            applied = True
        elif hasattr(entity, "health"):
            entity.health -= self.damage
            applied = True

        if not applied:
            return False

        if self.single_use:
            return True

        self._cooldown_remaining = self.trigger_cooldown
        return False

    def draw(self, screen, camera):
        if not self.active:
            return
        screen_position = self.position - camera

        # dunkelrotes Dreieck/Warnsymbol als Fallen-Markierung
        points = [
            (screen_position.x, screen_position.y - self.r),
            (screen_position.x - self.r, screen_position.y + self.r * 0.7),
            (screen_position.x + self.r, screen_position.y + self.r * 0.7),
        ]
        color = (150, 0, 0) if self._cooldown_remaining <= 0 else (90, 90, 90)
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, (0, 0, 0), points, 2)

        # Ausrufezeichen
        x, y = screen_position.x, screen_position.y
        pygame.draw.line(screen, (255, 255, 255), (x, y - self.r * 0.5), (x, y + self.r * 0.05), 2)
        pygame.draw.circle(screen, (255, 255, 255), (x, y + self.r * 0.35), 1.5)


class InteractableManager:
    """Verwaltet sämtliche Interactables (Health Packs, Fallen, ...) der Arena.

    Übernimmt das Platzieren zur Laufzeit (durch Spieler oder Gegner),
    das Aktualisieren/Zeichnen sowie die Kollisionsauflösung mit Spieler
    und Gegnern. Wird analog zu ``ObjectCollision`` einmal in ``game.py``
    erzeugt und in der Game-Loop verwendet.

    Beispiel::

        interactables = InteractableManager()
        interactables.spawn_health_pack(player.position.x, player.position.y)
        ...
        interactables.update(dt, player, enemies)
        interactables.draw(screen, camera)
    """

    def __init__(self):
        self.items: list[Interactable] = []

    # ------------------------------------------------------------------ #
    #  Platzieren (Spieler & Gegner)                                      #
    # ------------------------------------------------------------------ #

    def spawn_health_pack(self, x, y, heal_amount=25, lifetime=None, owner=None) -> HealthPack:
        """Platziert ein Health Pack an Position (x, y).

        Kann sowohl vom Spieler (z.B. über eine Tastenbindung) als auch von
        Gegnern (z.B. als Drop) aufgerufen werden.
        """
        pack = HealthPack(x, y, heal_amount=heal_amount, lifetime=lifetime, owner=owner)
        self.items.append(pack)
        return pack

    def spawn_trap(self, x, y, damage=15, lifetime=None, owner=None,
                   single_use=True, trigger_cooldown=1.0, friendly_fire=False) -> Trap:
        """Platziert eine Falle an Position (x, y).

        Kann sowohl vom Spieler als auch von Gegnern (z.B. automatisch mit
        Cooldown) aufgerufen werden.
        """
        trap = Trap(x, y, damage=damage, lifetime=lifetime, owner=owner,
                    single_use=single_use, trigger_cooldown=trigger_cooldown,
                    friendly_fire=friendly_fire)
        self.items.append(trap)
        return trap

    def spawn_at_entity(self, kind: str, entity, offset=0, owner=None, **kwargs) -> Interactable:
        """Platziert ein Interactable relativ zur Position/Blickrichtung von ``entity``
        (Player oder Enemy). ``offset`` verschiebt die Platzierung in Blickrichtung
        (0 = genau auf der Einheit, >0 = vor ihr in Blickrichtung).

        Args:
            kind: "health_pack" oder "trap"
            entity: Player oder Enemy, von dem aus platziert wird
            offset: Abstand in Pixel in Blickrichtung der Einheit
            owner: wer das Objekt platziert hat, z.B. "player" oder "enemy";
                wird automatisch aus dem Klassennamen abgeleitet, falls None
        """
        spawn_pos = pygame.Vector2(entity.position)
        if offset:
            direction = getattr(entity, "direction", None)
            if direction and direction.length_squared() > 0:
                spawn_pos += direction.normalize() * offset
            else:
                rad = math.radians(getattr(entity, "alpha", 0))
                spawn_pos += pygame.Vector2(math.cos(rad), -math.sin(rad)) * offset

        if owner is None:
            owner = "player" if entity.__class__.__name__ == "Player" else "enemy"

        if kind == "health_pack":
            return self.spawn_health_pack(spawn_pos.x, spawn_pos.y, owner=owner, **kwargs)
        elif kind == "trap":
            return self.spawn_trap(spawn_pos.x, spawn_pos.y, owner=owner, **kwargs)
        else:
            raise ValueError(f"Unbekannter Interactable-Typ: {kind}")

    # ------------------------------------------------------------------ #
    #  Update / Draw / Kollision                                          #
    # ------------------------------------------------------------------ #

    def update(self, dt, player, enemies,arena):
        """Aktualisiert alle Interactables, prüft Kollisionen mit Spieler &
        Gegnern und entfernt verbrauchte/abgelaufene Objekte."""
        for item in self.items:
            item.update(dt, player, enemies)

            if not item.active:
                continue

            # Kollision mit Spieler
            if item.try_interact(player):
                item.active = False
                continue

            # Kollision mit Gegnern
            for enemy in enemies:
                if item.try_interact(enemy):
                    item.active = False
                    break

        # abgelaufene / verbrauchte Objekte entfernen
        self.items = [item for item in self.items if item.active]

        # weitere healthpacks spawnen

        if sum(1 for item in self.items if isinstance(item, HealthPack))<=4:
            pos = arena.get_random_tile_positions("dirt", count=1)
            self.spawn_health_pack(pos[0].x, pos[0].y)

    def draw(self, screen, camera):
        for item in self.items:
            item.draw(screen, camera)

    def clear(self):
        """Entfernt alle aktuell platzierten Interactables (z.B. bei Levelwechsel)."""
        self.items.clear()
