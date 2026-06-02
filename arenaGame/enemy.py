import pygame
import math
import random
import movement

class Enemy:
    def __init__(self, x, y, r, alpha, base_speed, movement, speed_modifier=1, health=10, damage=5, movementType="random"):
        self.position = pygame.Vector2(x, y)
        self.r = r
        self.alpha = alpha
        self.direction = pygame.Vector2()

        self.base_speed = base_speed
        self.speed_modifier = speed_modifier
        self.health = health
        self.damage = damage
        self.movement_type = movementType
        self.movement = movement  # Movement-Objekt übergeben

        # --- movement Erweiterung ---
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 800
        self.max_speed = 300
        self.friction = 0.90

        '''handles the updating of all player related methods changing the coordinates accordingly'''




    def update(self, dt, player, clock):
        self.move(dt,player,clock)
        self.alpha = math.degrees(math.atan2(-self.direction.y, self.direction.x))

    def draw(self, screen, camera):
        screen_position = self.position - camera
        pygame.draw.circle(screen, "red", (screen_position.x, screen_position.y), self.r)
        pygame.draw.circle(screen, (0, 0, 0), (screen_position.x, screen_position.y), self.r, 2)

        rad = math.radians(self.alpha)
        end_x = screen_position.x + math.cos(rad) * self.r
        end_y = screen_position.y - math.sin(rad) * self.r
        pygame.draw.line(screen, (0, 0, 0), (screen_position.x, screen_position.y), (int(end_x), int(end_y)), 2)

    def calcDirection(self, player, clock):
        if self.movement_type == "random":
            if random.randint(0, 500) == 0:
                self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
                if self.direction.length() > 0:
                    self.direction.normalize_ip()

        elif self.movement_type == "aggressive":
            diff = player.position - self.position
            if diff.length() > 0:
                self.direction = diff.normalize()

        elif self.movement_type == "passive":
            if (player.position - self.position).length() < 100:
                diff = self.position - player.position
                if diff.length() > 0:
                    self.direction = diff.normalize()
            elif (player.position - self.position).length() > 200:
                diff = player.position - self.position
                if diff.length() > 0:
                    self.direction = diff.normalize()
            else:
                self.direction = pygame.Vector2(0, 0)

        else:
            self.speed_modifier = 0

    def move(self, dt, player, clock):
        self.calcDirection(player, clock)
        # movement.move() übernimmt Kollision & Tile-Geschwindigkeit automatisch

        self.position = self.movement.move(
            self,
            dt
        )