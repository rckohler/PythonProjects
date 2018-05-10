from CalvertGame import *
from CalvertScreen import *
from CalvertObjects import *
import random

actors = pygame.sprite.Group()
background = pygame.sprite.Group()

#2 screen variables
screenWidth = 400 #arbitrary
screenHeight = 300 #arbitrary

#2b create screen
groups = [background,actors]
screen = Screen(screenWidth,screenHeight,groups)

class Guy(AnimatedObject):
    #create constants for different animations
    WALK = 0
    #create animation that go with Rocket
    walkAnimation = Animation("ElijahExampleImages/wobbles_",4,WALK)
    animations = [walkAnimation]

    def __init__(self,x,y):
        super().__init__(Guy.animations,x,y)
        #add variables that are necessary for your rocket here.
        self.name = "a cool walking dude"
        actors.add(self)

def loop():
    pass

def initializeGame():
    b = DrawableObject(pygame.image.load("exampleImages/space.png"), screenWidth / 2, screenHeight / 2)
    b.width = screenWidth
    b.height = screenHeight
    background.add(b)
    # update all objects prior to starting game to correctly size them.
    guy = Guy(100,100)
    guy.update()

    for b in background:
        b.update()

game = Game(screen,loop,initializeGame)
game.run()