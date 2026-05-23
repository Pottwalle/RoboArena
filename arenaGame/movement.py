import pygame


class Movement:
    def __init__(self, tilemap):
        self.tilemap = tilemap

    def move(self, player, dt):
        pos = player.position
        direction = player.direction
        radius = player.r

        velocity = player.velocity
        acceleration = player.acceleration
        max_speed = player.max_speed
        friction = player.friction

        # --- Tile Speed Modifier ---
        speed_mod = self.handleMoveSpeed(pos, radius)

        # --- Beschleunigung ---
        if direction.length() > 0:
            dir_norm = direction.normalize()

            # Richtungswechsel abbremsen
            if velocity.length() > 0:
                vel_dir = velocity.normalize()
                if vel_dir.dot(dir_norm) < 0:
                    velocity *= 0.5

            # Beschleunigung (inkl. Tile-Speed)
            velocity += dir_norm * acceleration * speed_mod * dt

        # --- Max Speed ---
        if velocity.length() > max_speed * speed_mod:
            velocity = velocity.normalize() * max_speed * speed_mod

        # --- Reibung ---
        velocity *= friction

        # --- Bewegung ---
        new_pos = pos + velocity * dt

        # --- Kollision ---
        if self.handleCollision(new_pos, radius):
            # bei Kollision Geschwindigkeit stoppen
            velocity = pygame.Vector2(0, 0)
            player.velocity = velocity
            return pos

        # Velocity zurückspeichern
        player.velocity = velocity
        return new_pos

    def handleCollision(self, pos, radius):
        player_rect = pygame.Rect(pos.x - radius, pos.y - radius, radius*2, radius*2)

        for row in self.tilemap:
            for tile in row:
                if tile.solid and tile.rect.colliderect(player_rect):
                    return True
        return False

    def handleMoveSpeed(self, pos, radius):
        player_rect = pygame.Rect(pos.x - radius, pos.y - radius, radius*2, radius*2)

        for row in self.tilemap:
            for tile in row:
                if tile.rect.colliderect(player_rect):
                    return tile.speed_modifier
        return 1.0

    def getCurrentTile(self, pos, radius):
        player_rect = pygame.Rect(pos.x - radius, pos.y - radius, radius*2, radius*2)

        for row in self.tilemap:
            for tile in row:
                if tile.rect.colliderect(player_rect):
                    return tile
        return None
