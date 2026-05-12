import pygame
import math


# Roboter Klasse mit Attributen, Position, Radius und Richtung
class BasicRobot:
    def __init__(self, x, y, r, alpha):
        self.x = x
        self.y = y
        self.r = r
        self.alpha = alpha

    def draw(self, screen):
        # Zeichnet den blauen Kreis
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.r)
        # Zeichnet den schwarzen Rand
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.r, 2)

        # Berechnung der Blickrichtung
        rad = math.radians(self.alpha)
        end_x = self.x + math.cos(rad) * self.r
        end_y = self.y - math.sin(rad) * self.r

        # zeichnen Richtungslinie
        pygame.draw.line(screen, (0, 0, 0), (int(self.x), int(self.y)), (int(end_x), int(end_y)), 2)


#  Test-Block
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Test wird erstellt
    test_roboter = BasicRobot(400, 300, 40, 45)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        # Testen die Richtung um 360 grad:
        test_roboter.alpha += 1

        test_roboter.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
