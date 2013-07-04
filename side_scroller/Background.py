'''
Created on Jul 4, 2013

@author: 200197858
'''

import pygame
from __init__ import IMG_DIRECTORY


class Background(pygame.sprite.Sprite):    
    def __init__(self):         
        pygame.sprite.Sprite.__init__(self)        
        self.image = pygame.image.load( IMG_DIRECTORY + "new_cave_bg.jpg" )        
        self.rect = self.image.get_rect()        
        self.dx = -5                    
        
    def update (self):        
        self.rect.right += self.dx        
        if self.rect.right <= 800:            
            self.rect.left = 0