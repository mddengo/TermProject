# Michelle Deng + mdeng +
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
        margin = 7
        isColliding = False
        for step in data.stepsList:
            if (len(step.rect.collidelistall([self])) > 0):
                isColliding = True
        if (isColliding):
            #self.handleCollision(data)
            self.rect = self.rect.move(0, -data.speedy)
            if not self.wasColliding:
                data.bounceSound.play()
                data.bounceSound.set_volume(0.45)
                self.wasColliding = True
        elif ((self.rect.y + margin) > (data.height - self.height)):
            pass   
        else:
            self.wasColliding = False
            self.rect = self.rect.move(0, self.gravity)
    
    def handleCollision(self, data):
    # right clip
    # left clip
    # top clip
    # bottom clip
    # correct for collisions
        for step in data.stepsList:
            bottomClip = (data.stepHeight - (self.height/2))
            print "bottom clip: ", bottomClip/4
            if (self.rect.bottom > step.rect.y):
                self.rect.bottom -= bottomClip/4
            else:
                pass

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
    
    # There should be at most 3 steps in each row
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
        data.FPS += 18
        data.level += 1
        data.timeElapsed = 0

def drawPause(data):
    data.pauseSplash = pygame.image.load("pausesplash.png").convert_alpha()
    data.pauseSplash = pygame.transform.smoothscale(data.pauseSplash, data.screenSize)
    data.screen.blit(data.pauseSplash, (0,0))

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
        # Takes player to pause screen
        drawPause(data)
        pygame.display.update()
    elif (data.menuActive == True) and (event.key == pygame.K_SPACE) :
        data.screen.blit(data.menuPlayPressed, (data.xpos, data.playYPos))
        pygame.display.update()
        pygame.display.flip()
        data.paused = False
        data.menuActive = False
    elif (event.key == pygame.K_r):
        # The following two lines could not have been possible without
        # http://www.daniweb.com/software-development/python/code/260268/restart-your-python-program
        # This will restart the game
        python = sys.executable
        os.execl(python, python, * sys.argv)

def drawGameOver(data):
    data.ggSplash = pygame.image.load("ggsplash.png").convert_alpha()
    data.ggSplash = pygame.transform.smoothscale(data.ggSplash, data.screenSize)
    data.screen.blit(data.ggSplash, (0,0))

def drawFinalScoreText(data):
    scoreFontHeight = 45
    scoreFont = pygame.font.Font("Font/Level_Score.ttf", scoreFontHeight)
    label = scoreFont.render("Final Score:", 1, data.whiteText) 
    data.screen.blit(label, (data.width/4, data.height*.45))

def gameOver(data):
    if (data.ball.rect.top <= 0):
        data.ballDiesSound.play()
        win(data)
    if (data.level == 8):
        win(data)

# Check for win
def win(data):
    data.mode = "Done"
    data.gameOver = True
    # win screen, etc.
    data.screen.fill((0, 0, 0))
    drawGameOver(data)
    drawFinalScoreText(data)
    fontHeight = 35
    scoreFont = pygame.font.Font("Font/Level_Score.ttf", fontHeight)
    label = scoreFont.render("%d" % (data.score), 1, data.whiteText)
    data.screen.blit(label, (data.width*.45, data.height*.55))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                data.mode = "Done"
                data.gameOver = True
                pygame.quit()
            elif (event.type == pygame.KEYDOWN):
                keyPressed(event, data)      

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

def drawMenu(data):
    data.menuActive = True
    data.menuScreen = pygame.image.load("menusplashwtitle.png").convert_alpha()
    data.menuScreen = pygame.transform.smoothscale(data.menuScreen, data.screenSize)
    data.screen.blit(data.menuScreen, (0,0))
    if (data.iconWidth > data.iconMaxWidth):
        data.iconWidth = data.iconMaxWidth
    if (data.iconHeight > data.iconMaxHeight):
        data.iconHeight = data.iconMaxHeight 
    # Load icons
    data.menuPlay = pygame.image.load("menuPlayTxt.png").convert_alpha()
    data.menuPlayPressed = pygame.image.load("menuplay_pressed.png").convert_alpha()

    # Scale icons
    data.menuPlay = pygame.transform.smoothscale(data.menuPlay, data.iconSize)
    data.menuPlayPressed = pygame.transform.smoothscale(data.menuPlayPressed,
        data.iconSize)
    # Display button
    data.screen.blit(data.menuPlay, (data.xpos, data.playYPos))

    fontHeight = 25
    font = pygame.font.Font("Font/Level_Score.ttf", fontHeight)
    label = font.render("Press the space bar to play", 1, data.whiteText)
    data.screen.blit(label, (data.width*.2, data.height*.75))
    
def timerFired(data):
    redrawAll(data)
    data.clock.tick(data.FPS)
    data.ball.ballStepsColl(data)
    
    changeLevel(data)
    updateScore(data)
    gameOver(data)

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            data.gameOver = True
            pygame.quit()
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            mousePressed(event, data)
        elif (event.type == pygame.KEYDOWN):
            keyPressed(event, data)
   
def redrawAll(data):
    data.ballSprite.update()
    data.screen.blit(data.background, (0, 0))
    data.ballSprite.draw(data.screen)
    data.stepsList.draw(data.screen)

    drawScore(data)
    drawLevel(data)
    changeColor(data)

    if (data.menuActive != False):
        data.paused = True
        drawMenu(data)
    pygame.display.update()
    pygame.display.flip()

def initSounds(data):
    data.themeSound = pygame.mixer.Sound("Sounds/fallDown.wav")
    data.bounceSound = pygame.mixer.Sound("Sounds/fx/ballbounce.wav")
    data.ballDiesSound = pygame.mixer.Sound("Sounds/fx/squish.wav")

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

def initTimes(data):
    data.timeElapsed = 0
    data.timeElapsedScore = 0
    data.timeForLevelChange = 18000
    data.timeToChangeScore = 250

def initButtons(data):
    data.iconMaxWidth = 375
    data.iconMaxHeight = 105
    data.iconWidth = int(0.7 * data.width)
    data.iconHeight = int(0.4 * data.height)
    data.iconSize = (data.iconWidth, data.iconHeight)

def initMenuButts(data):
    data.xpos = data.width*.15  
    data.playYPos = data.height*.4 

def initBackground(data):
    data.screen = pygame.display.get_surface()
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
    data.paused = False
    data.menuActive = True
    data.gameOver = False
    initTimes(data)
    initSteps(data)
    initBall(data)
    initSounds(data)
    initBackground(data)
    initButtons(data)
    initMenuButts(data)
    drawMenu(data)
    

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
        data.gameOver = False
        if not data.paused:
            timerFired(data)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                data.gameOver = True
                pygame.quit()
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                mousePressed(event, data)
            elif (event.type == pygame.KEYDOWN):
                keyPressed(event, data)
              


run()
