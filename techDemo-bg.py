# Michelle Deng
# Technology Demonstration

# Import modules:
import os, sys, math
import pygame
from pygame.locals import *

class Koala(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('koala.png', -1)

    def update(self):
        "move the koala based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos

def load_image(name, colorkey = None):
    fullname = os.path.join('', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
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

def rotKoala(data):
    # Rotating the koala
    rotated = pygame.transform.rotate(data.koala, math.pi / 2)
    return rotated

def redrawAll(data):
    data.allsprites.update()
    data.screen.blit(data.background, (0, 0))
    data.allsprites.draw(data.screen)
    pygame.display.flip()

def init(data):
    data.mode = "Running"
    data.FPS = 30
    pygame.mouse.set_visible(0)

    data.koala = Koala()
    data.allsprites = pygame.sprite.RenderPlain(data.koala)
    data.screen = pygame.display.get_surface()
    
    data.background = pygame.Surface(data.screen.get_size())
    data.background = data.background.convert()
    data.background.fill((250, 250, 250))

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
