from CalvertGame import *
from CalvertScreen import *
from CalvertObjects import *
import random

actors = pygame.sprite.Group()
background = pygame.sprite.Group()

screenWidth = 400
screenHeight = 300

class Minion(AnimatedObject):
    MINION_DEATH = 1
    dyingAnimation = SingleAnimationFromSpriteSheet("exampleImages/minionDying", MINION_DEATH, 5, 5, 25)
    dyingAnimation.isRecurring = False
    animations = [dyingAnimation]
    radius = 10

    def __init__(self,x,y):
        self.width = 50
        self.height = 50
        self.xPos = random.randint(self.width, screenWidth - self.width)
        self.yPos = random.randint(self.height, screenHeight- self.height)
        self.update()

    def minionDie(self):
        self.currentAnimation = Minion.MINION_DEATH
    def checkForRemoval(self):
       if self.currentAnimation == Minion.MINION_DEATH and self.currentFrame > 23:
           self.shouldBeRemoved = True
    def update(self):
        super().update()
        self.shrinkMinion()

    def shrinkMinion(self):
        self.radius -= 1

    def moveMinion(self, x, y):
        changeX = random.randint(0,screenWidth)
        changeY = random.randint(0,screenHeight)