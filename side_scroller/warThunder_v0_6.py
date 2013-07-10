"""
 Author Name: Justin Hellsten
 Last Modified by: Justin Hellsten
 Last Modified Date: July 9 2013
 
 Program Description: A side scroller game for assignment 4 Intro to Graphics.
 
 Revision History:
 
     -> Change set up so each module represents a version history
     -> Moved some of the code in main def 'outside'
     -> Change game loop to execute in order: Start Screen, GamePlay Screen, Game-End Screen
     -> Split screens into functions (Start Screen, Game Play Screen, Game-End Screen)
     -> Change name to 'War Thunder'
     -> Implemented to continue 
     -> Fixed up Parallax class
     
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
            
         
         
def startScreen():
    running = True
    
    #Clear Screen
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    #Declare sprites
    backgroundSprite = Parallax(screen, pygame.image.load( IMG_DIRECTORY + "stage%d.jpg" % (random.randint(0, 2)) ))
                     
    #Define groups
    backgroundSprites = pygame.sprite.Group(backgroundSprite)
    
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
        backgroundSprites.draw(screen)
        
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