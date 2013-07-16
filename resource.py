"""
 Author Name: Justin Hellsten
 Last Modified by: Justin Hellsten
 Last Modified Date: July 11 2013
"""

import pygame

IMG_DIRECTORY = 'gfx/'
SOUND_DIRECTORY = 'sfx/'
CONFIG_DIRECTORY = 'side_scroller.cfg'
    
STAGE_BACKGROUNDS = [ [IMG_DIRECTORY + 'stage1/city.png', IMG_DIRECTORY + 'stage1/sky.png'], IMG_DIRECTORY + 'stage2.jpg', IMG_DIRECTORY + 'stage3.jpg']
STAGE_THEMES = ['stage1_theme.ogg', 'stage2_theme.ogg', 'stage3_theme.ogg']
CLOUD_IMAGES = ['cloud1.png', 'cloud2.png', 'cloud3.png']

class GfxResource():
    
    explosion = []
    re = None
    collectableMissile = None
    clouds = []

class SfxResource():

    reHit = None
    reDeath = None
                    
#Initialize this module
def init():
    #Initialize Graphics Resource Class
    
    #Load Explosion Animation
    for i in range(25):
        GfxResource.explosion.append(pygame.image.load(IMG_DIRECTORY + 'explosion/ex{0}.png'.format(i+1)))              
            
    #Load Single Images
    GfxResource.re = pygame.image.load(IMG_DIRECTORY + 'random_enemy.png')
    
    GfxResource.clouds.append(pygame.image.load(IMG_DIRECTORY + 'cloud1.png'))
    GfxResource.clouds.append(pygame.image.load(IMG_DIRECTORY + 'cloud2.png'))
    GfxResource.clouds.append(pygame.image.load(IMG_DIRECTORY + 'cloud3.png'))
    
    GfxResource.collectableMissile = pygame.image.load(IMG_DIRECTORY + 'collectable_missile.png')
    #Initialize Sound Resource Class
    if not pygame.mixer:
        print("Cannot Load Sounds")
    else:    
        SfxResource.reHit = pygame.mixer.Sound( SOUND_DIRECTORY + "reHit.ogg")
        SfxResource.reDeath = pygame.mixer.Sound( SOUND_DIRECTORY + "reDeath.ogg")
        
        
            