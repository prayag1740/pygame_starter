#simple pygame program

import pygame
pygame.init()

screen = pygame.display.set_mode([500,500])

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #filling screen with white color
    screen.fill((255,255,255))

    pygame.draw.circle(screen, (0,0,255), (250, 250), 75) #parameters -- screen; tuple of color ; position of circle ; radius of circle

    #flip the display ; updates the contents of display on screen
    pygame.display.flip()

pygame.quit()