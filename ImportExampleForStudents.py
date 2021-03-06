from CalvertScreen import Screen
from CalvertObjects import *
from CalvertGame import Game
import random
pygame.init()

### create screen
actors = pygame.sprite.Group()
scenery = pygame.sprite.Group()
groups = [scenery,actors]
screen_width = 700
screen_height = 500
screen = Screen(screen_width,screen_height,groups)


class Zombie(OctagonallyBasedCharacter):
    ATTACK = 2
    DIE = 3

    moveAnimation = OctagonalAnimation("exampleImages/zombie",OctagonallyBasedCharacter.MOVE,8,36,4,8,[2,3,4,5,6,7,0,1])
    moveAnimation.isRecurring = True
    idleAnimation = OctagonalAnimation("exampleImages/zombie",OctagonallyBasedCharacter.IDLE,8,36,0,4,[2,3,4,5,6,7,0,1])
    idleAnimation.isRecurring = True

    attackAnimation = OctagonalAnimation("exampleImages/zombie",ATTACK,8,36,12,10,[2,3,4,5,6,7,0,1])
    attackAnimation.isRecurring = False

    deathAnimation = OctagonalAnimation("exampleImages/zombie",DIE,8,36,22,2,[2,3,4,5,6,7,0,1])
    animations = [idleAnimation,moveAnimation,attackAnimation]
    def __init__(self,x,y):
        super().__init__(Zombie.animations,x,y)

    def wander(self):
        if random.randint(1,2)==1:
            self.move(random.randint(0,7))
        else:
            self.currentAnimation = OctagonallyBasedCharacter.IDLE
            self.xVelocity = 0
            self.yVelocity = 0
    def munchOnNearThing(self,munchee):
            self.currentAnimation = Zombie.ATTACK
    def die(self):
            self.currentAnimation = Zombie.DIE
    def update(self):
        super().update()
        if random.randint(1,20) == 1:
            self.wander()
        if self.animations[self.currentAnimation].isFinished:
            self.animations[self.currentAnimation].isFinished = False
            self.currentAnimation = Zombie.IDLE
            self.currentFrame = 0
        if self.currentAnimation == Zombie.DIE and self.animations[self.currentAnimation].isFinished:
            actors.remove(self)
class Cowboy(OctagonallyBasedCharacter):
    ATTACK = 2
    moveAnimation = OctagonalAnimation("exampleImages/cowboy",OctagonallyBasedCharacter.MOVE,10,14,1,10,[5,4,3,2,9,8,7,6])
    moveAnimation.isRecurring = True
    idleAnimation = OctagonalAnimation("exampleImages/cowboy",OctagonallyBasedCharacter.IDLE,10,14,0,1,[5,4,3,2,9,8,7,6])
    idleAnimation.isRecurring = True

    attackAnimation = OctagonalAnimation("exampleImages/cowboy",ATTACK,10,14,10,3,[5,4,3,2,9,8,7,6])
    attackAnimation.isRecurring = False
    animations = [idleAnimation,moveAnimation,attackAnimation]

    def __init__(self):
        super().__init__(Cowboy.animations,100,100)
        self.width = 50
        self.height = 50
        for zombie in actors:
            if isinstance(zombie,Zombie):
                if math.abs(zombie.xPos - o.xPos)<25 or math.ab(zombie.yPos - o.yPos)< 25:
                    zombie.die()
    def update(self):
        super().update()
        try:
            if self.animations[self.currentAnimation].isFinished:
                self.currentAnimation = Cowboy.IDLE
        except:
            print("error")
    def fire(self):
        self.currentAnimation = Cowboy.ATTACK
        self.currentFrame = 1
        self.xVelocity = 0
        self.yVelocity = 0
#r = Rocket()
o = Cowboy()
actors.add(o)
def loop():
    handleEvents()
def initializeGame():
    global r
    #actors.add(r)
    for i in range(20):
        actors.add(Zombie(random.randint(1,screen_width),random.randint(1,screen_height)))
    backgroundImage = pygame.image.load("exampleImages/moonSurface.jpg")
    background = DrawableObject(backgroundImage,screen_width/2,screen_height/2)
    background.width = screen_width
    background.height = screen_height
    scenery.add(background)
def handleEvents():
    # this is a good example of a time when it would be better to write a function than hard code each point.
    for actor in actors:
        for otherActor in actors:
            if not actor == otherActor and isinstance(actor,Zombie) and actor.distanceFrom(otherActor)<50:
                actor.munchOnNearThing(otherActor)


    if pygame.key.get_pressed()[pygame.K_SPACE] != 0:
        o.fire()
    if pygame.key.get_pressed()[pygame.K_a] != 0:
        o.move(OctagonallyBasedCharacter.WEST)
    if pygame.key.get_pressed()[pygame.K_d] != 0:
        o.move(OctagonallyBasedCharacter.EAST)
    if pygame.key.get_pressed()[pygame.K_q] != 0:
        o.move(OctagonallyBasedCharacter.NORTH_WEST)
    if pygame.key.get_pressed()[pygame.K_w] != 0:
        o.move(OctagonallyBasedCharacter.NORTH)
    if pygame.key.get_pressed()[pygame.K_e] != 0:
        o.move(OctagonallyBasedCharacter.NORTH_EAST)
    if pygame.key.get_pressed()[pygame.K_c] != 0:
        o.move(OctagonallyBasedCharacter.SOUTH_EAST)
    if pygame.key.get_pressed()[pygame.K_x] != 0:
        o.move(OctagonallyBasedCharacter.SOUTH)
    if pygame.key.get_pressed()[pygame.K_z] != 0:
        o.move(OctagonallyBasedCharacter.SOUTH_WEST)

game = Game(screen,loop,initializeGame)
game.run()
