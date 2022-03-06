import pygame
import numpy
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import winsound


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
