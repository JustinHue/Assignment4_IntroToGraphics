'''
Created on Jul 4, 2013

@author: 200197858
'''

import pygame
from __init__ import IMG_DIRECTORY

class Ship(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        
        self.rect = self.image.get_rect()
        self.screen = screen
        
        self.rect.center = (100, screen.get_height()/2)
        
        # Set mouse track fields
        self.lastmousey = 0
        self.curmousey = 0
        
    def update (self):                
        mousex, mousey = pygame.mouse.get_pos()
        
        if mousey - self.rect.height / 2 < 0:
            self.rect.centery = self.rect.height / 2
        elif mousex + self.rect.height / 2 > self.screen.get_height():
            self.rect.centery = self.screen.get_height() - self.rect.height / 2
        else:
            self.rect.centery = mousey

        self.lastmousey = self.curmousey
        self.curmousey = mousey
        

class MiGX3(Ship):
    def __init__(self, screen):
        self.image = pygame.surface.Surface((64, 50))
        Ship.__init__(self, screen)
        
        self.spritesheet = pygame.image.load( IMG_DIRECTORY + "MiG-X3.png" )
        self.image.blit(self.spritesheet, (0,0))
        
    def update(self):
        Ship.update(self)
        
        dmy = self.curmousey - self.lastmousey 
        if dmy > 0:
            self.flyDown() 
        elif dmy < 0:
            self.flyUp()
        else:
            self.flyStraight()
                
        
    def flyDown(self):
        self.image.blit(self.spritesheet, (64,0))
        print 'Flying Down'
        
    def flyUp(self):
        self.image.blit(self.spritesheet, (128,0))
        print 'Flying up'
        
    def flyStraight(self):
        self.image.blit(self.spritesheet, (0,0))
        print 'Flying straight'

        
        


