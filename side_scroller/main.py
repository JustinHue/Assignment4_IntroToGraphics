'''
Created on Jun 14, 2013

@author: Justin Hellsten
'''

# Import and Initialize
import pygame
import utility
import sys

from __init__ import *

pygame.init()
utility.init()

        
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


    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))


    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                

        pygame.display.flip()
    
if __name__ == "__main__" : main()

