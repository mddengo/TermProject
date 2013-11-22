# Michelle Deng


# Import modules:
import os, sys, math, random
import pygame
from pygame.locals import *

# Create the ball
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        # Call Sprite initializer
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("crystal_sphere.png", -1)
        self.speedx = 6
        self.speedy = 0
        self.area = self.image.get_rect()
        self.width = self.area.width
        self.height = self.area.height
    
    # Moving the ball
    def moveLeft(self):
        self.rect = self.rect.move(-self.speedx, self.speedy)

    def moveRight(self):
        self.rect = self.rect.move(self.speedx, self.speedy)

    # Add gravity so ball falls down to the next step
    def gravity(self):
        # if the ball isn't touching any of the steps,
        # increase the "speed" of the ball in the +y direction (down)
        # to simulate the effects of gravity
        # at the same time, keep the positive or negative speed in the
        # x direction (left/right) the same so the ball doesn't just fall;
        # the ball should also keep moving in the x-direction 
        pass

    # Test for collisions with edge of screen
    # ??? Not sure where to put this
def windowCollision(data):
    if (data.ball.rect.left < 0):
        data.ball.rect.left = 0
    if (data.ball.rect.right > data.width):
        data.ball.rect.right = data.width
    #if (data.ball.rect.top < 0):
    #    data.isGameOver = True    

# Uploads an image file
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

def mousePressed(event, data):
    print "Mouse Pressed"
    redrawAll(data)

def keyPressed(event, data):
    if (event.key == pygame.K_LEFT):
        windowCollision(data)
        data.ball.moveLeft()
        #data.ball.update()
    elif (event.key == pygame.K_RIGHT):
        data.ball.moveRight()
        #data.ball.update()
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


def createSteps(data):
    class Steps(pygame.sprite.Sprite):
        def __init__(self, width, height, color):
            pygame.sprite.Sprite.__init__(self)
            
            # The width of each step needs to be random
            self.height = height
            self.image = pygame.Surface([width, self.height])
            self.rect = self.image.get_rect()
            self.image.fill(color)
    
    # 40 represents ball size
    stepWidth = random.randint(30, data.width - 30)
    data.stepHeight = 20   
    (data.speedx, data.speedy) = (0, 1)
    data.spaceY = int(40 * 1.25)
    data.spaceX = int(40 * 1.25)
    red = data.redColor
    
    # Draw randomly sized steps
    # There should be spaces in between steps (vertically and horizontally)
    for i in xrange(100):
        data.randStep = Steps(stepWidth, data.stepHeight, red)
        data.randStep.rect.x = 0 
        data.randStep.rect.y = data.height #- data.spaceY
        data.stepsList.add(data.randStep)
   
def updateSteps(data):
    for step in data.stepsList:
        if (data.randStep.rect.y + data.speedy >= data.randStep.rect.y):
            data.randStep.rect.y -= data.spaceY
            data.randStep.rect.x += data.speedx
            data.randStep.rect.y += -data.speedy
    

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
    #createSteps(data)
    updateSteps(data)
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
    
    pygame.display.update()
    pygame.display.flip()

def init(data):
    data.mode = "Running"
    # Frames per second
    data.FPS = 10
    # Hides or shows the cursor by taking in a bool
    pygame.mouse.set_visible(0)

    data.keyHeld = False
    
    data.redColor = (255, 0, 60)
    data.ball = Ball()
    data.ballSprite = pygame.sprite.RenderPlain(data.ball)

    # Creating a sprites group for all the steps
    #data.steps = Steps()
    data.stepsList = pygame.sprite.Group()

    data.screen = pygame.display.get_surface()
    data.background = pygame.Surface(data.screen.get_size())
    data.background = data.background.convert()
    data.background.fill((0, 0, 0))
    
    createSteps(data)
    windowCollision(data)

def run():
    pygame.init()
    # Not given the Canvas class
    class Struct: pass
    data = Struct()
    # Initialize screen
    data.width = 350
    data.height = 550
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
