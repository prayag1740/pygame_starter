import pygame
import random
import time

#importing constants for easier access to key coordinates
from pygame.locals import (
    RLEACCEL,
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
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))


#game imp 
"""
1) processes user input
2) updates the state of game objects
3) updates the display and audio output
4)maintains the speed of the game
"""
#Sprites Group -- group of sprite objects


#sprite is a 2D representation of any object on the screen
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__() #call init method of Sprit class
        self.surf = pygame.image.load('enemy_escape_game/assets/cropped_player.jpeg').convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (50,50))
        self.rect = self.surf.get_rect()

    
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)

        #keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <=0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT



class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load('enemy_escape_game/assets/bullet.jpeg').convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (40,40))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH+20, SCREEN_HEIGHT+20),
                random.randint(0, SCREEN_HEIGHT),              
            )
        )
        self.speed = random.randint(5, 120)

    def update(self):
        self.rect.move_ip(-self.speed,0) #moves the enemy to the left side of screen
        if self.rect.right <0: #checking right right of rect <0
            self.kill()  #removes the sprite from every group it belonged



running = True
player = Player()

#creating groups of sprites
# enemies -- used for collision detection and position updates
# all_sprites -- used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

ADDENEMY = pygame.USEREVENT + 1  #defining a unique event for pygame
pygame.time.set_timer(ADDENEMY, 250) #adds event in event queue after every 250 ms

start_time = time.time()

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN: #if user pressed a key
            if event.key == K_ESCAPE: #if it was an escape key
                running = False

        elif event.type == QUIT: #if user closed the window
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    #white background for screen
    screen.fill((0, 0, 0))

    #creates a surface (rectangular object)and params are length and width
    surf = pygame.Surface((50, 50))

    surf.fill((0,0,0)) #seperate color for surface then screen
    rect = surf.get_rect()

    surf_center = (
        (SCREEN_WIDTH/2),
        (SCREEN_HEIGHT/2)
    )


    # screen.blit(player.surf, player.rect) #places one surface on another; 2nd argument here is the position

    pressed_keys = pygame.key.get_pressed() #get set of keys pressed and check for user input
    player.update(pressed_keys)

    enemies.update()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    #checks if player collides with any sprite in the enemies group
    if pygame.sprite.spritecollideany(player, enemies):
        end_time = time.time()
        time_played = end_time - start_time
        print(f"oops you lost {time_played}")
        player.kill()
        running = False 

    pygame.display.flip() #displays actual

pygame.quit()
            