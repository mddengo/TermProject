# Michelle Deng


# Import modules:
import os, sys, math
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
        self.state = "still"
        
##    # Updates the position of the ball
##    def update(self):
##        newPos = self.rect.move(self.movex, self.movey)
##        if self.area.contains(newPos):
##            self.rect = newPos
##        # Pumps events into event queue
##        pygame.event.pump()
    
    # Moving the ball
    def moveLeft(self):
        self.rect = self.rect.move(-self.speedx, self.speedy)
        self.state = "moveLeft"
    def moveRight(self):
        self.rect = self.rect.move(self.speedx, self.speedy)
        self.state = "moveRight"

        
    # Add gravity so ball falls down to the next step
    def gravity(self):
        # if the ball isn't touching any of the steps,
        # increase the "speed" of the ball in the +y direction (down)
        # to simulate the effects of gravity
        # at the same time, keep the positive or negative speed in the
        # x direction (left/right) the same so the ball doesn't just fall;
        # the ball should also keep moving in the x-direction 
        pass

    # updates ball's position and checks for collision
    # ???????!!!!
##    def update(self):
##        if (self.rect.left < 0) or (self.rect.right > self.width):
##            #self.speedx = -self.speedx
####        if (self.rect.top < 0):
####            #game over!
####            pass
##            self.rect.left = reset(self.rect.left, 0, self.width)
##            self.rect.right = reset(self.rect.right, 0, self.width)        
####        self.rect.top = reset(self.rect.top, 0, self.height)
####        self.rect.bottom = reset(self.rect.bottom, 0, self.height)
        
    # Test for collisions with edge of screen
    # ??? Not sure where to put this
def windowCollision(data):
    if (data.ball.rect.left < 0):
        data.ball.rect.left = data.screen.left
    if (data.ball.rect.right > data.width):
        data.ball.rect.right = data.screen.right
    if (data.ball.rect.top < 0):
        data.isGameOver = True
        
def reset(val, low, high):
    return min(max(val, low), high)        

### Create the steps
##class Steps(object):
##    
##    def __init__(self):
##        pygame.sprite.Sprite.__init__(self) # ??? error here
##        self.image, self.rect = load_image("presteps.png", -1)
##        self.rect.left = data.screen.left
##        self.rect.right = data.screen.right
##        # The speed should increase with each level
##        self.speed = 10
##        self.movex = 0
##        self.movey = 0
##        self.area = self.image.get_rect()
##        self.state = "still"
##        
##     # Updates the position of the steps
##    def update(self):
##        newPos = self.rect.move(self.movex, self.movey)
##        if self.area.contains(newPos):
##            self.rect = newPos
##        # Pumps events into event queue
##        pygame.event.pump()
##        
##    # Move all the steps (the sprite group) in the -y direction (up)
##    def moveSteps(self)
##        self.movey -= self.speed
##        return self.rect.move(self.movex, self.movey)
##        # should be different than the format of the function for moving the Ball
##        # because the way the Steps move is based on time and not user control
##        self.state = "moveUp"        


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

# Check for win
def win(data):
    data.mode = "Done"
    # takes player to Game Over screen
    # the game over screen will display the score and an option whether to
    # return to the menu or play again
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                data.mode = "Done"
    pass

def mousePressed(event, data):
    print "Mouse Pressed"
    redrawAll(data)

def keyPressed(event, data):
    if (event.key == pygame.K_LEFT):
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
    if (data.mode != "Done"):
        redrawAll(data)

def keyUnpressed(event, data):
    # If the keys are not being pressed, the ball stops moving
    if (event.key == K_LEFT) or (event.key == K_DOWN):
        data.ball.speedx = 0
        data.ball.speedy = 0
        data.ball.state = "still"
        
def timerFired(data):
    if (data.mode != "Done"):
        redrawAll(data)
        data.clock.tick(data.FPS)
        data.mousePos = pygame.mouse.get_pos()
        # things to do with timing, such as updating things, dealing with collisions(??)
        # updating stuff, checking for win?
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


def redrawAll(data):
    data.ballSprite.update()
    #data.stepsSprite.update()
    data.screen.blit(data.background, (0, 0))
    data.ballSprite.draw(data.screen)
    #data.stepsSprite.draw(data.screen)
    pygame.display.update()
    pygame.display.flip()

def init(data):
    data.mode = "Running"
    # Frames per second
    data.FPS = 30
    # Hides or shows the cursor by taking in a bool
    pygame.mouse.set_visible(0)

    data.ball = Ball()
    data.ballSprite = pygame.sprite.RenderPlain(data.ball)


##    # Creating a sprites group for all the steps
##    data.stepsGroup = pygame.sprite.Group()
##    data.steps = Steps()
##    # ???
##    # Not sure where to put this -- in the class Steps?
##    data.stepsGroup.add(data.steps) 
##    
##    data.stepsSprite = pygame.sprite.RenderPlain(data.steps)

    data.screen = pygame.display.get_surface()

    data.background = pygame.Surface(data.screen.get_size())
    data.background = data.background.convert()
    data.background.fill((0, 0, 0))

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
    pygame.display.set_caption("Code Artifacts")

    # Initialize clock
    data.clock = pygame.time.Clock()
    init(data)
    timerFired(data)
    while True:
        timerFired(data)
    
run()
