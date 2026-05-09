import pygame
import math


# Roboter Klasse mit Attributen, Position, Radius und Richtung
class Player:
    def __init__(self, x, y, r, alpha, base_speed, speed_modifier = 1):
        '''Represents th Player in the game holding the position, handling the movement and drawing of the player

        Attributes:
            x: players x position
            y: players y position
            r: player radius #WIP
            alpha: ?
            base_speed: the bas movement speed of the player
            speed_modifier: the multiplier of the base speed, initially 1
        '''
        self.position = pygame.Vector2(x, y)
        self.r = r
        self.alpha = alpha
        self.direction = pygame.Vector2()

        self.base_speed = base_speed
        self.speed_modifier = speed_modifier
    
    def update(self, dt):
        '''handles the updating of all player related methods in the main game loop'''
        self.input()
        self.move(dt)

    def paint(self, screen):
        # Zeichnet den blauen Kreis
        pygame.draw.circle(screen, (173, 216, 230), (int(self.position.x), int(self.position.y)), self.r)
        # Zeichnet den schwarzen Rand
        pygame.draw.circle(screen, (0, 0, 0), (int(self.position.x), int(self.position.y)), self.r, 2)

        # Berechnung der Blickrichtung
        rad = math.radians(self.alpha)
        end_x = self.position.x + math.cos(rad) * self.r
        end_y = self.position.y - math.sin(rad) * self.r

        # zeichnen Richtungslinie
        pygame.draw.line(screen, (0, 0, 0), (int(self.position.x), int(self.position.y)), (int(end_x), int(end_y)), 2)

    def input(self):
        '''handles the inputs for the player movement and sets the direction value accordingly
        
        sets the direction y to w = -1, s = 1, and x to a = -1, d = 1'''
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_w]:
            self.direction.y = -1
        if keys[pygame.K_s]:
            self.direction.y = 1
        if keys[pygame.K_a]:
            self.direction.x = -1
        if keys[pygame.K_d]:
            self.direction.x = 1

        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
    
    def move(self, dt):
        '''moves the player
        
        Attributes:
            dt - delta time (time elapsed since last frame)'''
        self.position += self.direction * self.speed * self.speed_modifier * dt
