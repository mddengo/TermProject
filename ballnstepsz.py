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

class Screens(object):
    def __init__(self):
        # Draws screens and buttons
        pass
    def draw(self, screen, screenWidth, screenHeight, image):
        image = pygame.Surface([screenWidth, screenHeight])
        image = pygame.transform.smoothscale(image, (screenWidth,screenHeight))
        screen.blit(image, (0,0))
    
# Draws menu splash screen with buttons   
class MenuScreen(Screens):
    def __init__(self, screenWidth, screenHeight):
        self.menuSplash = load_image("menusplashwtitle.png")
        iconMaxWidth = 275
        iconMaxHeight = 150
        self.buttonPressed = False
        self.active = False
        self.iconWidth = int(0.4 * screenWidth)
        self.iconHeight = int(0.2 * screenHeight)
        self.iconSize = (self.iconWidth, self.iconHeight)

        self.menuPlay = load_image("menuPlayTxt.png", -1)
        self.menuPlay = pygame.Surface(self.iconSize)
        self.menuPlayPressed = load_image("menuplay_pressed.png", -1)
        self.menuPlayPressed = pygame.Surface(self.iconSize)
        self.menuTut = load_image("menututTxt.png", -1)
        self.menuTut = pygame.Surface(self.iconSize)
        self.menuTutPressed = load_image("menutut_pressed.png", -1)
        self.menuTutPressed = pygame.Surface(self.iconSize)
        self.menuCreds = load_image("menucredsTxt.png", -1)
        self.menuCreds = pygame.Surface(self.iconSize)
        self.menuCredsPressed = load_image("menucreds_pressed.png", -1)
        self.menuCredsPressed = pygame.Surface(self.iconSize)

        if (self.iconWidth > iconMaxWidth):
            self.iconWidth = iconMaxWidth
        if (self.iconHeight > iconMaxHeight):
            self.iconHeight = iconMaxHeight
        
        # Scale icons
        self.menuPlay = pygame.transform.smoothscale(self.menuPlay,
                                                     self.iconSize)
        self.menuTut = pygame.transform.smoothscale(self.menuTut, self.iconSize)
        self.menuCreds = pygame.transform.smoothscale(self.menuCreds,
                                                      self.iconSize)
        # Scale pressed icons
        self.menuPlayPressed = pygame.transform.smoothscale(self.menuPlayPressed,
                                                            self.iconSize)
        self.menuTutPressed = pygame.transform.smoothscale(self.menuTutPressed,
                                                           self.iconSize)
        self.menuCredsPressed = pygame.transform.smoothscale(self.menuCredsPressed,
                                                             self.iconSize)

    def draw(self, screen, screenWidth, screenHeight):
        pygame.mouse.set_visible(1)
        # Draw menu screen
        Screens().draw(screen, screenWidth, screenHeight, self.menuSplash)
        
        # Position buttons
        playPos = (int(0.5 * screenWidth), int(0.35 * screenHeight))
        tutPos = (int(0.5 * screenWidth),
                  int(0.35 * screenHeight + 1.25 * self.iconHeight))
        credsPos = (int(0.5 * screenWidth),
                    int(0.70 * screenHeight + 0.25 * self.iconHeight))
        
        # Show pressed state when button is clicked
        if not(self.buttonPressed):
            screen.blit(self.menuPlay, playPos)
            screen.blit(self.menuTut, tutPos)
            screen.blit(self.menuCreds, credsPos)
        else:
            screen.blit(self.menuPlayPressed, playPos)
            screen.blit(self.menuTutPressed, tutPos)
            screen.blit(self.menuCredsPressed, credsPos)

    def updateAll(self, screenWidth, screenHeight):
        (mouseClickX, mouseClickY) = pygame.mouse.get_pos()
        playPos = (int(0.5 * screenWidth), int(0.35 * screenHeight))
        tutPos = (int(0.5 * screenWidth),
                  int(0.35 * screenHeight + 1.25 * self.iconHeight))
        credsPos = (int(0.5 * screenWidth),
                    int(0.70 * screenHeight + 0.25 * self.iconHeight))
        # Store icon coordinates (top left & bottom right)
        self.playCoords = [playPos, (playPos[0] + self.iconWidth, playPos[1] +
                                     self.iconHeight)]
        self.tutCoords = [tutPos, (tutPos[0] + self.iconWidth, tutPos[1] +
                                   self.iconHeight)]
        self.credsCoords = [credsPos, (credsPos[0] + self.iconWidth, credsPos[1] +
                                       self.iconHeight)]
        
        # Check if player clicks the icons
        if ((mouseClickX < self.playCoords[1][0]) and
            (mouseClickX > self.playCoords[0][0])):
                if ((mouseClickY < self.playCoords[1][1]) and
                    (mouseClickY > self.playCoords[0][1])):
                    self.buttonPressed = True
                    return
        elif ((mouseClickX < self.tutCoords[1][0]) and
            (mouseClickX > self.tutCoords[0][0])):
            if ((mouseClickY < self.tutCoords[0][1])):
                self.buttonPressed = True
                return
        elif ((mouseClickX < self.credsCoords[1][0]) and
            (mouseClickX > self.credsCoords[0][0])):
            if ((mouseCLickY < self.credsCoords[0][1])):
                self.buttonPressed = True
                return
        self.buttonPressed = False
        
    def clicked(self):
        return self.buttonPressed
    
class Paused(Screens):
    def __init__(self, screenWidth, screenHeight):
        self.pausedSplash = load_image("pausesplash.png", -1)

    def draw(self, screen, screenWidth, screenHeight):
        Screens().draw(screen, screenWidth, screenHeight,
                                 self.pausedSplash)

class GameOver(Screens):
    def __init__(self, screenWidth, screenHeight):
        self.ggScreen = load_image("ggsplash.png", -1)
        iconMaxWidth = 275
        iconMaxHeight = 150
            
        self.iconWidth = int(0.4 * screenWidth)
        self.iconHeight = int(0.2 * screenHeight)
        self.iconSize = [self.iconWidth, self.iconHeight]

        self.buttonPressed = False
        self.menuPressed = load_image("menubutt-pressed.png", -1)
        self.menuPressed = pygame.Surface(self.iconSize)
        self.menuButt = load_image("menubutt.png", -1)
        self.menuButt = pygame.Surface(self.iconSize)
        self.playPressed = load_image("menuplay_pressed.png", -1)
        self.playPressed = pygame.Surface(self.iconSize)
        self.playButt = load_image("menuplayTxt.png", -1)
        self.playButt = pygame.Surface(self.iconSize)

        if (self.iconWidth > iconMaxWidth):
            self.iconWidth = iconMaxWidth
        if (self.iconHeight > iconMaxHeight):
            self.iconHeight = iconMaxHeight
        # Scale icons
        self.menuButt = pygame.transform.smoothscale(self.menuButt,
                                                     self.iconSize)
        self.playButt = pygame.transform.smoothscale(self.playButt,
                                                     self.iconSize)
        # Scale pressed icons
        self.menuPressed = pygame.transform.smoothscale(self.menuPressed,
                                                            self.iconSize)
        self.playPressed = pygame.transform.smoothscale(self.playPressed,
                                                     self.iconSize)
    def draw(self, screen, screenWidth, screenHeight):
        pygame.mouse.set_visible(1)
        Screens().draw(screen, screenWidth, screenHeight, self.ggScreen)
        # Position buttons
        menuPos = (int(0.25 * screenWidth), int(0.85 * screenHeight))
        playPos = (int(0.75 * screenWidth), int(0.85 * screenHeight))
        # Show pressed state when button is clicked
        if not(self.buttonPressed):
            screen.blit(self.menuButt, menuPos)
            screen.blit(self.playButt, playPos)
        else:
            screen.blit(self.menuPressed, menuPos)
            screen.blit(self.playPressed, playPos)

    def updateAll(self):
        (mouseClickX, mouseClickY) = pygame.mouse.get_pos()
        # Store icon coordinates (top left & bottom right)
        self.menuCoords = [menuPos, (menuPos[0] + self.iconSize, pos[1] +
                                     self.iconSize)]
        self.playCoords = [playPos, (playPos[0] + self.iconSize, pos[1] +
                                    self.iconSize)]
        # Check if player clicks the icons
        if ((mouseClickX < self.menuCoords[1][0]) and
            (mouseClickX > self.menuCoords[0][0])):
                if ((mouseClickY < self.menuCoords[1][1]) and
                    (mouseClickY > self.menuCoords[0][1])):
                    self.buttonPressed = True
                    return
        elif ((mouseClickX < self.playCoords[1][0]) and 
            (mouseClickX > self.playCoords[0][0])):
            if ((mouseClickY < self.playCoords[1][1]) and
                (mouseClickY > self.playCoords[0][1])):
                self.buttonPressed = True
                return 
        self.buttonPressed = False

    def clicked(self):
        return self.buttonPressed

class Tutorial(Screens):
    def __init__(self, screenWidth, screenHeight):
        self.tutScreen = load_image("tutsplash.png", -1)
        iconMaxWidth = 275
        iconMaxHeight = 150
        self.iconWidth = int(0.5 * screenWidth)
        self.iconHeight = int(0.2 * screenHeight)
        self.iconSize = (self.iconWidth, self.iconHeight)
        self.buttonPressed = False

        self.menuPressed = load_image("menubutt-pressed.png", -1)
        self.menuPressed = pygame.Surface(self.iconSize)
        self.menuButt = load_image("menubutt.png", -1)
        self.menuButt = pygame.Surface(self.iconSize)
        self.playPressed = load_image("menuplay_pressed.png", -1)
        self.playPressed = pygame.Surface(self.iconSize)
        self.playButt = load_image("menuplayTxt.png", -1)
        self.playButt = pygame.Surface(self.iconSize)

        if (self.iconWidth > iconMaxWidth):
            self.iconWidth = iconMaxWidth
        if (self.iconHeight > iconMaxHeight):
            self.iconHeight = iconMaxHeight
        # Scale icons
        self.menuButt = pygame.transform.smoothscale(self.menuButt,
                                                     self.iconSize)
        self.playButt = pygame.transform.smoothscale(self.playButt,
                                                     self.iconSize)
        # Scale pressed icons
        self.menuPressed = pygame.transform.smoothscale(self.menuPressed,
                                                            self.iconSize)
        self.playPressed = pygame.transform.smoothscale(self.playPressed,
                                                     self.iconSize)

    def draw(self, screen, screenWidth, screenHeight):
        pygame.mouse.set_visible(1)
        Screens().draw(screen, screenWidth, screenHeight, self.credsScreen)
        # Position buttons
        menuPos = (int(0.25 * screenWidth), int(0.9 * screenHeight))
        playPos = (int(0.75 * screenWidth), int(0.9 * screenHeight))
        
        # Show pressed state when button is clicked
        if not(self.buttonPressed):
            screen.blit(self.menuButt, menuPos)
            screen.blit(self.playButt, playPos)
        else:
            screen.blit(self.menuPressed, menuPos)
            screen.blit(self.playPressed, playPos)

    def updateAll(self):
        (mouseClickX, mouseClickY) = pygame.mouse.get_pos()
        
        # Store icon coordinates (top left & bottom right)
        self.menuCoords = [menuPos, (menuPos[0] + self.iconSize, pos[1] +
                                     self.iconSize)]
        self.playCoords = [playPos, (playPos[0] + self.iconSize, pos[1] +
                                    self.iconSize)]
        
        # Check if player clicks the icons
        if ((mouseClickX < self.menuCoords[1][0]) and
            (mouseClickX > self.menuCoords[0][0])):
                if ((mouseClickY < self.menuCoords[1][1]) and
                    (mouseClickY > self.menuCoords[0][1])):
                    self.buttonPressed = True
                    return
        elif ((mouseClickX < self.playCoords[1][0]) and 
            (mouseClickX > self.playCoords[0][0])):
            if ((mouseClickY < self.playCoords[1][1]) and
                (mouseClickY > self.playCoords[0][1])):
                self.buttonPressed = True
                return 
        self.buttonPressed = False

    def clicked(self):
        return self.buttonPressed
    
class Creds(Screens):
    def __init__(self):
        self.credsScreen = load_image("credssplash.png", -1)
        iconMaxWidth = 275
        iconMaxHeight = 150
        
        self.buttonPressed = False
        self.menuPressed = load_image("menubutt-pressed.png", -1)
        self.menuButt = load_image("menubutt.png", -1)
        self.iconWidth = int(0.3 * screenWidth)
        self.iconHeight = int(0.2 * screenHeight)
        self.iconSize = (self.iconWidth, self.iconHeight)

        if (self.iconWidth > iconMaxWidth):
            self.iconWidth = iconMaxWidth
        if (self.iconHeight > iconMaxHeight):
            self.iconHeight = iconMaxHeight

        # Scale icons
        self.menuButt = pygame.transform.smoothscale(self.menuButt,
                                                     self.iconSize)
        # Scale pressed icons
        self.menuPressed = pygame.transform.smoothscale(self.menuPressed,
                                                            self.iconSize)

    def draw(self, screen, screenWidth, screenHeight):
        pygame.mouse.set_visible(1)
        Screens().draw(screen, screenWidth, screenHeight, self.credsScreen)
        
        # Position buttons
        menuPos = (int(0.50 * screenWidth), int(0.9 * screenHeight))
        
        # Show pressed state when button is clicked
        if not(self.buttonPressed):
            screen.blit(self.menuButt, menuPos)
        else:
            screen.blit(self.menuPressed, menuPos)

    def update(self):
        (mouseClickX, mouseClickY) = pygame.mouse.get_pos()
        
        # Store icon coordinates (top left & bottom right)
        self.menuCoords = [menuPos, (menuPos[0] + self.iconSize, pos[1] +
                                     self.iconSize)]
        
        # Check if player clicks the icons
        if ((mouseClickX < self.menuCoords[1][0]) and
            (mouseClickX > self.menuCoords[0][0])):
                if ((mouseClickY < self.menuCoords[1][1]) and
                    (mouseClickY > self.menuCoords[0][1])):
                    self.buttonPressed = True
                    return
        self.buttonPressed = False

    def clicked(self):
        return self.buttonPressed

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

# # Rotate an image around its center
# # I did NOT write this function!
# # Credits: http://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
# def rot_center(image, angle):
#     orig_rect = image.get_rect()
#     rot_image = pygame.transform.rotate(image, angle)
#     rot_rect = orig_rect.copy()
#     rot_rect.center = rot_image.get_rect().center
#     rot_image = rot_image.subsurface(rot_rect).copy()
#     return rot_image

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

def enteredNewLevel(data):
    fontHeight = 150
    levelFont = pygame.font.Font("Font/Level_Score.ttf", fontHeight)
    label = levelFont.render("New Level!", 1, data.whiteText) 
    #data.textRenderList.add(label)
    if (changeLevel(data)):
        data.screen.blit(label, (data.width/2, data.height/2))
        # if (data.score == data.score + 5):
        #     data.textRenderList.remove(label)
        print "new level draw!"

###############
## POWER UPS ##
###############

# freeze screen for 5s (3rd most common)
# +5 points (most common)
# bomb (bad) (least common)
# increase ball speed for 5s (2nd most common)

# also have to determine how often a powerup is placed on the screen
    # if random.randint(1, 4) == 1 then decide on powerup

class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("powerup.png", -1)
        self.area = self.image.get_rect()
        self.width = self.area.width
        self.height = self.area.height
        self.randNum = random.randint(1, 10)
        # randomly generate a loc to place powerup; has to be on a step
        # 1, 2, 3 --> +5 points
        # 4, 5, 6 --> increase ball speed
        # 7, 8 --> freeze
        # 9, 10 --> kill enemy (only appear if there's an enemy on screen??)
    def genLocation(self, data):
        # randomly generate a location to place the powerup
        self.randx = random.randint(0, data.width)
        self.randy = random.randint(0, data.height)
        pass
    def update(self, data, position):
        # draw powerup to screen
        # make sure it's sitting on a step
        data.screen.blit(self.image, position)
        for step in data.stepsList:
            if (pygame.sprite.spritecollide(self, step) == True):
                self.rect = self.rect.move(0, -data.speedy)

        if ((self.rect.y + self.height) == 0):
            data.spritesList.remove(self)
            # as long as it doesn't overlap with step we are good
            # if touching a step move with step
            pass
    def remove(self):
        # if ball collides with powerup, remove from screen
        pass

class addPoints(Powerup):
    def whenToSpawn(self):
        if (self.randNum == 1) or (self.randNum == 2) or (self.randNum == 3):
            # self.draw(somewhere), screen.blit?
            pass
    def plusFive(self, data):
        # +5 appears on screen then disappears
        data.score += 5

class freezeScreen(Powerup):
    # def __init__(self):
    #     self.timeToWait = 5000
    #     self.
    def whenToSpawn(self):
        if (self.randNum == 7) or (self.randNum == 8):      
            pass
    def freezeScreen(self):
        # Freezes the steps for 5 seconds
        pass

class incBallSpeed(Powerup):
    def whenToSpawn(self):
        if (self.randNum == 4) or (self.randNum == 5) or (self.randNum == 6):
            # screen.blit(somewhere)
            pass
    def increase(self):
        # Increases the speed of the ball for 5 seconds
        data.ball.speedx += 5
        # for 5 seconds (5000ms)

def drawPause(data):
    fontHeight = 105
    pauseFont = pygame.font.Font("Font/theme_font.TTF", fontHeight)
    label = pauseFont.render("Paused!", 1, data.whiteText) 
    #data.textRenderList.add(label)
    data.screen.blit(label, (data.width/6, data.height/3))
    

def mousePressed(event, data):
    print "Mouse Pressed"
    if (data.activateMenu):
        pass
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
    elif (event.key == pygame.K_r):
        data.themeSound.stop()
        init(data)

def drawGameOver(data):
    fontHeight = 69
    scoreFont = pygame.font.Font("Font/theme_font.TTF", fontHeight)
    label = scoreFont.render("Game Over!", 1, data.whiteText) 
    data.screen.blit(label, (data.width*.1, data.height*.2))

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
                pygame.quit()
                data.mode = "Done"

# if (data.mode == "Done"):
#     if (event.key == pygame.K_r):
#         data.themeSound.stop()
#             init(data)
                

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
    #data.textRenderList.add(label)
    data.screen.blit(label, (data.width*.8, 0))
  
def timerFired(data):
    redrawAll(data)
    data.clock.tick(data.FPS)
    data.mousePos = pygame.mouse.get_pos()
    data.ball.ballStepsColl(data)
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
    drawScore(data)
    drawLevel(data)
    enteredNewLevel(data)
    changeColor(data)
    # if (data.activateMenu) and (not data.gameActive):
    #     data.menuScreen.draw(data.screen, data.width, data.height)
    #     data.menuScreen.updateAll(data.width, data.height)
    pygame.display.update()
    pygame.display.flip()

def initSounds(data):
    data.themeSound = pygame.mixer.Sound("Sounds/fallDown.wav")
    data.bounceSound = pygame.mixer.Sound("Sounds/fx/ballbounce.wav")
    data.chachingSound = pygame.mixer.Sound("Sounds/fx/chaching.wav")
    data.freezeSound = pygame.mixer.Sound("Sounds/fx/freeze.wav")
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

def initPowerups(data):
    data.powerupsList = pygame.sprite.Group()

def initTimes(data):
    data.timeElapsed = 0
    data.timeElapsedScore = 0
    data.timeForLevelChange = 18250
    data.timeToChangeScore = 200

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
    data.paused = False
    data.activateMenu = True
    data.gameActive = False
    data.menuScreen = MenuScreen(data.width, data.height)
    initTimes(data)
    initSteps(data)
    initBall(data)
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
        data.gameActive = True
        if not data.paused:
            timerFired(data)
        for event in pygame.event.get():
            #data.menuScreen.updateAll()
            if (event.type == pygame.QUIT):
                pygame.quit()
                data.gameActive = False
                data.mode = "Done"
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                mousePressed(event, data)
            elif (event.type == pygame.KEYDOWN):
                keyPressed(event, data)


run()
