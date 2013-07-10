"""
 Author Name: Justin Hellsten
 Last Modified by: Justin Hellsten
 Last Modified Date: July 10 2013
 
 Program Description: A side scroller game for assignment 4 Intro to Graphics.
 
 Revision History: 0.0.7
 
    -> Fixed up ship classes
    -> Implemented MyFont class for quick font rendering
    -> Removed sos import and moved files outside of package
    -> Added instructions to start screen
    -> Made it so it shows bullets and special shots on mouse down events during start screen (instruction) phase
    -> Added bullet and special shot classes
    -> Added primary and secondary weapon sfx and gfx
    -> Added a class called Projectile above missile and bullet
    -> Set up stage one (no enemies currently)
    
"""

""" Import and Initialize """
import pygame, utility, sys, random

pygame.init()
utility.init()

""" Game Constants """
CONFIG_DIRECTORY = 'side_scroller.cfg'
IMG_DIRECTORY = 'gfx/'
SOUND_DIRECTORY = 'sfx/'

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
      
class Projectile(pygame.sprite.Sprite):
    def __init__(self, screen, image, startx, starty):   
        pygame.sprite.Sprite.__init__(self)  
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (startx, starty)

    def update(self):
        if self.rect.left >= screen.get_width():
            self.kill()
                    
class Bullet(Projectile):
    def __init__(self, screen, startx, starty):   
        Projectile.__init__(self, screen, pygame.image.load( IMG_DIRECTORY + 'bullet2.png'), startx, starty)
        self.dx = 20
        
    def update(self):
        Projectile.update(self)
        self.rect.left += self.dx
        
class SpecialShot(Projectile):
    def __init__(self, screen, startx, starty):
        Projectile.__init__(self, screen, pygame.image.load( IMG_DIRECTORY + 'missile.png'), startx, starty)
        self.speed = 0.0
        self.dx = 1
        
    def update(self):
        Projectile.update(self)
        self.speed += self.dx
        self.rect.right += self.speed

            
class MyFont(pygame.sprite.Sprite):
    def __init__(self, text, centerx, centery, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("None", size)
        self.image = self.font.render(text, 1, color)
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)
        
        
class Ship(pygame.sprite.Sprite):
    def __init__(self, screen, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = spritesheet
        self.screen = screen   
        
        # Set mouse track fields
        self.lastmousey = 0
        self.curmousey = 0

    def update (self):                
        mousex, mousey = pygame.mouse.get_pos()
        
        # Collision check on screen boundaries
        if mousey - self.rect.height / 2 < 0:
            self.rect.centery = self.rect.height / 2
        elif mousex + self.rect.height / 2 > self.screen.get_height():
            self.rect.centery = self.screen.get_height() - self.rect.height / 2
        else:
            self.rect.centery = mousey

        #Set last and current mouse positions
        self.lastmousey = self.curmousey
        self.curmousey = mousey
                      

            
class MiGX3(Ship):
    def __init__(self, screen, centerx, centery):
        Ship.__init__(self, screen, pygame.image.load( IMG_DIRECTORY + "MiG-X3.png" ))
        self.image = pygame.surface.Surface((64, 50), pygame.SRCALPHA)

        self.image.blit(self.spritesheet, (0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)
        
        if not pygame.mixer:
            print("Cannot Load Sounds")
        else:
            pygame.mixer.init()
            #Make sound a list so we can have multiple weapon bullet shots
            self.sndPrimaryWeapon = pygame.mixer.Sound( SOUND_DIRECTORY + "bullet.ogg")
            self.sndSecondaryWeapon = pygame.mixer.Sound( SOUND_DIRECTORY + "missile.ogg")


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
        
    mainTitle = MyFont('War Thunder', screen.get_width()/2, 100, 50, (0, 0, 0))
    movementText = MyFont('Move the mouse up/down to move your ship.', screen.get_width()/2*0.45, 200, 22, (225, 225, 225))
    shootBulletText = MyFont('Left mouse click to shoot primary weapon.', screen.get_width()/2*0.45, 250, 22, (225, 225, 225))
    shootSpecialText = MyFont('Right mouse click to shoot secondary weapon (limited)!', screen.get_width()/2*0.55, 300, 22, (225, 225, 225))
    clickAnywhereText = MyFont('Click any key to continue...', screen.get_width()/2, screen.get_height()/2+100, 30, (0, 0, 0))
    
    #Define groups
    backgroundSprites = pygame.sprite.Group(backgroundSprite)
    playerSprites = pygame.sprite.Group(shipSprite)
    fontSprites = pygame.sprite.Group(mainTitle, movementText, shootBulletText, shootSpecialText, clickAnywhereText)
    bulletSprites = pygame.sprite.Group()
    specialShotSprites = pygame.sprite.Group()
    
    # Play intro theme
    if not pygame.mixer:
        print("Cannot Load Sounds")
    else:
        pygame.mixer.init()
        pygame.mixer.music.load(SOUND_DIRECTORY + "intro_theme.ogg")
        pygame.mixer.music.play(-1)
            
    while running:
        clock.tick(30)
        mouseState = pygame.mouse.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                toContinue = False
            if event.type == pygame.KEYDOWN:
                toContinue = True
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseState = pygame.mouse.get_pressed()
                if mouseState[2]: #Shoot secondary weapon
                    shipSprite.sndSecondaryWeapon.stop()
                    shipSprite.sndSecondaryWeapon.play()    
                    specialShotSprites.add(SpecialShot(screen, shipSprite.rect.centerx, shipSprite.rect.centery-3))
        
        # Have this out here so we shoot the primary all the time if the mouse button is pressed
        if mouseState[0]: #Shoot primary weapon
            shipSprite.sndPrimaryWeapon.stop()
            shipSprite.sndPrimaryWeapon.play()
            bulletSprites.add(Bullet(screen, shipSprite.rect.centerx, shipSprite.rect.centery-3))
                            
        backgroundSprites.update()
        playerSprites.update()
        fontSprites.update()
        bulletSprites.update()
        specialShotSprites.update()
        
        backgroundSprites.draw(screen)
        bulletSprites.draw(screen)
        specialShotSprites.draw(screen)
        playerSprites.draw(screen)
        fontSprites.draw(screen)
        
        
        pygame.display.flip()
        
    return toContinue

        
def gamePlayScreen():
    running = True
    currentStage = 3
    
    #Clear Screen
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    #Declare sprites
    backgroundSprite = Parallax(screen, pygame.image.load( IMG_DIRECTORY + "stage%d.jpg" % currentStage ))
    shipSprite = MiGX3(screen, 50, 0)
        
    #Define groups
    backgroundSprites = pygame.sprite.Group(backgroundSprite)
    playerSprites = pygame.sprite.Group(shipSprite)
    bulletSprites = pygame.sprite.Group()
    specialShotSprites = pygame.sprite.Group()
    
    # Play intro theme
    if not pygame.mixer:
        print("Cannot Load Sounds")
    else:
        pygame.mixer.init()
        pygame.mixer.music.load(SOUND_DIRECTORY + "stage3_theme.ogg")
        pygame.mixer.music.play(-1)
            
    while running:
        clock.tick(30)
        mouseState = pygame.mouse.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                toContinue = False
            if event.type == pygame.KEYDOWN:
                toContinue = True
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseState = pygame.mouse.get_pressed()
                if mouseState[2]: #Shoot secondary weapon
                    shipSprite.sndSecondaryWeapon.stop()
                    shipSprite.sndSecondaryWeapon.play()    
                    specialShotSprites.add(SpecialShot(screen, shipSprite.rect.centerx, shipSprite.rect.centery-3))
        
        # Have this out here so we shoot the primary all the time if the mouse button is pressed
        if mouseState[0]: #Shoot primary weapon
            shipSprite.sndPrimaryWeapon.stop()
            shipSprite.sndPrimaryWeapon.play()
            bulletSprites.add(Bullet(screen, shipSprite.rect.centerx, shipSprite.rect.centery-3))
                            
        backgroundSprites.update()
        playerSprites.update()
        bulletSprites.update()
        specialShotSprites.update()
        
        backgroundSprites.draw(screen)
        bulletSprites.draw(screen)
        specialShotSprites.draw(screen)
        playerSprites.draw(screen)
        
        
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