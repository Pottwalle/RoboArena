import pygame

class Movement:
    def __init__(self, tilemap):
        self.tilemap = tilemap

    def move(self, player, dt):
        # echte Spielerposition (Sprite-Mitte)
        pos = player.position
        radius = player.r
        offset = player.hitbox_offset

        direction = player.direction
        velocity = player.velocity
        acceleration = player.acceleration
        max_speed = player.max_speed
        friction = player.friction

        # --- Tile Speed Modifier ---
        speed_mod = self.handleMoveSpeed(pos + offset, radius)

        # --- Beschleunigung ---
        if direction.length() > 0:
            dir_norm = direction.normalize()

            # Richtungswechsel abbremsen
            if velocity.length() > 0:
                vel_dir = velocity.normalize()
                if vel_dir.dot(dir_norm) < 0:
                    velocity *= 0.5

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
        if self.handleCollision(test_pos_x + offset, radius):
            velocity.x = 0
        else:
            new_pos.x = test_pos_x.x

        # --- dann Y-Achse bewegen ---
        test_pos_y = pygame.Vector2(new_pos.x, new_pos.y + delta.y)
        if self.handleCollision(test_pos_y + offset, radius):
            velocity.y = 0
        else:
            new_pos.y = test_pos_y.y

        player.velocity = velocity
        return new_pos


    # ---------------------------------------------------------
    # Kollisionen — immer mit pos + offset arbeiten!
    # ---------------------------------------------------------

    def getCollidingTiles(self, pos, radius):
        hit_pos = pos
        player_rect = pygame.Rect(hit_pos.x - radius, hit_pos.y - radius, radius*2, radius*2)

        tiles = []
        for row in self.tilemap:
            for tile in row:
                if tile.solid and tile.rect.colliderect(player_rect):
                    tiles.append(tile)
        return tiles

    def getCollisionNormal(self, pos, radius, tile_rect):
        hit_pos = pos 
        player_rect = pygame.Rect(hit_pos.x - radius, hit_pos.y - radius, radius*2, radius*2)

        dx = (player_rect.centerx - tile_rect.centerx) / tile_rect.width
        dy = (player_rect.centery - tile_rect.centery) / tile_rect.height

        if abs(dx) > abs(dy):
            return pygame.Vector2(1 if dx > 0 else -1, 0)
        else:
            return pygame.Vector2(0, 1 if dy > 0 else -1)

    def getCollisionTile(self, pos, radius):
        hit_pos = pos 
        player_rect = pygame.Rect(hit_pos.x - radius, hit_pos.y - radius, radius*2, radius*2)

        for row in self.tilemap:
            for tile in row:
                if tile.solid and tile.rect.colliderect(player_rect):
                    return tile
        return None

    def handleCollision(self, pos, radius):
        hit_pos = pos  # pos ist bereits pos + offset in move()
        player_rect = pygame.Rect(hit_pos.x - radius, hit_pos.y - radius, radius*2, radius*2)

        for row in self.tilemap:
            for tile in row:
                if tile.solid and tile.rect.colliderect(player_rect):
                    return True
        return False

    def handleMoveSpeed(self, pos, radius):
        hit_pos = pos
        player_rect = pygame.Rect(hit_pos.x - radius, hit_pos.y - radius, radius*2, radius*2)

        for row in self.tilemap:
            for tile in row:
                if tile.rect.colliderect(player_rect):
                    return tile.speed_modifier
        return 1.0

    def getCurrentTile(self, pos, radius):
        hit_pos = pos
        player_rect = pygame.Rect(hit_pos.x - radius, hit_pos.y - radius, radius*2, radius*2)

        for row in self.tilemap:
            for tile in row:
                if tile.rect.colliderect(player_rect):
                    return tile
        return None
