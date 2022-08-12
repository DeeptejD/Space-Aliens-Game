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
# background sound
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

ufo_x_speed = 1
for i in range(0, num_ufos):
    ufo_sprite.append(pygame.image.load('ufo.png'))
    ufoX.append(random.randint(0, 735))
    ufoY.append(random.randint(50, 200))
    ufoxchange.append(ufo_x_speed)
    ufoychange.append(40)

# bullet
bullet = pygame.image.load('bullet.png')
bulletX = 0 
bulletY = 480 
bulletxchange = 0
bulletychange = -20
# the state of the bullet
bullet_state = 'ready' 

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


# gameover font
over_font = pygame.font.Font('sunny.otf', 64)
def gameover_text():
    game_over = over_font.render('GAME OVER!\nFinal Score: {}'.format(score_value), True, (255, 255, 255))
    screen.blit(game_over, (135, 250))

running = True

while running:
    screen.fill((0, 0, 51))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -0.8
            if event.key == pygame.K_RIGHT:
                x_change = 0.8

            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                if bullet_state == 'ready':
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0

    playerX += x_change
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_ufos):
        #game over
        if ufoY[i] > 440:
            for j in range(num_ufos):
                ufoY[j] = 2000
            gameover_text()
            break

        ufoX[i] += ufoxchange[i]
        if ufoX[i] < 0:
            ufoxchange[i] = ufo_x_speed
            ufoY[i] += ufoychange[i]
        elif ufoX[i] >= 736:
            ufoxchange[i] = -ufo_x_speed
            ufoY[i] += ufoychange[i]
        collision = is_collision(ufoX[i], ufoY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            if ufo_x_speed <=3:
                ufo_x_speed += 0.2
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