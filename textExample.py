#this video will cover the basics of creating a simple game using classes I have written for you
#and pygame.

#0 import my classes
from CalvertGame import *
from CalvertScreen import *
from CalvertObjects import *
import random

#1 create classes that will be used in your game
#1b create groups that will hold your objects
actors = pygame.sprite.Group()
background = pygame.sprite.Group()

#2 screen variables
screenWidth = 400 #arbitrary
screenHeight = 300 #arbitrary

#2b create screen
groups = [background,actors]
screen = Screen(screenWidth,screenHeight,groups)

def drawText():
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render('Some Text', False, (255, 255, 255))
    screen.screen.blit(textsurface, (0, 0))


def loop():
    if pygame.time.get_ticks()%500 == 0:
        drawText()

def initializeGame():
    pygame.font.init()
    b = DrawableObject(pygame.image.load("exampleImages/space.png"),screenWidth/2,screenHeight/2)
    b.width = screenWidth
    b.height = screenHeight
    background.add(b)
    #update all objects prior to starting game to correctly size them.
    for b in background:
        b.update()
        drawText()


#4 create game

game = Game(screen,loop,initializeGame)
game.run()

