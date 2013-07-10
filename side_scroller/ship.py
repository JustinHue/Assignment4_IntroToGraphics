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
        self.image = pygame.surface.Surface((64, 50), pygame.SRCALPHA)

        self.spritesheet = pygame.image.load( IMG_DIRECTORY + "MiG-X3.png" )
        self.image.blit(self.spritesheet, (0,0))
        
        Ship.__init__(self, screen)
        
        
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

        
        


