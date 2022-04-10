import pygame
import numpy
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector

pygame.init()
win = pygame.display.set_mode((1280,720))

pygame.display.set_caption('Hockey Computer Vision')
icon = pygame.image.load('hockey.png')
pygame.display.set_icon(icon)

white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
font = pygame.font.Font('Spiky.otf', 50)
font1 = pygame.font.Font('Spiky.otf', 30)

player1 = pygame.image.load('player_left1.png').convert_alpha()
player2 = pygame.image.load('player_right1.png').convert_alpha()
background = pygame.image.load('1280x720.png').convert_alpha()
background1 = pygame.image.load('1280x720full.png').convert_alpha()

rect_player1 = player1.get_rect()
rect_player2 = player2.get_rect()
rect_background = background.get_rect()
rect_background1 = background1.get_rect()

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(3,1280)
cap.set(4, 720)

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10,75])
        # self.image.fill(white)
        self.rect = self.image.get_rect()
        self.points = 0

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([15,15])
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x = 1280 // 2
        self.rect.y = 720 // 2 + 20
        self.speed = 15
        self.dx = 1
        self.dy = 1

detector = HandDetector(detectionCon=0.8, maxHands=2)

paddle1 = Paddle()
paddle1.rect.x = 100
paddle1.rect.y = 225
rect_player1.x = 0
rect_player1.y = 225

paddle2 = Paddle()
rect_player2.x = 1145
rect_player2.y = 225

paddle_speed = 20

pong = Ball()
ballx = Ball()
ballx.image.fill(red)

all_sprites = pygame.sprite.Group()
all_sprites.add(pong)
extra_ball = 0

def Xball():
    if extra_ball >= 3:
        ballx.speed = 25
        all_sprites.add(ballx)
        ballx.rect.x += ballx.speed * ballx.dx
        ballx.rect.y += ballx.speed * ballx.dy
        if ballx.rect.x > 1280:
            ballx.rect.x, ballx.rect.y = 640, 360
            paddle1.points += 1
        if ballx.rect.y > 680:
            ballx.dy = -1
        if ballx.rect.y < 20:
            ballx.dy = 1
        if ballx.rect.x < 10:
            ballx.dx = 1
        if rect_player1.colliderect(ballx.rect):
            ballx.dx = 1
        if rect_player2.colliderect(ballx.rect):
            ballx.dx = -1
    else: all_sprites.remove(ballx)

def game_over():
    if pong.speed == 50:
        pong.dx = 0
        pong.dy = 0
        ballx.dy = 0
        ballx.dx = 0
        Game_Over_text1 = font.render('Game Over - Speed 50', False, black)
        Game_Over_rect1 = Game_Over_text1.get_rect()
        Game_Over_rect1.center = (640, 340)
        win.blit(Game_Over_text1, Game_Over_rect1)
        Game_Over_text = font.render('Game Over - Speed 50', False, green)
        Game_Over_rect = Game_Over_text.get_rect()
        Game_Over_rect.center = (640, 345)
        win.blit(Game_Over_text,Game_Over_rect)
        all_sprites.draw(win)
        pygame.display.update()

def redraw():
    text = font.render('Score',False, black)
    textRect = text.get_rect()
    textRect.center = (1280//2,50)

    text_speed = font1.render(f'Speed: {pong.speed}', False, red)
    textRect_speed = text_speed.get_rect()
    textRect_speed.center = (1280 // 2, 100)

    #Player 1 Score
    p1_score = font.render(str(paddle1.points),False,black)
    p1Rect = p1_score.get_rect()
    p1Rect.center = (100,70)
    win.blit(p1_score, p1Rect)

    p2_score = font.render(str(paddle2.points), False, red)
    p2Rect = p2_score.get_rect()
    p2Rect.center = (1150, 70)
    win.blit(p2_score, p2Rect)

    win.blit(text, textRect)
    win.blit(text_speed, textRect_speed)
    all_sprites.draw(win)
    pygame.display.update()

run= True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        if rect_player1.y <0:
            rect_player1.y = 5
        rect_player1.y += - paddle_speed
    if key[pygame.K_s]:
        rect_player1.y +=  paddle_speed
        if rect_player1.y >650:
            rect_player1.y = 630

    succes, img = cap.read()
    img = cv.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        hand = hands[0]
        x, y = hand['lmList'][8]
        rect_player2.y = y
    pong.rect.x += pong.speed * pong.dx
    pong.rect.y += pong.speed * pong.dy

    if pong.rect.x > 1280//2:
        pong.image.fill(green)

    if pong.rect.x < 1280 // 2:
        pong.image.fill(black)

    if pong.rect.y > 680:
        pong.dy = -1

    if pong.rect.x > 1280:
        pong.rect.x, pong.rect.y = 640,360
        pong.speed +=5
        pong.dx = -1
        paddle1.points +=1

    if pong.rect.y < 20:
        pong.dy = 1
    if pong.rect.x < 10:
        pong.rect.x, pong.rect.y = 640, 360
        pong.speed +=5
        pong.dx = 1
        paddle2.points +=1
        extra_ball += 1


    if rect_player1.colliderect(pong.rect):
        pong.dx = 1
    if rect_player2.colliderect(pong.rect):
        pong.dx = -1

    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    imgRGB = numpy.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame, True, False)
    win.blit(frame, (0, 0))
    win.blit(background, rect_background)
    win.blit(player1, rect_player1)
    win.blit(player2, rect_player2)
    redraw()
    Xball()
    game_over()

pygame.quit()
