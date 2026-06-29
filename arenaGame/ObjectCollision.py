import pygame
import math
class ObjectCollision:
    """Detects and resolves collisions between circular game objects.

    All game objects (Player, Enemy) use a circle as their hitbox,
    defined by ``obj.position`` (pygame.Vector2) and ``obj.r`` (radius).

    Typical usage (in the game loop)::

        collision = ObjectCollision(arena.grid)
        collision.handle_player_enemy(player, enemies)
        collision.handle_enemy_enemy(enemies)
    """

    def __init__(self, tilemap=None):
        """
        Args:
            tilemap: optionales 2D-Tile-Grid (z.B. ``arena.grid``), das genutzt
                wird, um Objekte nach einer Separation aus soliden Tiles
                (Wänden) herauszuschieben. Ohne tilemap wird nur die
                Kreis-zu-Kreis-Separation durchgeführt, ohne Wand-Korrektur.
        """
        self.tilemap = tilemap

    # ------------------------------------------------------------------ #
    #  Core helper                                                         #
    # ------------------------------------------------------------------ #

    @staticmethod
    def circles_overlap(a, b) -> bool:
        """Return True when two circular objects overlap.

        Args:
            a: any object with ``.position`` (Vector2) and ``.r`` (float)
            b: any object with ``.position`` (Vector2) and ``.r`` (float)

        Returns:
            bool: True if the circles overlap, False otherwise.
        """
        distance_sq = (a.position - b.position).length_squared()
        min_distance = a.r + b.r
        return distance_sq < min_distance ** 2

    @staticmethod
    def get_overlap(a, b) -> float:
        """Return the penetration depth between two circular objects.

        A positive value means the circles overlap by that many pixels.
        Zero or a negative value means they are not touching.

        Args:
            a: object with ``.position`` and ``.r``
            b: object with ``.position`` and ``.r``

        Returns:
            float: penetration depth (positive = overlap, negative = gap).
        """
        distance = (a.position - b.position).length()
        return (a.r + b.r) - distance

    # ------------------------------------------------------------------ #
    #  Separation (push-apart)                                            #
    # ------------------------------------------------------------------ #

    def separate(self, a, b, ratio_a: float = 0.5, ratio_b: float = 0.5):
        """Push two overlapping objects apart along their connecting axis.

        ``ratio_a + ratio_b`` should equal 1.0.  Pass ``ratio_a=0`` and
        ``ratio_b=1`` to move only *b* (e.g. when *a* is the player and
        should not be displaced by enemies).

        Falls eine tilemap übergeben wurde, wird jedes verschobene Objekt
        (ratio > 0) danach zusätzlich per ``find_safe_position`` aus
        soliden Tiles herausgeschoben, damit der reine Kreis-Push nicht
        in eine Wand hineinschieben kann.

        Args:
            a: object with ``.position`` and ``.r``
            b: object with ``.position`` and ``.r``
            ratio_a: fraction of the correction applied to *a* (default 0.5)
            ratio_b: fraction of the correction applied to *b* (default 0.5)
        """
        delta = b.position - a.position
        dist = delta.length()

        if dist == 0:
            # Exactly on top of each other – push b in a fixed direction
            delta = pygame.Vector2(1, 0)
            dist = 1.0

        overlap = (a.r + b.r) - dist
        if overlap <= 0:
            return

        push = delta.normalize() * overlap
        a.position -= push * ratio_a
        b.position += push * ratio_b

        if self.tilemap is not None:
            if ratio_a > 0:
                a.position = self.find_safe_position(a.position, a.r)
            if ratio_b > 0:
                b.position = self.find_safe_position(b.position, b.r)

    # ------------------------------------------------------------------ #
    #  Wand-Korrektur (sichere Position außerhalb solider Tiles)          #
    # ------------------------------------------------------------------ #

    def _get_overlapping_solid_tiles(self, pos, radius):
        """Liefert alle soliden Tiles, deren Rect mit der AABB von
        ``pos``/``radius`` überlappt (gleiche AABB-Logik wie ``Movement``)."""
        obj_rect = pygame.Rect(pos.x - radius, pos.y - radius, radius * 2, radius * 2)
        tiles = []
        for row in self.tilemap:
            for tile in row:
                if tile.solid and tile.rect.colliderect(obj_rect):
                    tiles.append(tile)
        return tiles

    @staticmethod
    def _mtv_out_of_tile(pos, radius, tile_rect: pygame.Rect) -> pygame.Vector2:
        """Berechnet den minimalen Verschiebungsvektor (Minimum Translation
        Vector), um die AABB von ``pos``/``radius`` aus ``tile_rect``
        herauszuschieben (kürzeste Strecke entlang X oder Y).
        """
        obj_rect = pygame.Rect(pos.x - radius, pos.y - radius, radius * 2, radius * 2)

        # Überlappung auf beiden Achsen
        overlap_x = min(obj_rect.right, tile_rect.right) - max(obj_rect.left, tile_rect.left)
        overlap_y = min(obj_rect.bottom, tile_rect.bottom) - max(obj_rect.top, tile_rect.top)

        if overlap_x <= 0 or overlap_y <= 0:
            return pygame.Vector2(0, 0)

        # entlang der Achse mit der geringeren Überlappung herausschieben
        if overlap_x < overlap_y:
            direction = 1 if obj_rect.centerx >= tile_rect.centerx else -1
            return pygame.Vector2(direction * overlap_x, 0)
        else:
            direction = 1 if obj_rect.centery >= tile_rect.centery else -1
            return pygame.Vector2(0, direction * overlap_y)

    def find_safe_position(self, pos: pygame.Vector2, radius: float,
                            max_iterations: int = 8,
                            spiral_search_step: float = 4.0,
                            spiral_max_radius: float = None) -> pygame.Vector2:
        """Findet die nächste "sichere" Position außerhalb aller soliden Tiles.

        Schiebt ``pos`` iterativ per Minimum-Translation-Vector aus jedem
        überlappenden soliden Tile heraus (löst auch Überlappungen mit
        mehreren/diagonal angeordneten Tiles zuverlässig auf). Falls das
        nach ``max_iterations`` Versuchen nicht konvergiert (z.B. weil das
        Objekt komplett in einer Wandmasse feststeckt), wird als Fallback
        spiralförmig nach der nächstgelegenen freien Position gesucht.

        Args:
            pos: aktuelle (ggf. überlappende) Position
            radius: Radius/Hitbox-Größe des Objekts
            max_iterations: maximale Anzahl an MTV-Korrekturschritten
            spiral_search_step: Schrittweite der Fallback-Spiralsuche in Pixel
            spiral_max_radius: maximaler Suchradius der Spirale (Default:
                ``20 * radius``)

        Returns:
            pygame.Vector2: korrigierte Position, garantiert kollisionsfrei
            mit soliden Tiles, sofern eine freie Stelle innerhalb des
            Suchradius existiert; sonst die best mögliche (am wenigsten
            überlappende) gefundene Position.
        """
        if self.tilemap is None:
            return pos

        safe_pos = pygame.Vector2(pos)

        # --- 1) iterative MTV-Korrektur gegen alle aktuell überlappten Tiles ---
        for _ in range(max_iterations):
            colliding_tiles = self._get_overlapping_solid_tiles(safe_pos, radius)
            if not colliding_tiles:
                return safe_pos

            # pro Iteration nur die größte (dringendste) Korrektur anwenden,
            # damit sich mehrere Tiles nicht gegenseitig aufheben
            best_mtv = None
            best_len_sq = -1
            for tile in colliding_tiles:
                mtv = self._mtv_out_of_tile(safe_pos, radius, tile.rect)
                len_sq = mtv.length_squared()
                if len_sq > best_len_sq:
                    best_len_sq = len_sq
                    best_mtv = mtv

            if best_mtv is None or best_len_sq == 0:
                break

            safe_pos += best_mtv

        # --- 2) Fallback: spiralförmige Suche nach der nächsten freien Stelle ---
        if not self._get_overlapping_solid_tiles(safe_pos, radius):
            return safe_pos

        return self._spiral_search_free_position(
            pygame.Vector2(pos), radius, spiral_search_step, spiral_max_radius
        )

    def _spiral_search_free_position(self, origin: pygame.Vector2, radius: float,
                                      step: float, max_radius: float = None) -> pygame.Vector2:
        """Sucht spiralförmig um ``origin`` nach der nächstgelegenen Position,
        die mit keinem soliden Tile überlappt. Wird nur als Fallback genutzt,
        wenn die iterative MTV-Korrektur nicht konvergiert ist.
        """
        if max_radius is None:
            max_radius = radius * 20

        if not self._get_overlapping_solid_tiles(origin, radius):
            return origin

        # archimedische Spirale: Radius wächst kontinuierlich mit dem Winkel,
        # Winkel-Schrittweite klein genug, um keine Stelle zu überspringen
        angle = 0.0
        angle_step = math.radians(20)
        current_radius = step

        while current_radius <= max_radius:
            candidate = origin + pygame.Vector2(
                math.cos(angle) * current_radius,
                math.sin(angle) * current_radius
            )
            if not self._get_overlapping_solid_tiles(candidate, radius):
                return candidate

            angle += angle_step
            if angle >= 2 * math.pi:
                angle = 0.0
                current_radius += step

        # keine freie Stelle im Suchradius gefunden -> Ausgangsposition zurückgeben
        return origin

    # ------------------------------------------------------------------ #
    #  High-level helpers                                                  #
    # ------------------------------------------------------------------ #

    def handle_player_enemy(self, player, enemies: list,
                            damage_on_contact: bool = True,
                            contact_damage: float = None) -> list:
        """Check collisions between the player and every enemy.

        By default the player is pushed away from each enemy (enemies are
        not moved, so they don't interfere with their own AI movement).
        Optionally, enemies deal contact damage to the player.

        Args:
            player: the Player object
            enemies: list of Enemy objects
            damage_on_contact: if True, touching enemies reduce player HP.
            contact_damage: damage per collision (uses enemy.damage if None).

        Returns:
            list[Enemy]: enemies that are currently touching the player.
        """
        touching = []
        for enemy in enemies:
            if self.circles_overlap(player, enemy):
                touching.append(enemy)
                # push only the player away (ratio_a=1, ratio_b=0)
                self.separate(player, enemy, ratio_a=1.0, ratio_b=0.0)

                if damage_on_contact:
                    dmg = contact_damage if contact_damage is not None else getattr(enemy, "damage", 0)
                    if dmg:
                        player.hp -= dmg

        return touching

    def handle_enemy_enemy(self, enemies: list):
        """Prevent enemies from overlapping each other.

        Each pair is pushed apart equally (50 / 50 split).

        Args:
            enemies: list of Enemy objects
        """
        for i in range(len(enemies)):
            for j in range(i + 1, len(enemies)):
                if self.circles_overlap(enemies[i], enemies[j]):
                    self.separate(enemies[i], enemies[j], ratio_a=0.5, ratio_b=0.5)

    def handle_any(self, objects_a: list, objects_b: list,
                   ratio_a: float = 0.5, ratio_b: float = 0.5) -> list:
        """Generic collision detection between two arbitrary object lists.

        Each object must have a ``.position`` (Vector2) and ``.r`` (float).

        Args:
            objects_a: first group of objects
            objects_b: second group of objects
            ratio_a: push fraction for objects in *objects_a*
            ratio_b: push fraction for objects in *objects_b*

        Returns:
            list[tuple]: every (a, b) pair that was found to overlap.
        """
        collisions = []
        for a in objects_a:
            for b in objects_b:
                if a is not b and self.circles_overlap(a, b):
                    collisions.append((a, b))
                    self.separate(a, b, ratio_a=ratio_a, ratio_b=ratio_b)
        return collisions

