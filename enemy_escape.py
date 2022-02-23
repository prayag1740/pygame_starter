import pygame

#importing constants for easier access to key coordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

pygame.init() #initializing pygame

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))

#game imp 
"""
1) processes user input
2) updates the state of game objects
3) updates the display and audio output
4)maintains the speed of the game
"""

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN: #if user pressed a key
            if event.key == K_ESCAPE: #if it was an escape key
                running = False

        elif event.type == QUIT: #if user closed the window
            running = False

    #white background for screen
    screen.fill((255, 255, 255))

    #creates a surface (rectangular object)and params are length and width
    surf = pygame.Surface((50, 50))

    surf.fill((0,0,0)) #seperate color for surface then screen
    rect = surf.get_rect()

    surf_center = (
        (SCREEN_WIDTH/2),
        (SCREEN_HEIGHT/2)
    )

    screen.blit(surf, surf_center) #places one surface on another; 2nd argument here is the position
    pygame.display.flip() #displays actual

pygame.quit()
            