'''
Created on Jun 14, 2013

@author: Justin Hellsten
'''

# Fix directory pathing
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))


# Import and Initialize
import pygame
import utility
import sys

import ship
import parallax
import startScreen
from __init__ import *

pygame.init()
utility.init()

pygame.font.init()

def main():
    utility.set_config_file(CONFIG_DIRECTORY)
    
    width = int(utility.get_config_value('width', DEF_WINDOW_W))
    height = int(utility.get_config_value('height', DEF_WINDOW_H))
    title = utility.get_config_value('title', DEF_TITLE)
    depth = int(utility.get_config_value('depth', DEF_DEPTH))
    mode = int(utility.get_config_value('mode', DEF_MODE))
           
    if not pygame.display.get_init():
        print 'Could not initialize display screen'
        sys.exit()

    depth = pygame.display.mode_ok((width, height), mode, depth)   
    
    # Create our screen window
    screen = pygame.display.set_mode((width, height), mode, depth)    
    pygame.display.set_caption(title)

    startscreen = startScreen.StartScreen(screen)
    
    # Create game objects
    shipSprite = ship.MiGX3(screen)
    stageOne = parallax.Parallax(screen, pygame.image.load( IMG_DIRECTORY + "stage1.jpg" ))
    
    gameSprites = pygame.sprite.OrderedUpdates(stageOne, shipSprite)

    if not pygame.mixer:
         print("Cannot Load Sounds")
    else:
        pygame.mixer.init()

        
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
        if startscreen.menuState == startScreen.StartScreen.MENU_PLAY:
            gameSprites.update()
            gameSprites.draw(screen)
        elif startscreen.menuState == startScreen.StartScreen.MENU_INSTRUCTION:
            gameSprites.update()
            gameSprites.draw(screen)
        elif startscreen.menuState == startScreen.StartScreen.MENU_EXIT:
            gameSprites.update()
            gameSprites.draw(screen) 
        else:
            startscreen.update()
            startscreen.draw(screen)
        
        pygame.display.flip()

        
if __name__ == "__main__" : main()

