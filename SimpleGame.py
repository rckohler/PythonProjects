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

class Rocket(AnimatedObject):
    #create constants for different animations
    ROCKET_NOT_FIRING = 0
    ROCKET_FIRING = 1
    ROCKET_EXPLODING = 2
    #create animation that go with Rocket
    firingAnimation = Animation("exampleImages/rocketFiring",1,ROCKET_FIRING)
    notFiringAnimation = Animation("exampleImages/rocket",1,ROCKET_NOT_FIRING)
    rocketExploding = SingleAnimationFromSpriteSheet("exampleImages/explosion",ROCKET_EXPLODING,4,4,16)
    rocketExploding.isRecurring = False
    animations = [notFiringAnimation,firingAnimation,rocketExploding]

    def __init__(self,x,y):
        super().__init__(Rocket.animations,x,y)
        #add variables that are necessary for your rocket here.
        self.name = "a cool rocket"

        self.angle = 90 #not sure if i used degrees or radians...
        #so the remove is not working but everything else seems ok.
        #...
    def explode(self):
        self.currentAnimation = Rocket.ROCKET_EXPLODING

    def checkForRemoval(self):
        if self.currentAnimation == Rocket.ROCKET_EXPLODING and self.currentFrame > 23:
            self.shouldBeRemoved = True

class Asteroid(AnimatedObject):
    ASTEROID_MOVING = 0
    ASTEROID_EXPLODING = 1

    movingAnimation = Animation("exampleImages/world",1,ASTEROID_MOVING)
    explodingAnimation = Rocket.rocketExploding #same animation as rocket exploding
    animations = [movingAnimation,explodingAnimation]
    def __init__(self):
        super().__init__(Asteroid.animations,0,0)
        #obviously the sizes were off.
        self.width = 50
        self.height = 50
        self.yVelocity = 1 #random.randint(5,50)/100 # positive velocity moves down the screen.
        self.xPos = random.randint(self.width,screenWidth-self.width)
        self.yPos =  self.height #start off screen.
        self.update()
        print("created asteroid")
    def explode(self):
        self.currentAnimation = Asteroid.ASTEROID_EXPLODING
    def checkForRemoval(self):
       if self.currentAnimation ==  Asteroid.ASTEROID_EXPLODING and self.currentFrame > 14:
           #the names on these were switched before which is why it wasn't working....
            self.shouldBeRemoved = True
    def update(self):
        super().update()
        self.angle +=1
#3 create loop and initialize game

o = Rocket(screenWidth/2,screenHeight*.86)
o.angle = 0
def loop():
    # check for collisions
    for actor in actors:
        for potentialCollision in actors:
            if not actor == potentialCollision:
                if actor.distanceFrom(potentialCollision)<(actor.width + potentialCollision.width)/2:
                    actor.explode()
                    potentialCollision.explode()

                    #this is not the best way to do this with regard to memory but oh well.
    # check for input
    if pygame.key.get_pressed()[pygame.K_a] != 0:
        o.xVelocity = -1
    if pygame.key.get_pressed()[pygame.K_d] != 0:
        o.xVelocity = 1

    #create randomAsteroids
    if random.gauss(0,1) > 3.5:
        a = Asteroid()
        actors.add(a)

    #remove exploded objects
    toBeRemoved = []
    for actor in actors:
        actor.checkForRemoval()
        if actor.shouldBeRemoved:
            toBeRemoved.append(actor)
            #add is for groups, append is for lists.
    for actor in toBeRemoved:
        actors.remove(actor)
    toBeRemoved.clear()
    print(actors.__len__())

def initializeGame():
    actors.add(o)
    b = DrawableObject(pygame.image.load("exampleImages/space.png"),screenWidth/2,screenHeight/2)
    b.width = screenWidth
    b.height = screenHeight
    background.add(b)
    #update all objects prior to starting game to correctly size them.
    o.update()
    for b in background:
        b.update()

#4 create game

game = Game(screen,loop,initializeGame)
game.run()

