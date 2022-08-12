import math
import random

import pygame

pygame.init()

# setting a window
screen = pygame.display.set_mode((800, 600))
# icon
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
# title
pygame.display.set_caption('UFO Buster!')
# background
background = pygame.image.load('background.jpg')

# score
score = 0

# player
sprite = pygame.image.load('arcade-game.png')
playerX = 370
playerY = 480
x_change = 0
y_change = 0

# enemy ufo
ufo_sprite = pygame.image.load('ufo.png')
ufoX = random.randint(0, 736)
ufoY = random.randint(0, 200)
ufoxchange = 0.5
ufoychange = 40

# bullet
bullet = pygame.image.load('bullet.png')
bulletX = 0  # will be changed in the while loop
bulletY = 480  # 480 because bullet is always starting at the same level at the player
bulletxchange = 0
bulletychange = -20
# the state of the bullet
bullet_state = 'ready'  # ready state is when u can't see the bullet


# fire state would mean that the bullet is currently moving

# updating variables


def player(x, y):
    screen.blit(sprite, (x, y))


def ufo(x, y):
    screen.blit(ufo_sprite, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet, (x + 16, y + 10))


def is_collision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    if distance < 27:
        return True
    else:
        return False


running = True

while running:
    screen.fill((0, 0, 51))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #     checking if any key is pressed on the keyboard
        if event.type == pygame.KEYDOWN:
            # print('A keystroke has been pressed')
            if event.key == pygame.K_LEFT:
                x_change = -0.8
                # print('Left arrow key has been pressed')
            if event.key == pygame.K_RIGHT:
                # print('Right arrow key was pressed')
                x_change = 0.8
            # if event.key == pygame.K_UP:
            #     y_change = -0.5
            # if event.key == pygame.K_DOWN:
            #     y_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # y_change = 0
                x_change = 0

    playerX += x_change
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    ufoX += ufoxchange
    if ufoX < 0:
        ufoxchange = 0.5
        ufoY += ufoychange
    elif ufoX >= 736:
        ufoxchange = -0.5
        ufoY += ufoychange
    if bulletY <= 0:
        bullet_state = 'ready'
        bulletY = 480

    if bullet_state == 'fire':
        bulletX = playerX
        fire_bullet(bulletX, bulletY)
        bulletY += bulletychange

    player(playerX, playerY)
    ufo(ufoX, ufoY)

    if is_collision(ufoX, ufoY, playerX, playerY):
        bulletY = 480
        bullet_state = 'ready'
        score += 1
        print(score)

    pygame.display.update()
