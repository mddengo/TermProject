
# Michelle Deng


import pygame

# Uploads an image file
def load_image(name, colorkey = None):
    fullname = os.path.join('', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Cannot load image:", name
        raise SystemExit, message
    image = image.convert_alpha()
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
        image = pygame.transform.smoothscale(image, (screenWidth,screenHeight))
        screen.blit(image, (0,0))
    
# Draws menu splash screen with buttons   
class menuScreen(Screens):
    def __init__(self, screenWidth, screenHeight):
        iconMaxWidth = 275
        iconMaxHeight = 150
        
        self.buttonPressed = False
        
        self.menuPlayPressed = load_image("menuplay_pressed.png", -1)
        self.menuTut = load_image("menututTxt.png", -1)
        self.menuTutPressed = load_image("menutut_pressed.png", -1)
        self.menuCreds = load_image("menucredsTxt.png", -1)
        self.menuCredsPressed = load_image("menucreds_pressed.png", -1)
        self.menuSplash = load_image("menusplashwtitle.png")
        
        self.iconWidth = int(0.5 * screenWidth)
        self.iconHeight = int(0.2 * screenHeight)
        self.iconSize = (self.iconWidth, self.iconHeight)

        if (self.iconWidth > iconMaxWidth):
            self.iconWidth = iconMaxWidth
        if (self.iconHeight > iconMaxHeight):
            self.iconHeight = iconMaxHeight
        
        # Scale icons
        self.menuPlay = pygame.transform.smoothscale(self.menuPlay,
                                                     self.titleSize)
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

    def updateAll(self):
        (mouseClickX, mouseClickY) = pygame.mouse.get_pos()
        
        # Store icon coordinates (top left & bottom right)
        self.playCoords = []
        self.tutCoords = []
        self.credsCoords = []
        
        # Check if player clicks the icons
        if ((mouseClickX < self.playCoords[1][0]) and
            (mouseClickX > self.playCoords[0][0])):
                if ((mouseClickY < self.playCoords[1][1]) and
                    (mouseClickY > self.playCoords[0][1])):
                    self.buttonPressed = True
                    return
        # repeat for other buttons
        self.buttonPressed = False
        
    def clicked(self):
        return self.buttonPressed
    
class Paused(Screens):
    #code
    pass

class GameOver(Screens):
    #code
    pass

class Creds(Screens):
    #code
    pass



    