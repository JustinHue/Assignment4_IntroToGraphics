'''
Created on Jul 9, 2013

@author: Justin Hellsten
'''

import pygame
import parallax

from __init__ import IMG_DIRECTORY, SOUND_DIRECTORY

class StageOne:
    def __init__(self, screen):
        self.parallax = parallax.Parallax(screen, pygame.image.load( IMG_DIRECTORY + "stage1.jpg" ))
        self.stageSprites = pygame.sprite.Group(self.parallax)
        
        if not pygame.mixer:
            print("Cannot Load Sounds")
        else:
            pygame.mixer.init()
            theme = pygame.mixer.Sound(SOUND_DIRECTORY + "stage1_theme.ogg")
            theme.play(-1)
            
        
    def update(self):
        self.stageSprites.update()
        
        
    def draw(self, screen):
        self.stageSprites.draw(screen)
        
    
class StageTwo:
    def __init__(self, screen):
        self.parallax = parallax.Parallax(screen, pygame.image.load( IMG_DIRECTORY + "stage2.jpg" ))
        self.stageSprites = pygame.sprite.Group(self.parallax)
        
        if not pygame.mixer:
            print("Cannot Load Sounds")
        else:
            pygame.mixer.init()
            self.theme = pygame.mixer.Sound(SOUND_DIRECTORY + "stage2_theme.ogg")
            self.theme.play(-1)
        
    def update(self):
        self.stageSprites.update()
        
    def draw(self, screen):
        self.stageSprites.draw(screen)
        
        
class StageThree:
    def __init__(self, screen):
        self.parallax = parallax.Parallax(screen, pygame.image.load( IMG_DIRECTORY + "stage3.jpg" ))
        self.stageSprites = pygame.sprite.Group(self.parallax)
        
        if not pygame.mixer:
            print("Cannot Load Sounds")
        else:
            pygame.mixer.init()
            self.theme = pygame.mixer.Sound(SOUND_DIRECTORY + "stage3_theme.ogg")
            self.theme.play(-1)
        
    def update(self):
        self.stageSprites.update()
        
    def draw(self, screen):
        self.stageSprites.draw(screen)
        