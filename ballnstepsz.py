# Michelle Deng


# Import modules:
import os, sys, math, random
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
        self.speedx = 10
        self.speedy = 0
        self.area = self.image.get_rect()
        self.width = self.area.width
        self.height = self.area.height
        self.loBound = self.rect.y + self.height
        self.gravity = 19
    
    # Moving the ball
    def moveLeft(self):
        if (self.rect.x != 0):
            self.rect = self.rect.move(-self.speedx, self.speedy)
        else:
            print "no move left"
    def moveRight(self, data):
        data.margin = 3
        if (self.rect.x + self.width + data.margin < data.width):    
            self.rect = self.rect.move(self.speedx, self.speedy)
        else:
            print "no move right"

    # Add gravity so ball falls down to the next step
    def addGravity(self, data):
        self.loBound += self.gravity
        self.rect = self.rect.move(0, self.gravity)
        if (self.loBound >= data.height):
            self.gravity = 0
        # if the ball isn't touching any of the steps add gravity 

#if (data.ball.rect.top < 0):
#    data.isGameOver = True
    def ballStepsColl(self, data):
        # make sure ball still moves along step
        for step in data.stepsList:
            if (pygame.sprite.collide_rect(self, step) == True):
                self.rect.y -= data.speedy
            else:
                data.ball.addGravity(data) #?    

class Steps(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        
        self.height = height
        self.image = pygame.Surface([width, self.height])
        self.rect = self.image.get_rect()
        self.image.fill(color)

def createLeftStep(data):
    # 40 represents ball size
    # The width of each step needs to be random
    stepWidth = random.randint(30, data.width - 40)
    
    data.stepHeight = 20   
    (data.speedx, data.speedy) = (0, 5)
    # Minimum distance between two steps on top of each other
    data.spaceY = int(40 * 1.75)
    red = data.redColor
    # Draw randomly sized steps
    data.leftRandStep = Steps(stepWidth, data.stepHeight, red)
    # Positions steps on left side of screen
    data.leftRandStep.rect.x = 0 
    data.leftRandStep.rect.y = data.height 
    data.stepsList.add(data.leftRandStep)

def createRightStep(data):
    # 40 represents ball size
    # The width of each step needs to be random
    stepWidth = random.randint(30, data.width - 40)

    red = data.redColor
    # Draw randomly sized steps
    data.rightRandStep = Steps(stepWidth, data.stepHeight, red)
    # Sets each step on the right side of the screen
    data.rightRandStep.rect.x = data.width - stepWidth 
    data.rightRandStep.rect.y = data.height 
    data.stepsList.add(data.rightRandStep)

def createMiddleStep(data):
    # 40 represents ball size
    # The width of each step needs to be random
    stepWidth = random.randint(30, data.width - 40)
    # Choose a random point on which to center the middle step
    randCenterX = random.randint(75, data.width - 75) # how to decide?????
    red = data.redColor
    
    # Draw randomly sized steps
    data.midRandStep = Steps(stepWidth, data.stepHeight, red)
    # Centers step on a random point 
    data.midRandStep.rect.centerx = randCenterX
    data.midRandStep.rect.y = data.height 
    data.stepsList.add(data.midRandStep)
   
def updateSteps(data):
    # Minimum distance between two steps next to each other
    data.spaceX = int(40 * 1.75)
    # There should at most be 3 steps in each row
    randStepsInRow = random.randint(1, 3) # where to put this??
    for step in data.stepsList:
        step.rect.y -= data.speedy
        if (step.rect.y + data.stepHeight == 0):
            data.stepsList.remove(step)
        if ((data.leftRandStep.rect.right == data.midRandStep.rect.x) or
        (data.midRandStep.rect.right == data.rightRandStep.rect.x)):
        # add space??
            pass

def trySpawnNewStep(data):
    # add spaces in here?
    
    data.lowest += data.speedy
    data.lowest %= data.spaceY
    if (data.lowest == 0):
        createLeftStep(data)
        createRightStep(data)
        createMiddleStep(data)



def mousePressed(event, data):
    print "Mouse Pressed"
    redrawAll(data)

def keyPressed(event, data):
    if (event.key == pygame.K_LEFT):    
        data.ball.moveLeft()
    elif (event.key == pygame.K_RIGHT):
        data.ball.moveRight(data)
    elif (event.key == pygame.K_p):
        # pause the game
        # takes player to pause screen
        # if player presses 'p' again, resumes the game
        pass

def keyUnpressed(event, data):
    # If the keys are not being pressed, the ball stops moving
    if (event.key == K_LEFT) or (event.key == K_DOWN):
        data.ball.speedx = 0
        data.ball.speedy = 0

# Check for win
def win(data):
    data.mode = "Done"
    # win screen, etc.
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                data.mode = "Done"

  
def timerFired(data):
    redrawAll(data)
    data.clock.tick(data.FPS)
    data.mousePos = pygame.mouse.get_pos()
    data.ball.addGravity(data)
    data.ball.ballStepsColl(data)
    
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
    updateSteps(data)
    trySpawnNewStep(data)
    
    pygame.display.update()
    pygame.display.flip()

def initSteps(data):
    # Creating a sprites group for all the steps
    data.stepsList = pygame.sprite.Group()
    data.lowest = 0
    data.redColor = (255, 0, 60)
    
    createLeftStep(data)
    createRightStep(data)
    createMiddleStep(data)
    updateSteps(data)
    
def initBall(data):
    data.ball = Ball()
    data.ballSprite = pygame.sprite.RenderPlain(data.ball)
    data.ball.moveRight(data)
    data.ball.addGravity(data)

def init(data):
    data.mode = "Running"
    # Frames per second
    data.FPS = 20
    # Hides or shows the cursor by taking in a bool
    pygame.mouse.set_visible(0)

    data.keyHeld = False
    
    initSteps(data)
    initBall(data)
    

    data.screen = pygame.display.get_surface()
    data.background = pygame.Surface(data.screen.get_size())
    data.background = data.background.convert()
    data.background.fill((0, 0, 0))


def run():
    pygame.init()
    class Struct: pass
    data = Struct()
    # Initialize screen
    (data.width, data.height) = (350, 550)
    data.screenSize = (data.width, data.height)
    data.screen = pygame.display.set_mode(data.screenSize)
    pygame.display.set_caption("Window")
    # Initialize clock
    data.clock = pygame.time.Clock()
    init(data)
    timerFired(data)
    while (data.mode != "Done"):
        timerFired(data)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                data.mode = "Done"
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                mousePressed(event, data)
            elif (event.type == pygame.KEYDOWN):
                data.keyHeld = True
                keyPressed(event, data)
            elif (event.type == pygame.KEYUP):
                data.keyHeld = False
                keyUnpressed(event, data)

run()
