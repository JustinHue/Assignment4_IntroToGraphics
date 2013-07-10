'''
Created on Jul 9, 2013

@author: Justin Hellsten
'''

import pygame
import parallax
from __init__ import IMG_DIRECTORY, SOUND_DIRECTORY

class StartScreen(pygame.sprite.Sprite):
    
    # Menu States
    MENU_NONE = -1
    MENU_PLAY = 0
    MENU_INSTRUCTION = 1
    MENU_EXIT = 2
    
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)  
        self.spriteGroup = pygame.sprite.Group(parallax.Parallax(screen, pygame.image.load( IMG_DIRECTORY + "stage1.jpg" )))
        
        #self.font = pygame.font.SysFont("None", 50)
        self.menuState = StartScreen.MENU_NONE
        
        #self.text = "Play\nInstruction"
        #self.image = self.font.render(self.text, 1, (0, 255, 0))
        
        if not pygame.mixer:
            print("Cannot Load Sounds")
        else:
            pygame.mixer.init()
            sndIntroTheme = pygame.mixer.Sound(SOUND_DIRECTORY + "intro_theme.ogg")
            sndIntroTheme.play(-1)
        
    def update(self):
        self.spriteGroup.update()
        mousex, mousey = pygame.mouse.get_pos()
        
    def draw(self, screen):
        self.spriteGroup.draw(screen)