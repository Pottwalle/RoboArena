
class ObjectCollision:
    """Detects and resolves collisions between circular game objects.

    All game objects (Player, Enemy) use a circle as their hitbox,
    defined by ``obj.position`` (pygame.Vector2) and ``obj.r`` (radius).

    Typical usage (in the game loop)::

        collision = ObjectCollision()
        collision.handle_player_enemy(player, enemies)
        collision.handle_enemy_enemy(enemies)
    """

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

    @staticmethod
    def separate(a, b, ratio_a: float = 0.5, ratio_b: float = 0.5):
        """Push two overlapping objects apart along their connecting axis.

        ``ratio_a + ratio_b`` should equal 1.0.  Pass ``ratio_a=0`` and
        ``ratio_b=1`` to move only *b* (e.g. when *a* is the player and
        should not be displaced by enemies).

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
