# Michelle Deng
# fallDown.py

# Import modules:
import os, sys, random
import pygame
from pygame.locals import *


# Uploads an image file
# I did NOT write this function!
# Credits: http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html
def load_image(name, colorkey = None):
    fullname = os.path.join('', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Cannot load image:", name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        # If there isn't an image file, changes the color to the one at the
        # top left corner (sets transparency)
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        # RLEACCEL is for older computers; tunes the graphics
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

# Create the ball
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        # Call Sprite initializer
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("crystal_sphere.png", -1)
        self.speedx = 19
        self.speedy = 0
        self.area = self.image.get_rect()
        self.width = self.area.width
        self.height = self.area.height
        self.loBound = self.rect.y + self.height
        self.gravity = 25
        self.wasColliding = False
    
    # Moving the ball
    def moveLeft(self):
        if (self.rect.x != 0):
            self.rect = self.rect.move(-self.speedx, self.speedy)
        else:
            print "no move left"
    def moveRight(self, data):
        margin = 3
        if (self.rect.x + self.width + margin < data.width):    
            self.rect = self.rect.move(self.speedx, self.speedy)
        else:
            print "no move right"

    def ballStepsColl(self, data):
        # make sure ball still moves along step
        isColliding = False
        
        for step in data.stepsList:
            if (len(step.rect.collidelistall([self])) > 0):
                #self.rect.y -= data.speedy
                isColliding = True

        if (isColliding):
            self.rect = self.rect.move(0, -data.speedy)
            if not self.wasColliding:
                data.bounceSound.play()
                self.wasColliding = True
        elif (self.rect.y > (data.height - self.height)):
            pass   
        else:
            self.wasColliding = False
            self.rect = self.rect.move(0, self.gravity)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # Call Sprite initializer
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("enemy.png", -1)
        self.speedx = 14
        self.speedy = 0
        self.area = self.image.get_rect()
        self.width = self.area.width
        self.height = self.area.height
        self.loBound = self.rect.y + self.height
        self.gravity = 25
    def movingLeft(self, data):
        #if (self.rect.x != 0):
        self.rect = self.rect.move(-self.speedx, self.speedy)
        if (self.rect.x <= 0):
            self.rect = self.rect.move(self.speedx, self.speedy)
    def movingRight(self, data):
        #if (self.rect.x + self.width < data.width):
        self.rect = self.rect.move(self.speedx, self.speedy)
        if (self.rect.x + self.width < data.width):
            self.rect = self.rect.move(-self.speedx, self.speedy)
    def enemyCollSteps(self, data):
        isColliding = False
        for step in data.stepsList:
            if (len(step.rect.collidelistall([self])) > 0):
                isColliding = True
        if (isColliding):
            self.rect = self.rect.move(0, -data.speedy)
        else:
            self.rect = self.rect.move(0, self.gravity)
    def killBall(self, data):
        pass


# Rotate an image around its center
# I did NOT write this function!
# Credits: http://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

class Steps(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.height = height
        self.image = pygame.Surface([width, self.height])
        self.rect = self.image.get_rect()
        self.image.fill(color)

#############
# RED STEPS #
#############
def oneHoleRed(data):
    red = data.redColor
    randHolePos = random.randint(data.spaceX, data.width - data.spaceX)
    
    leftStepWidth = randHolePos - data.spaceX/2
    data.leftStep = Steps(leftStepWidth, data.stepHeight, red)
    data.leftStep.rect.x = 0 
    data.leftStep.rect.y = data.height
    data.stepsList.add(data.leftStep)
    
    rightStepWidth = data.width - (randHolePos + data.spaceX/2)
    data.rightStep = Steps(rightStepWidth, data.stepHeight, red)
    # Sets each step on the right side of the screen
    data.rightStep.rect.x = data.width - rightStepWidth 
    data.rightStep.rect.y = data.height 
    data.stepsList.add(data.rightStep)

def twoHolesRed(data):
    red = data.redColor
    leftStepWidth = random.randint(0, (data.width/2 - 2*data.spaceX))
    data.leftStep = Steps(leftStepWidth, data.stepHeight, red)
    # Position the step on the left edge of the screen
    data.leftStep.rect.x = 0 
    data.leftStep.rect.y = data.height
    data.stepsList.add(data.leftStep)
    
    rightStepWidth = random.randint((data.width/2 + 2*data.spaceX), data.width)
    data.rightStep = Steps(rightStepWidth, data.stepHeight, red)
    # Position the step on the right edge of the screen
    data.rightStep.rect.x = rightStepWidth
    data.rightStep.rect.y = data.height 
    data.stepsList.add(data.rightStep)
    
    spaceWidth = data.rightStep.rect.x - leftStepWidth
    midStepWidth = spaceWidth - 2*data.spaceX
    data.midStep = Steps(midStepWidth, data.stepHeight, red)
    data.midStep.rect.x = leftStepWidth + data.spaceX
    data.midStep.rect.y = data.height
    data.stepsList.add(data.midStep)

def createRandRedStep(data):
    data.ballWidth = 40
    # The width of each step needs to be random
    data.stepHeight = 20
    (data.speedx, data.speedy) = (0, 5)
    # Minimum distance between two steps on top of each other
    data.spaceY = int(data.ballWidth * 1.75)
    data.spaceX = int(data.ballWidth * 1.25)
    
    # There should at most be 3 steps in each row
    numHoles = random.randint(1, 2)
    if (numHoles == 1):
        oneHoleRed(data)
    else:
        twoHolesRed(data)

def updateRedSteps(data):
    for step in data.stepsList:
        step.rect.y -= data.speedy
        if (step.rect.y + data.stepHeight == 0):
            data.stepsList.remove(step)

def trySpawnNewRedStep(data):
    data.lowest += data.speedy
    data.lowest %= data.spaceY
    if (data.lowest == 0):
        createRandRedStep(data)

#############
#   ORANGE  #
#############
def oneHoleOrange(data):
    orange = data.orangeColor
    randHolePos = random.randint(data.spaceX, data.width - data.spaceX)
    
    leftStepWidth = randHolePos - data.spaceX/2
    data.leftStep = Steps(leftStepWidth, data.stepHeight, orange)
    data.leftStep.rect.x = 0 
    data.leftStep.rect.y = data.height
    data.stepsList.add(data.leftStep)
    
    rightStepWidth = data.width - (randHolePos + data.spaceX/2)
    data.rightStep = Steps(rightStepWidth, data.stepHeight, orange)
    # Sets each step on the right side of the screen
    data.rightStep.rect.x = data.width - rightStepWidth 
    data.rightStep.rect.y = data.height 
    data.stepsList.add(data.rightStep)

def twoHolesOrange(data):
    orange = data.orangeColor
    leftStepWidth = random.randint(0, (data.width/2 - 2*data.spaceX))
    data.leftStep = Steps(leftStepWidth, data.stepHeight, orange)
    # Position the step on the left edge of the screen
    data.leftStep.rect.x = 0 
    data.leftStep.rect.y = data.height
    data.stepsList.add(data.leftStep)
    
    rightStepWidth = random.randint((data.width/2 + 2*data.spaceX), data.width)
    data.rightStep = Steps(rightStepWidth, data.stepHeight, orange)
    # Position the step on the right edge of the screen
    data.rightStep.rect.x = rightStepWidth
    data.rightStep.rect.y = data.height 
    data.stepsList.add(data.rightStep)
    
    spaceWidth = data.rightStep.rect.x - leftStepWidth
    midStepWidth = spaceWidth - 2*data.spaceX
    data.midStep = Steps(midStepWidth, data.stepHeight, orange)
    data.midStep.rect.x = leftStepWidth + data.spaceX
    data.midStep.rect.y = data.height
    data.stepsList.add(data.midStep)

def createRandOrangeStep(data):
    data.ballWidth = 40
    # The width of each step needs to be random
    data.stepHeight = 20
    (data.speedx, data.speedy) = (0, 5)
    # Minimum distance between two steps on top of each other
    data.spaceY = int(data.ballWidth * 1.75)
    data.spaceX = int(data.ballWidth * 1.25)
    
    # There should at most be 3 steps in each row
    numHoles = random.randint(1, 2)
    if (numHoles == 1):
        oneHoleOrange(data)
    else:
        twoHolesOrange(data)

def updateOrangeSteps(data):
    for step in data.stepsList:
        step.rect.y -= data.speedy
        if (step.rect.y + data.stepHeight == 0):
            data.stepsList.remove(step)

def trySpawnNewOrangeStep(data):
    data.lowest += data.speedy
    data.lowest %= data.spaceY
    if (data.lowest == 0):
        createRandOrangeStep(data)


#############
#  YELLOW   #
#############
def oneHoleYell(data):
    yellow = data.yellowColor
    randHolePos = random.randint(data.spaceX, data.width - data.spaceX)
    
    leftStepWidth = randHolePos - data.spaceX/2
    data.leftStep = Steps(leftStepWidth, data.stepHeight, yellow)
    data.leftStep.rect.x = 0 
    data.leftStep.rect.y = data.height
    data.stepsList.add(data.leftStep)
    
    rightStepWidth = data.width - (randHolePos + data.spaceX/2)
    data.rightStep = Steps(rightStepWidth, data.stepHeight, yellow)
    # Sets each step on the right side of the screen
    data.rightStep.rect.x = data.width - rightStepWidth 
    data.rightStep.rect.y = data.height 
    data.stepsList.add(data.rightStep)

def twoHolesYell(data):
    yellow = data.yellowColor
    leftStepWidth = random.randint(0, (data.width/2 - 2*data.spaceX))
    data.leftStep = Steps(leftStepWidth, data.stepHeight, yellow)
    # Position the step on the left edge of the screen
    data.leftStep.rect.x = 0 
    data.leftStep.rect.y = data.height
    data.stepsList.add(data.leftStep)
    
    rightStepWidth = random.randint((data.width/2 + 2*data.spaceX), data.width)
    data.rightStep = Steps(rightStepWidth, data.stepHeight, yellow)
    # Position the step on the right edge of the screen
    data.rightStep.rect.x = rightStepWidth
    data.rightStep.rect.y = data.height 
    data.stepsList.add(data.rightStep)
    
    spaceWidth = data.rightStep.rect.x - leftStepWidth
    midStepWidth = spaceWidth - 2*data.spaceX
    data.midStep = Steps(midStepWidth, data.stepHeight, yellow)
    data.midStep.rect.x = leftStepWidth + data.spaceX
    data.midStep.rect.y = data.height
    data.stepsList.add(data.midStep)

def createRandYellowStep(data):
    data.ballWidth = 40
    # The width of each step needs to be random
    data.stepHeight = 20
    (data.speedx, data.speedy) = (0, 5)
    # Minimum distance between two steps on top of each other
    data.spaceY = int(data.ballWidth * 1.75)
    data.spaceX = int(data.ballWidth * 1.25)
    
    # There should at most be 3 steps in each row
    numHoles = random.randint(1, 2)
    if (numHoles == 1):
        oneHoleYell(data)
    else:
        twoHolesYell(data)

def updateYellowSteps(data):
    for step in data.stepsList:
        step.rect.y -= data.speedy
        if (step.rect.y + data.stepHeight == 0):
            data.stepsList.remove(step)

def trySpawnNewYellowStep(data):
    data.lowest += data.speedy
    data.lowest %= data.spaceY
    if (data.lowest == 0):
        createRandYellowStep(data)

#############
#   GREEN   #
#############

def oneHoleGreen(data):
    green = data.greenColor
    randHolePos = random.randint(data.spaceX, data.width - data.spaceX)
    
    leftStepWidth = randHolePos - data.spaceX/2
    data.leftStep = Steps(leftStepWidth, data.stepHeight, green)
    data.leftStep.rect.x = 0 
    data.leftStep.rect.y = data.height
    data.stepsList.add(data.leftStep)
    
    rightStepWidth = data.width - (randHolePos + data.spaceX/2)
    data.rightStep = Steps(rightStepWidth, data.stepHeight, green)
    # Sets each step on the right side of the screen
    data.rightStep.rect.x = data.width - rightStepWidth 
    data.rightStep.rect.y = data.height 
    data.stepsList.add(data.rightStep)

def twoHolesGreen(data):
    green = data.greenColor
    leftStepWidth = random.randint(0, (data.width/2 - 2*data.spaceX))
    data.leftStep = Steps(leftStepWidth, data.stepHeight, green)
    # Position the step on the left edge of the screen
    data.leftStep.rect.x = 0 
    data.leftStep.rect.y = data.height
    data.stepsList.add(data.leftStep)
    
    rightStepWidth = random.randint((data.width/2 + 2*data.spaceX), data.width)
    data.rightStep = Steps(rightStepWidth, data.stepHeight, green)
    # Position the step on the right edge of the screen
    data.rightStep.rect.x = rightStepWidth
    data.rightStep.rect.y = data.height 
    data.stepsList.add(data.rightStep)
    
    spaceWidth = data.rightStep.rect.x - leftStepWidth
    midStepWidth = spaceWidth - 2*data.spaceX
    data.midStep = Steps(midStepWidth, data.stepHeight, green)
    data.midStep.rect.x = leftStepWidth + data.spaceX
    data.midStep.rect.y = data.height
    data.stepsList.add(data.midStep)

def createRandGreenStep(data):
    data.ballWidth = 40
    # The width of each step needs to be random
    data.stepHeight = 20
    (data.speedx, data.speedy) = (0, 5)
    # Minimum distance between two steps on top of each other
    data.spaceY = int(data.ballWidth * 1.75)
    data.spaceX = int(data.ballWidth * 1.25)
    
    # There should at most be 3 steps in each row
    numHoles = random.randint(1, 2)
    if (numHoles == 1):
        oneHoleGreen(data)
    else:
        twoHolesGreen(data)

def updateGreenSteps(data):
    for step in data.stepsList:
        step.rect.y -= data.speedy
        if (step.rect.y + data.stepHeight == 0):
            data.stepsList.remove(step)

def trySpawnNewGreenStep(data):
    data.lowest += data.speedy
    data.lowest %= data.spaceY
    if (data.lowest == 0):
        createRandGreenStep(data)

#############
#   BLUE    #
#############
def oneHoleBlue(data):
    blue = data.blueColor
    randHolePos = random.randint(data.spaceX, data.width - data.spaceX)
    
    leftStepWidth = randHolePos - data.spaceX/2
    data.leftStep = Steps(leftStepWidth, data.stepHeight, blue)
    data.leftStep.rect.x = 0 
    data.leftStep.rect.y = data.height
    data.stepsList.add(data.leftStep)
    
    rightStepWidth = data.width - (randHolePos + data.spaceX/2)
    data.rightStep = Steps(rightStepWidth, data.stepHeight, blue)
    # Sets each step on the right side of the screen
    data.rightStep.rect.x = data.width - rightStepWidth 
    data.rightStep.rect.y = data.height 
    data.stepsList.add(data.rightStep)

def twoHolesBlue(data):
    blue = data.blueColor
    leftStepWidth = random.randint(0, (data.width/2 - 2*data.spaceX))
    data.leftStep = Steps(leftStepWidth, data.stepHeight, blue)
    # Position the step on the left edge of the screen
    data.leftStep.rect.x = 0 
    data.leftStep.rect.y = data.height
    data.stepsList.add(data.leftStep)
    
    rightStepWidth = random.randint((data.width/2 + 2*data.spaceX), data.width)
    data.rightStep = Steps(rightStepWidth, data.stepHeight, blue)
    # Position the step on the right edge of the screen
    data.rightStep.rect.x = rightStepWidth
    data.rightStep.rect.y = data.height 
    data.stepsList.add(data.rightStep)
    
    spaceWidth = data.rightStep.rect.x - leftStepWidth
    midStepWidth = spaceWidth - 2*data.spaceX
    data.midStep = Steps(midStepWidth, data.stepHeight, blue)
    data.midStep.rect.x = leftStepWidth + data.spaceX
    data.midStep.rect.y = data.height
    data.stepsList.add(data.midStep)

def createRandBlueStep(data):
    data.ballWidth = 40
    # The width of each step needs to be random
    data.stepHeight = 20
    (data.speedx, data.speedy) = (0, 5)
    # Minimum distance between two steps on top of each other
    data.spaceY = int(data.ballWidth * 1.75)
    data.spaceX = int(data.ballWidth * 1.25)
    
    # There should at most be 3 steps in each row
    numHoles = random.randint(1, 2)
    if (numHoles == 1):
        oneHoleBlue(data)
    else:
        twoHolesBlue(data)

def updateBlueSteps(data):
    for step in data.stepsList:
        step.rect.y -= data.speedy
        if (step.rect.y + data.stepHeight == 0):
            data.stepsList.remove(step)

def trySpawnNewBlueStep(data):
    data.lowest += data.speedy
    data.lowest %= data.spaceY
    if (data.lowest == 0):
        createRandBlueStep(data)

#############
#  INDIGO   #
#############
def oneHoleIndigo(data):
    indigo = data.indigoColor
    randHolePos = random.randint(data.spaceX, data.width - data.spaceX)
    
    leftStepWidth = randHolePos - data.spaceX/2
    data.leftStep = Steps(leftStepWidth, data.stepHeight, indigo)
    data.leftStep.rect.x = 0 
    data.leftStep.rect.y = data.height
    data.stepsList.add(data.leftStep)
    
    rightStepWidth = data.width - (randHolePos + data.spaceX/2)
    data.rightStep = Steps(rightStepWidth, data.stepHeight, indigo)
    # Sets each step on the right side of the screen
    data.rightStep.rect.x = data.width - rightStepWidth 
    data.rightStep.rect.y = data.height 
    data.stepsList.add(data.rightStep)

def twoHolesIndigo(data):
    indigo = data.indigoColor
    leftStepWidth = random.randint(0, (data.width/2 - 2*data.spaceX))
    data.leftStep = Steps(leftStepWidth, data.stepHeight, indigo)
    # Position the step on the left edge of the screen
    data.leftStep.rect.x = 0 
    data.leftStep.rect.y = data.height
    data.stepsList.add(data.leftStep)
    
    rightStepWidth = random.randint((data.width/2 + 2*data.spaceX), data.width)
    data.rightStep = Steps(rightStepWidth, data.stepHeight, indigo)
    # Position the step on the right edge of the screen
    data.rightStep.rect.x = rightStepWidth
    data.rightStep.rect.y = data.height 
    data.stepsList.add(data.rightStep)
    
    spaceWidth = data.rightStep.rect.x - leftStepWidth
    midStepWidth = spaceWidth - 2*data.spaceX
    data.midStep = Steps(midStepWidth, data.stepHeight, indigo)
    data.midStep.rect.x = leftStepWidth + data.spaceX
    data.midStep.rect.y = data.height
    data.stepsList.add(data.midStep)

def createRandIndyStep(data):
    data.ballWidth = 40
    # The width of each step needs to be random
    data.stepHeight = 20
    (data.speedx, data.speedy) = (0, 5)
    # Minimum distance between two steps on top of each other
    data.spaceY = int(data.ballWidth * 1.75)
    data.spaceX = int(data.ballWidth * 1.25)
    
    # There should at most be 3 steps in each row
    numHoles = random.randint(1, 2)
    if (numHoles == 1):
        oneHoleIndigo(data)
    else:
        twoHolesIndigo(data)

def updateIndySteps(data):
    for step in data.stepsList:
        step.rect.y -= data.speedy
        if (step.rect.y + data.stepHeight == 0):
            data.stepsList.remove(step)

def trySpawnNewIndyStep(data):
    data.lowest += data.speedy
    data.lowest %= data.spaceY
    if (data.lowest == 0):
        createRandIndyStep(data)

#############
#   VIOLET  #
#############
def oneHoleViolet(data):
    violet = data.violetColor
    randHolePos = random.randint(data.spaceX, data.width - data.spaceX)
    
    leftStepWidth = randHolePos - data.spaceX/2
    data.leftStep = Steps(leftStepWidth, data.stepHeight, violet)
    data.leftStep.rect.x = 0 
    data.leftStep.rect.y = data.height
    data.stepsList.add(data.leftStep)
    
    rightStepWidth = data.width - (randHolePos + data.spaceX/2)
    data.rightStep = Steps(rightStepWidth, data.stepHeight, violet)
    # Sets each step on the right side of the screen
    data.rightStep.rect.x = data.width - rightStepWidth 
    data.rightStep.rect.y = data.height 
    data.stepsList.add(data.rightStep)

def twoHolesViolet(data):
    violet = data.violetColor
    leftStepWidth = random.randint(0, (data.width/2 - 2*data.spaceX))
    data.leftStep = Steps(leftStepWidth, data.stepHeight, violet)
    # Position the step on the left edge of the screen
    data.leftStep.rect.x = 0 
    data.leftStep.rect.y = data.height
    data.stepsList.add(data.leftStep)
    
    rightStepWidth = random.randint((data.width/2 + 2*data.spaceX), data.width)
    data.rightStep = Steps(rightStepWidth, data.stepHeight, violet)
    # Position the step on the right edge of the screen
    data.rightStep.rect.x = rightStepWidth
    data.rightStep.rect.y = data.height 
    data.stepsList.add(data.rightStep)
    
    spaceWidth = data.rightStep.rect.x - leftStepWidth
    midStepWidth = spaceWidth - 2*data.spaceX
    data.midStep = Steps(midStepWidth, data.stepHeight, violet)
    data.midStep.rect.x = leftStepWidth + data.spaceX
    data.midStep.rect.y = data.height
    data.stepsList.add(data.midStep)

def createRandVioletStep(data):
    data.ballWidth = 40
    # The width of each step needs to be random
    data.stepHeight = 20
    (data.speedx, data.speedy) = (0, 5)
    # Minimum distance between two steps on top of each other
    data.spaceY = int(data.ballWidth * 1.75)
    data.spaceX = int(data.ballWidth * 1.25)
    
    # There should at most be 3 steps in each row
    numHoles = random.randint(1, 2)
    if (numHoles == 1):
        oneHoleViolet(data)
    else:
        twoHolesViolet(data)

def updateVioletSteps(data):
    for step in data.stepsList:
        step.rect.y -= data.speedy
        if (step.rect.y + data.stepHeight == 0):
            data.stepsList.remove(step)

def trySpawnNewVioletStep(data):
    data.lowest += data.speedy
    data.lowest %= data.spaceY
    if (data.lowest == 0):
        createRandVioletStep(data)

def changeColor(data):
    if (data.level == 1):
        updateRedSteps(data)
        trySpawnNewRedStep(data)
    elif (data.level == 2):
        updateOrangeSteps(data)
        trySpawnNewOrangeStep(data)
    elif (data.level == 3):
        updateYellowSteps(data)
        trySpawnNewYellowStep(data)
    elif (data.level == 4):
        updateGreenSteps(data)
        trySpawnNewGreenStep(data)
    elif (data.level == 5):
        updateBlueSteps(data)
        trySpawnNewBlueStep(data)
    elif(data.level == 6):
        updateIndySteps(data)
        trySpawnNewIndyStep(data)
    else:
        updateVioletSteps(data)
        trySpawnNewVioletStep(data)

def changeLevel(data):
    data.timeElapsed += data.clock.tick(data.FPS)
    if (data.timeElapsed > data.timeForLevelChange):
        print "new level!"
        data.FPS += 20
        data.level += 1
        data.timeElapsed = 0
        data.timeElapsed = 0

###############
## POWER UPS ##
###############

# freeze screen for 5s (3rd most common)
# +5 points (most common)
# kill enemy (least common)
# increase ball speed (2nd most common)

# also have to determine how often a powerup is placed on the screen
    # if random.randint(1, 4) == 1 then decide on powerup

class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("powerup.png", -1)
        self.area = self.image.get_rect()
        self.width = self.area.width
        self.randNum = random.randint(1, 10)
        # randomly generate a loc to place powerup; has to be on a step
        # 1, 2, 3 --> +5 points
        # 4, 5, 6 --> increase ball speed
        # 7, 8 --> freeze
        # 9, 10 --> kill enemy (only appear if there's an enemy on screen??)
    def genLocation(self):
        # randomly generate a location to place the powerup
        pass
    def draw(self, position):
        # draw powerup to screen
        # make sure it's sitting on a step
        pass
    def remove(self):
        # if ball collides with powerup, remove from screen
        pass

class addPoints(Powerup):
    def whenToSpawn(self):
        Powerup().genPowerup() #???
        if (self.randNum == 1) or (self.randNum == 2) or (self.randNum == 3):
            # screen.blit(somewhere)
            pass

class freezeScreen(Powerup):
    def whenToSpawn(self):
        if (self.randNum == 7) or (self.randNum == 8):      
            pass

class incBallSpeed(Powerup):
    def whenToSpawn(self):
        if (self.randNum == 4) or (self.randNum == 5) or (self.randNum == 6):
            # screen.blit(somewhere)
            pass

class killEnemy(Powerup):
    def whenToSpawn(self):
        if (self.randNum == 9) or (self.randNum == 10):
            # screen.blit(somewhere)
            pass



def mousePressed(event, data):
    print "Mouse Pressed"
    redrawAll(data)

def keyPressed(event, data):
    if (event.key == pygame.K_LEFT):    
        if not data.paused:
            data.ball.moveLeft()
        
    elif (event.key == pygame.K_RIGHT):
        if not data.paused:
            data.ball.moveRight(data)
    elif (event.key == pygame.K_p):
        data.paused = not data.paused
        # takes player to pause screen 

def keyUnpressed(event, data):
    # If the keys are not being pressed, the ball stops moving
    if (event.key == K_LEFT) or (event.key == K_DOWN):
        data.ball.speedx = 0
        data.ball.speedy = 0

def gameOver(data):
    if (data.ball.rect.top <= 0):
        data.ballDiesSound.play()
        win(data)
    if (data.level == 8):
        win(data)

# Check for win
def win(data):
    data.mode = "Done"
    # win screen, etc.
    # pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                data.mode = "Done"

def drawScore(data):
    fontHeight = 25
    scoreFont = pygame.font.Font("Font/Level_Score.ttf", fontHeight)
    label = scoreFont.render("Score: %d" % (data.score), 1, data.whiteText) 
    data.screen.blit(label, (0, 0))

def updateScore(data):
    data.timeElapsedScore += data.clock.tick(data.FPS)
    if (data.timeElapsedScore > data.timeToChangeScore):
        data.score += 1
        data.timeElapsedScore = 0

def drawLevel(data):
    fontHeight = 25
    levelFont = pygame.font.Font("Font/Level_Score.ttf", fontHeight)
    label = levelFont.render("Level: %d" %(data.level), 1, data.whiteText)
    data.screen.blit(label, (data.width*.8, 0))
  
def timerFired(data):
    redrawAll(data)
    data.clock.tick(data.FPS)
    data.mousePos = pygame.mouse.get_pos()
    data.ball.ballStepsColl(data)
    data.enemy.movingLeft(data)
    data.enemy.movingRight(data)
    data.enemy.enemyCollSteps(data)
    changeLevel(data)
    updateScore(data)
    gameOver(data)

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            data.mode = "Done"
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            mousePressed(event, data)
        elif (event.type == pygame.KEYDOWN):
            keyPressed(event, data)
   
def redrawAll(data):
    data.ballSprite.update()
    data.screen.blit(data.background, (0, 0))
    data.ballSprite.draw(data.screen)
    data.stepsList.draw(data.screen)
    if (data.level > 1):
        data.enemySprite.draw(data.screen)
    drawScore(data)
    drawLevel(data)
    changeColor(data)
    
    pygame.display.update()
    pygame.display.flip()

def initSounds(data):
    data.themeSound = pygame.mixer.Sound("Sounds/fallDown.wav")
    data.bounceSound = pygame.mixer.Sound("Sounds/fx/ballbounce.wav")
    data.chachingSound = pygame.mixer.Sound("Sounds/fx/chaching.wav")
    data.freezeSound = pygame.mixer.Sound("Sounds/fx/freeze.wav")
    data.enemyKilledSound = pygame.mixer.Sound("Sounds/fx/pewpew.wav")
    data.ballDiesSound = pygame.mixer.Sound("Sounds/fx/squish.wav")
    data.ballSpeedsUpSound = pygame.mixer.Sound("Sounds/fx/zoom.wav")

    # Loops through theme song forever
    data.themeSound.play(-1)

def initSteps(data):
    # Creating a sprites group for all the steps
    data.stepsList = pygame.sprite.Group()
    data.lowest = 0
    data.whiteText = (255, 255, 255)
    data.redColor = (255, 0, 60)
    data.orangeColor = (255, 96, 0)
    data.yellowColor = (255, 192, 0)
    data.greenColor = (52, 224, 125)
    data.blueColor = (0, 124, 229)
    data.indigoColor = (41, 60, 240)
    data.violetColor = (111, 57, 234)
    
    createRandRedStep(data)
    updateRedSteps(data)
    
def initBall(data):
    data.ball = Ball()
    data.ballSprite = pygame.sprite.RenderPlain(data.ball)
    data.ball.moveRight(data)
    #data.ball.addGravity(data)

def initEnemy(data):
    data.enemy = Enemy()
    data.enemySprite = pygame.sprite.RenderPlain(data.enemy)

def initPowerups(data):
    data.powerupsList = pygame.sprite.Group()

def initTimes(data):
    data.timeElapsed = 0
    data.timeElapsedScore = 0
    data.timeForLevelChange = 15000
    data.timeToChangeScore = 250

def initBackground(data):
    data.screen = pygame.display.get_surface()
    # data.background = load_image("menusplash.png", -1)
    # data.background = pygame.Surface(data.screenSize)
    # data.background = pygame.transform.smoothscale(data.background, data.screenSize)
    
    data.background = pygame.Surface(data.screen.get_size())
    data.background = data.background.convert()
    data.background.fill((0, 0, 0))

def init(data):
    data.mode = "Running"
    # Frames per second
    data.FPS = 30 
    data.score = 0
    data.level = 1
    # Hides or shows the cursor by taking in a bool
    pygame.mouse.set_visible(0)
    data.keyHeld = False
    data.paused = False

    initTimes(data)
    initSteps(data)
    initBall(data)
    initEnemy(data)
    initPowerups(data)
    initSounds(data)
    initBackground(data)
    

def run():
    pygame.init()
    class Struct: pass
    data = Struct()
    # Initialize screen
    (data.width, data.height) = (350, 500)
    data.screenSize = (data.width, data.height)
    data.screen = pygame.display.set_mode(data.screenSize)
    pygame.display.set_caption("FallDown!")
    # Initialize clock
    data.clock = pygame.time.Clock()
    init(data)
    timerFired(data)
    while (data.mode != "Done"):
        if not data.paused:
            timerFired(data)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                data.mode = "Done"
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                mousePressed(event, data)
            elif (event.type == pygame.KEYDOWN):
                keyPressed(event, data)
            elif (event.type == pygame.KEYUP):
                keyUnpressed(event, data)

run()
