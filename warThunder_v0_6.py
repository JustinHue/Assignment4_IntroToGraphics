"""
 Author Name: Justin Hellsten
 Last Modified by: Justin Hellsten
 Last Modified Date: July 10 2013
 
 Program Description: A side scroller game for assignment 4 Intro to Graphics.
 
 Revision History: 0.0.7
 
    -> Fixed up ship classes
    -> Implemented MyFont class for quick font rendering
    
"""



""" Import and Initialize """
import pygame, utility, sys, random, os

#Ensures pathing is correct
os.chdir(os.path.dirname(os.path.realpath(__file__)))

pygame.init()
utility.init()

""" Game Constants """
CONFIG_DIRECTORY = '../side_scroller.cfg'
IMG_DIRECTORY = '../gfx/'
SOUND_DIRECTORY = '../sfx/'

STAGE_BACKGROUNDS = ['stage1.jpg', 'stage2.jpg', 'stage3.jpg']

""" Read configuration file """
utility.set_config_file(CONFIG_DIRECTORY)
    
width = int(utility.get_config_value('width', 800))
height = int(utility.get_config_value('height', 600))
title = utility.get_config_value('title', 'War Thunder by Justin Hellsten')
depth = int(utility.get_config_value('depth', 32))
mode = int(utility.get_config_value('mode', 0))

if not pygame.display.get_init():
    print 'Could not initialize display screen'
    sys.exit()

#Check if depth is okay for display mode
depth = pygame.display.mode_ok((width, height), mode, depth)  
    
# Create our screen window
screen = pygame.display.set_mode((width, height), mode, depth)    
pygame.display.set_caption(title)
    
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()


""" Classes """
class Parallax(pygame.sprite.Sprite):    
    def __init__(self, screen, sprite):         
        pygame.sprite.Sprite.__init__(self)        
        self.screen = screen
        self.sprite = sprite
        self.image = pygame.surface.Surface((self.sprite.get_width()*3, self.sprite.get_height()))
        self.rect = self.image.get_rect()
        self.dx = -5
        
        self.image.blit(self.sprite, (0, 0))
        self.image.blit(pygame.transform.flip(self.sprite, True, False), (self.sprite.get_width(), 0))
        self.image.blit(self.sprite, (self.sprite.get_width()*2, 0))

    def update (self):
        self.rect.right += self.dx
        if self.rect.right <= self.screen.get_width():
            self.rect.left = self.screen.get_width() - self.sprite.get_width()
            
class MyFont(pygame.sprite.Sprite):
    def __init__(self, text, centerx, centery):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("None", 50)
        self.image = self.font.render(text, 1, (0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)
        
        
class Ship(pygame.sprite.Sprite):
    def __init__(self, screen, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = spritesheet
        self.screen = screen   
        
    def update (self):                
        mousex, mousey = pygame.mouse.get_pos()
        
        # Collision check on screen boundaries
        if mousey - self.rect.height / 2 < 0:
            self.rect.centery = self.rect.height / 2
        elif mousex + self.rect.height / 2 > self.screen.get_height():
            self.rect.centery = self.screen.get_height() - self.rect.height / 2
        else:
            self.rect.centery = mousey

        self.lastmousey = self.curmousey
        self.curmousey = mousey
        
  
      
class MiGX3(Ship):
    def __init__(self, screen, centerx, centery):
        Ship.__init__(self, screen, pygame.image.load( IMG_DIRECTORY + "MiG-X3.png" ))
        self.image = pygame.surface.Surface((64, 50), pygame.SRCALPHA)

        self.image.blit(self.spritesheet, (0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)
        
        # Set mouse track fields
        self.lastmousey = 0
        self.curmousey = 0
        
    def update(self):
        Ship.update(self)
        
        dmy = self.curmousey - self.lastmousey 
        
        if dmy != 0:
            self.flyVertically() 
        else:
            self.flyStraight()
      
                
    def flyVertically(self):  
        tmp_image = pygame.surface.Surface((64, 50), pygame.SRCALPHA)
        tmp_image.blit(self.spritesheet, (0,0), pygame.rect.Rect((64,0), (64,50)))
        self.image = tmp_image
        
    def flyStraight(self):
        tmp_image = pygame.surface.Surface((64, 50), pygame.SRCALPHA)
        tmp_image.blit(self.spritesheet, (0,0))
        self.image = tmp_image
        
         
    
def startScreen():
    running = True
    
    #Clear Screen
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    #Declare sprites
    backgroundSprite = Parallax(screen, pygame.image.load( IMG_DIRECTORY + "stage%d.jpg" % (random.randint(1, 3)) ))
    shipSprite = MiGX3(screen, screen.get_width()/2, 0)
        
    fontSprite = MyFont('War Thunder', screen.get_width()/2, 100)
    
    #Define groups
    backgroundSprites = pygame.sprite.Group(backgroundSprite)
    playerSprites = pygame.sprite.Group(shipSprite)
    fontSprites = pygame.sprite.Group(fontSprite)
    
    # Play intro theme
    if not pygame.mixer:
        print("Cannot Load Sounds")
    else:
        pygame.mixer.init()
        sndIntroTheme = pygame.mixer.Sound(SOUND_DIRECTORY + "intro_theme.ogg")
        sndIntroTheme.play(-1)
            
    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                toContinue = False
            elif event.type == pygame.KEYDOWN:
                toContinue = True
                running = False
        
        backgroundSprites.update()
        playerSprites.update()
        fontSprites.update()
        
        backgroundSprites.draw(screen)
        playerSprites.draw(screen)
        fontSprites.draw(screen)
        
        pygame.display.flip()
        
    return toContinue

        
def gamePlayScreen():
    running = True

    #Clear Screen
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
 
    while running:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                toContinue = False
              
        pygame.display.flip()
          
    return toContinue
          
def gameEndScreen():
    running = True
    
    while running:
        clock.tick(30)
    
def main():
    keepPlaying = True
    
    while keepPlaying:
        toContinue = startScreen()
        if toContinue:
            toContinue = gamePlayScreen()
            if toContinue:
                gameEndScreen()
            else:
                keepPlaying = False
        else:
            keepPlaying = False

    
    
if __name__ == '__main__': 
    main()