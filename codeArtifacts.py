# Michelle Deng
# Code Artifacts

# Import modules:
import os, sys, math
import pygame
from pygame.locals import *

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        # Call Sprite initializer
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("crystal_sphere.png",-1)
    

def load_image(name, colorkey = None):
    fullname = os.path.join('', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Cannot load image:", name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        # If there weren't an image file, changes the color to the one at the
        # top left corner
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        # RLEACCEL is for older computers; tunes the graphics
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def mousePressed(event, data):
    print "Mouse Pressed"
    redrawAll(data)

def keyPressed(event, data):
    pass

def timerFired(data):
    redrawAll(data)
    data.clock.tick(data.FPS)
    data.mousePos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            data.mode = "Done"
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            mousePressed(event, data)
        elif (event.type == pygame.KEYDOWN):
            keyPressed(event, data)

def redrawAll(data):
    data.allsprites.update()
    data.screen.blit(data.background, (0, 0))
    data.allsprites.draw(data.screen)
    pygame.display.flip()

def init(data):
    data.mode = "Running"
    # Frames per second
    data.FPS = 30
    # Hides or shows the cursor by taking in a bool
    pygame.mouse.set_visible(0)

    data.ball = Ball()
    data.allsprites = pygame.sprite.RenderPlain(data.ball)
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
    data.screenSize = (350, 650)
    data.screen = pygame.display.set_mode(data.screenSize)
    pygame.display.set_caption("Code Artifacts")

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
                keyPressed(event, data)

run()
