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

        # gewünschte Bewegung in diesem Frame
        delta = velocity * dt
        new_pos = pygame.Vector2(pos.x, pos.y)

        # --- erst X-Achse bewegen ---
        test_pos_x = pygame.Vector2(new_pos.x + delta.x, new_pos.y)
        if self.handleCollision(test_pos_x, radius):
            # X blockiert → X-Geschwindigkeit stoppen
            velocity.x = 0
        else:
            new_pos.x = test_pos_x.x

        # --- dann Y-Achse bewegen ---
        test_pos_y = pygame.Vector2(new_pos.x, new_pos.y + delta.y)
        if self.handleCollision(test_pos_y, radius):
            # Y blockiert → Y-Geschwindigkeit stoppen
            velocity.y = 0
        else:
            new_pos.y = test_pos_y.y

        player.velocity = velocity
        return new_pos


    def getCollidingTiles(self, pos, radius):
        player_rect = pygame.Rect(pos.x - radius, pos.y - radius, radius*2, radius*2)
        tiles = []

        for row in self.tilemap:
            for tile in row:
                if tile.solid and tile.rect.colliderect(player_rect):
                    tiles.append(tile)
        return tiles

    def getCollisionNormal(self, pos, radius, tile_rect):
        player_rect = pygame.Rect(pos.x - radius, pos.y - radius, radius*2, radius*2)

        dx = (player_rect.centerx - tile_rect.centerx) / tile_rect.width
        dy = (player_rect.centery - tile_rect.centery) / tile_rect.height

        if abs(dx) > abs(dy):
            return pygame.Vector2(1 if dx > 0 else -1, 0)
        else:
            return pygame.Vector2(0, 1 if dy > 0 else -1)
        
    def getCollisionTile(self, pos, radius):
        player_rect = pygame.Rect(pos.x - radius, pos.y - radius, radius*2, radius*2)

        for row in self.tilemap:
            for tile in row:
                if tile.solid and tile.rect.colliderect(player_rect):
                    return tile
        return None

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
