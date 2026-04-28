import pygame
import random
import math
import os

pygame.init()

# Base directory of this script
BASE_DIR = os.path.dirname(__file__)

def asset(path):
    return os.path.join(BASE_DIR, path)

# Load images
icon = pygame.image.load(asset("resources/images/5.png"))
background = pygame.image.load(asset("resources/images/5.png"))
player_img = pygame.image.load(asset("resources/images/5.png"))
enemy_img = pygame.image.load(asset("resources/images/5.png"))
bullet_img = pygame.image.load(asset("resources/images/5.png"))

# Game Window
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(icon)

# Player
player_x = 370
player_y = 480
player_x_change = 0
player_x_size = player_img.get_width()

def player(x, y):
    screen.blit(player_img, (x, y))

# Score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)

def show_score():
    score_blit = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_blit, (10, 10))

# Game over
game_over_font = pygame.font.Font("freesansbold.ttf", 64)

def game_over_text():
    game_over_blit = game_over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(game_over_blit, (200, 250))

# Enemy
enemy_width = enemy_img.get_width()
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = 40
number_of_enemies = 6

for i in range(number_of_enemies):
    enemy_x.append(random.randint(0, width - enemy_width))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(3)

def enemy(x, y):
    screen.blit(enemy_img, (x, y))

# Bullet
bullet_x = 0
bullet_y = 480
bullet_y_change = 10
bullet_ready = True

bullet_x_offset = bullet_img.get_width() // 2
bullet_y_offset = bullet_img.get_height() // 2

def fire_bullet(x, y):
    global bullet_ready
    bullet_ready = False
    screen.blit(bullet_img, (x + bullet_x_offset, y + bullet_y_offset))

def is_collision(ex, ey, bx, by):
    distance = math.sqrt((ex - bx)**2 + (ey - by)**2)
    return distance < 27

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player Movement
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                player_x_change = -4
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                player_x_change = 4
            if event.key == pygame.K_SPACE and bullet_ready:
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
                player_x_change = 0

    # Player movement
    player_x += player_x_change
    player_x = max(0, min(player_x, width - player_x_size))
    player(player_x, player_y)

    # Enemies
    for i in range(number_of_enemies):
        if enemy_y[i] > 440:
            for j in range(number_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0 or enemy_x[i] >= (width - enemy_width):
            enemy_x_change[i] *= -1
            enemy_y[i] += enemy_y_change

        enemy(enemy_x[i], enemy_y[i])

        # Collision
        if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            bullet_y = 480
            bullet_ready = True
            score += 1
            enemy_x[i] = random.randint(0, width - enemy_width)
            enemy_y[i] = random.randint(50, 150)

    # Bullet movement
    if not bullet_ready:
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    if bullet_y <= -20:
        bullet_y = 480
        bullet_ready = True

    show_score()

    clock.tick(60)
    pygame.display.update()
