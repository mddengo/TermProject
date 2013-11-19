# Michelle Deng
# Technology Demonstration

# Import modules:
import pygame, math
from pygame.locals import *

class Koala(object):
    imageFile = "koala.png"
    position = (300,300)
    surface = None

def mousePressed(event, data):
    print "Mouse Pressed"
    redrawAll(data)

def keyPressed(event, data):
    if (event.key == pygame.K_SPACE):
        data.koala = rot_center(data.koala, 3)
    redrawAll(data)

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

def rotKoala(data):
    # Rotating an image
    rotated = pygame.transform.rotate(data.koala, math.pi / 2)
    return rotated

def rot_center(image, angle):
    """Rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def redrawAll(data):
    # Copies the image to x=50, y=100 on the screen
    data.screen.blit(data.koala)
    pygame.display.flip()

def init(data):
    data.mode = "Running"
    data.FPS = 30
    data.koala = Koala()
    koala.surface = 

def run():
    pygame.init()
    
    #not given the Canvas class
    class Struct: pass
    data = Struct()
    
    #initialize the screen
    data.screenSize = (800,800)
    data.screen = pygame.display.set_mode(data.screenSize)
    pygame.display.set_caption("Window")
    
    #initialize clock
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
                keyPressed(event,data)

run()
