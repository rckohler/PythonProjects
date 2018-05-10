import pygame
import math

class DrawableObject(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.imageMaster = image
        self.image = image
        self.width = 100
        self.height = 100
        self.xPos = x
        self.yPos = y
        self.angle = 0
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.shouldBeRemoved = False

    def handleBoundingRectangleAndImage(self):
        self.image = pygame.transform.scale(self.imageMaster, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect.center = self.xPos, self.yPos
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (self.xPos, self.yPos)  # Put the new rect's center at old center.

    def distanceFrom(self,other):
        dx = self.xPos - other.xPos
        dy = self.yPos - other.yPos
        d = dx*dx + dy * dy
        d = math.pow(d,.5)
        return d
    def update(self):
        if not self.imageMaster == None:
            self.handleBoundingRectangleAndImage()

class PhysicalObject(DrawableObject):
    def __init__(self,image,x,y,mass = 1):
        super().__init__(image,x,y)
        self.xVelocity = 0
        self.yVelocity = 0
        self.xAcceleration = 0
        self.yAcceleration = 0
        self.mass = mass

    def applyForce(self,force,angle):
        xComponentOfForce = math.cos(angle)*force
        yComponentOfForce = math.sin(angle)*force
        self.xAcceleration += xComponentOfForce/self.mass
        self.yAcceleration += yComponentOfForce/self.mass

    def update(self):
        self.xVelocity += self.xAcceleration
        self.yVelocity += self.yAcceleration
        self.xPos += self.xVelocity
        self.yPos += self.yVelocity
        super().update()

class Animation:
    def __init__(self, path, size, ID, start = 0, leadingZeroes = 0, isRecurring = False):
        self.ID = ID
        self.isRecurring = isRecurring
        self.images = self.loadImages(path,size,leadingZeroes,start)
        self.isFinished = False
    @staticmethod
    def loadImages(path,size, leadingZeroes, start):
        ret = []
        for i in range(size):
            tempPath = path
            for z in range(leadingZeroes):
                tempPath += '0'  # bad
            tempPath += str(i + start) + ".png"
            image = pygame.image.load(tempPath)
            image = pygame.transform.rotate(image,0)
            ret.append(image)
        return ret

    def begin(self):
        self.isFinished = False
    def resume(self):
        self.isFinished = False
    def returnImageAtCurrentFrameOfAnimation(self,animatedObject):
        return self.images[animatedObject.currentFrame]
    def update(self, animatedObject):
        length = self.images.__len__()
        if animatedObject.currentFrame < length - 1 and not self.isRecurring:
            animatedObject.currentFrame += 1
        else:
            animatedObject.currentFrame = 0
            self.isFinished = True


class SingleAnimationFromSpriteSheet(Animation):
    def __init__(self,path,ID,rows,cols,frames,size = 1):
        super().__init__(path,size,ID)
        self.rows = rows
        self.cols = cols
        self.frames = frames
        dummyList = self.images[:]
        self.spriteSheet = dummyList[0]

    def returnImageAtCurrentFrameOfAnimation(self,animatedObject):
        row = int(animatedObject.currentFrame/self.cols)
        col = animatedObject.currentFrame - self.cols * row
        rect = self.spriteSheet.get_rect()
        frameWidth = rect.width/self.cols
        frameHeight = rect.height/self.rows

        rect = pygame.Rect(col*frameWidth,row*frameHeight, frameWidth, frameHeight)
        image = pygame.Surface(rect.size).convert()
        colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        image.blit(self.spriteSheet, (0, 0), rect)
        return image
    def update(self,animateObject):
        if animateObject.currentFrame > self.frames:

            if self.isRecurring:
                animateObject.currentFrame = 0
            else:
                self.isFinished = True
        else:
            animateObject.currentFrame+=1

class AnimatedObject(PhysicalObject):
    # an animated object should have constants defined which will decide which animation is playing.
    IDLE = 0
    MOVE = 1
    def __init__(self, animations, x, y):
        super().__init__(animations[0].images[0],x,y)
        self.animations = animations
        self.currentAnimation = 0
        self.currentFrame = 0
#well I will come back ... this should have gotten the idea across. the remove function is currently the problem.
    def update(self):
        self.imageMaster = self.animations[self.currentAnimation].returnImageAtCurrentFrameOfAnimation(self)
        super().update()
        self.animations[self.currentAnimation].update(self)

class OctagonalAnimation(Animation):
    def __init__(self,path,ID,rows,cols,startCol, frames, arrayMatchedTo_N_NE_E_SE_S_SW_W_NW):
        super().__init__(path,1,ID)
        self.directionReferenceArray = arrayMatchedTo_N_NE_E_SE_S_SW_W_NW
        self.rows = rows
        self.cols = cols
        dummyList = self.images[:]
        self.spriteSheet = dummyList[0]
        self.startCol = startCol
        self.frames = frames
    def returnImageAtCurrentFrameOfAnimation(self,animatedObject):
        row = self.directionReferenceArray[animatedObject.currentDirection]
        col = animatedObject.currentFrame + self.startCol
        rect = self.spriteSheet.get_rect()
        frameWidth = rect.width/self.cols
        frameHeight = rect.height/self.rows

        rect = pygame.Rect(col*frameWidth,row*frameHeight, frameWidth, frameHeight)
        image = pygame.Surface(rect.size).convert()
        colorKey = image.get_at((0,0))
        image.set_colorkey(colorKey, pygame.RLEACCEL)
        image.blit(self.spriteSheet, (0, 0), rect)
        return image
    def update(self,animatedObject):
        animatedObject.currentFrame+=1
        if animatedObject.currentFrame >= self.frames:
            if self.isRecurring:
                animatedObject.currentFrame = 0
            else:
                self.isFinished = True

class OctagonallyBasedCharacter(AnimatedObject):
    #Directions

    NORTH = 0
    NORTH_EAST = 1
    EAST = 2
    SOUTH_EAST = 3
    SOUTH = 4
    SOUTH_WEST = 5
    WEST = 6
    NORTH_WEST = 7

    def __init__(self,animations,x,y):
        super().__init__(animations,x,y)
        self.currentDirection = OctagonallyBasedCharacter.NORTH
        self.speed = 5
    def move(self,direction):
        self.currentAnimation = OctagonallyBasedCharacter.MOVE
        self.currentDirection = direction
        if direction == OctagonallyBasedCharacter.NORTH:
            self.xVelocity = 0
            self.yVelocity = -self.speed
        if direction == OctagonallyBasedCharacter.NORTH_EAST:
            self.xVelocity = self.speed
            self.yVelocity = -self.speed
        if direction == OctagonallyBasedCharacter.EAST:
            self.xVelocity = self.speed
            self.yVelocity = 0
        if direction == OctagonallyBasedCharacter.SOUTH_EAST:
            self.xVelocity = self.speed
            self.yVelocity = self.speed
        if direction == OctagonallyBasedCharacter.SOUTH:
            self.xVelocity = 0
            self.yVelocity = self.speed
        if direction == OctagonallyBasedCharacter.SOUTH_WEST:
            self.xVelocity = -self.speed
            self.yVelocity = self.speed
        if direction == OctagonallyBasedCharacter.WEST:
            self.xVelocity = -self.speed
            self.yVelocity = 0
        if direction == OctagonallyBasedCharacter.NORTH_WEST:
            self.xVelocity = -self.speed
            self.yVelocity = -self.speed


    def update(self):
        super().update()
        self.animations[self.currentAnimation].direction = self.currentDirection

