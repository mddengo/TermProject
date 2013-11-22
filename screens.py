
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
    
    
class menuScreen(Screens):
    def __init__(self, screenWidth, screenHeight):
        titleMaxWidth = 350
        titleMaxHeight = 225
        iconMaxWidth = 275
        iconMaxHeight = 150
        
        self.buttonPressed = False
        
        self.menuTitle = load_image("falldownTxt.png", -1)
        self.menuPlay = load_image("menuplayTxt.png", -1)
        self.menuPlayPressed = load_image("menuplay_pressed.png", -1)
        self.menuTut = load_image("menututTxt.png", -1)
        self.menuTutPressed = load_image("menutut_pressed.png", -1)
        self.menuCreds = load_image("menucredsTxt.png", -1)
        self.menuCredsPressed = load_image("menucreds_pressed.png", -1)
        self.menuSplash = load_image("menusplash.png")
        
        self.titleWidth = int(0.75 * screenWidth)
        self.titleHeight = int(0.25 * screenHeight)
        self.titleSize = (self.buttonWidth, self.buttonHeight)
        self.iconWidth = int(0.5 * screenWidth)
        self.iconHeight = int(0.2 * screenHeight)
        self.iconSize = (self.iconWidth, self.iconHeight)
        
        if (self.titleWidth > titleMaxWidth):
            self.titleWidth = titleMaxWidth
        if (self.titleHeight > titleMaxHeight):
            self.titleHeight = titleMaxHeight
        if (self.iconWidth > iconMaxWidth):
            self.iconWidth = iconMaxWidth
        if (self.iconHeight > iconMaxHeight):
            self.iconHeight = iconMaxHeight
        
        # Scale icons
        self.menuTitle = pygame.transform.smoothscale(self.menuTitle,
                                                      self.titleSize)
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
        # Draw menu splash screen
        Screens().draw(screen, screenWidth, screenHeight, self.menuSplash)
        # Position buttons
        pos = (int(screenWidth/2 - 0.5*self.iconSize),\
        screenHeight/2- 0.5*self.iconSize)
        # If the mouse is hovering over the icon, show pressed state
        if not(self.iconHover):
            screen.blit(self.startIcon,pos)
        else:
            screen.blit(self.startIcon_pressed,pos)
        # Store Top Left, Bottom Right of button
        self.buttonCoods = [pos, (pos[0] + self.iconSize, pos[1] + \
        self.iconSize)]
        
    def update(self):
        """Updates the menu ie. update if the user is hovering over the icon"""
        mouse_x,mouse_y = pygame.mouse.get_pos()
        # See if the cursor is within the rectuangular bounds of the icon
        if mouse_x < self.buttonCoods[1][0] and mouse_x > \
        self.buttonCoods[0][0]:
                if mouse_y < self.buttonCoods[1][1] and mouse_x > \
                self.buttonCoods[0][1]:
                    # If it is, set the iconHover and break out of this function
                    self.iconHover = True
                    return
        # Only reach here if the player isn't hovering over the icon
        self.iconHover = False
        
    def checkClick(self):
        return self.iconHover
    