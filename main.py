import pygame
import math
import random
from pygame import mixer

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
# backgrounf sound
mixer.music.load('8_bit_bg.wav')
mixer.music.play(-1)

# player
sprite = pygame.image.load('arcade-game.png')
playerX = 370
playerY = 480
x_change = 0
y_change = 0

# enemy ufo
ufo_sprite = []
ufoX = []
ufoY = []
ufoxchange = []
ufoychange = []
num_ufos = 6

ufo_x_speed = 0.5
for i in range(0, num_ufos):
    ufo_sprite.append(pygame.image.load('ufo.png'))
    ufoX.append(random.randint(0, 735))
    ufoY.append(random.randint(50, 200))
    ufoxchange.append(ufo_x_speed)
    ufoychange.append(40)

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

# score
score_value = 0
font = pygame.font.Font('sunny.otf', 32)

text_x = 10
text_y = 10


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(sprite, (x, y))


def ufo(x, y, i):
    screen.blit(ufo_sprite[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet, (x + 16, y + 10))


def is_collision(x1, y1, x2, y2):
    distance = math.sqrt((math.pow(x2-x1, 2))+(math.pow(y2-y1, 2)))
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

            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
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

    for i in range(num_ufos):
        ufoX[i] += ufoxchange[i]
        if ufoX[i] < 0:
            ufoxchange[i] = 0.5
            ufoY[i] += ufoychange[i]
        elif ufoX[i] >= 736:
            ufoxchange[i] = -0.5
            ufoY[i] += ufoychange[i]
        collision = is_collision(ufoX[i], ufoY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            ufo_x_speed += 1
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            ufoX[i] = random.randint(0, 735)
            ufoY[i] = random.randint(50, 150)

        ufo(ufoX[i], ufoY[i], i)
    
    if bulletY <= 0:
        bullet_state = 'ready'
        bulletY = 480

    if bullet_state == 'fire':
        bulletX = playerX
        fire_bullet(bulletX, bulletY)
        bulletY += bulletychange

    player(playerX, playerY)
    show_score(text_x, text_y)
    pygame.display.update()
