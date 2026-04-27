import pygame
import random
import math

# init pygame
pygame.init()

# Game Window
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
# set window title & icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("Space_Invaders/root/resources/images/5.png")
pygame.display.set_icon(icon)

# set Background
background = pygame.image.load("Space_Invaders/root/resources/images/5.png")

# Player
player_img = pygame.image.load("Space_Invaders/root/resources/images/5.png")
player_x = 370
player_y = 480
player_x_change = 0
player_x_size = player_img.get_size()[0]

def player(x, y):
    screen.blit(player_img, (x, y))

# Score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10

def show_score(x, y):
    score_blit = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_blit, (x, y))

# Game over
game_over_font = pygame.font.Font("freesansbold.ttf", 64)

def game_over_text():
    game_over_blit = game_over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(game_over_blit, (200, 250))

# Enemy
enemy_img = pygame.image.load("Space_Invaders/root/resources/images/5.png")
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
bullet_img = pygame.image.load("Space_Invaders/root/resources/images/5.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 4
bullet_y_change = 10
bullet_ready = False

bullet_x_offset = int(bullet_img.get_size()[0] / 2)
bullet_y_offset = int(bullet_img.get_size()[1] / 2)

def fire_bullet(x, y):
    global bullet_ready
    bullet_ready = False
    screen.blit(bullet_img, (x + bullet_x_offset, y + bullet_y_offset))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2)
    if distance < 27:
        return True
    else:
        return False

# basic game loop
running = True
clock = pygame.time.Clock()
while running:
    # draw Background
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
                # fire bullet logic at current player x
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
                player_x_change = 0

    # draw Player & change coords + boundaries
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= (width - player_x_size):
        player_x = (width - player_x_size)
    player(player_x, player_y)

    # draw enemy and change its coords + boundaries
    for i in range(number_of_enemies):
        # Game over calc
        if enemy_y[i] > 440: # height at wich when reached by enemies game is over
            for j in range(number_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0 or enemy_x[i] >= (width - player_x_size):
            enemy_x_change[i] *= -1
            enemy_y[i] += enemy_y_change
        
        enemy(enemy_x[i], enemy_y[i])

        # collision enemy / bullet
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 480
            bullet_ready = True
            score += 1

            enemy_x[i] = random.randint(0, width - enemy_width)
            enemy_y[i] = random.randint(50, 150)

    # bullet movement
    if bullet_y <= 0 - bullet_y_offset * 2:
        bullet_y = 480
        bullet_ready = True

    if not bullet_ready:
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
    
    show_score(text_x, text_y)


    clock.tick(60)
    pygame.display.update()