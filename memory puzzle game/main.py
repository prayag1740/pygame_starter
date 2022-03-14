import pygame, random

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width
WINDOWHEIGHT = 480 # size of window's height
REVEALSPEED = 8 # speed of boxes reveals and covers
BOXSIZE = 40
GAPSIZE = 10
BOARDWIDTH = 10 #no of colums of icons
BOARDHEIGHT = 7 # no of rows of icons
assert (BOARDHEIGHT * BOARDWIDTH) % 2 == 0, 'Board needs to have an even number for pairs of matches'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2) 

#COLORS
GRAY = (100,100, 100)
NAVBLUE = (60,60,100)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,128,0)
PURPLE = (255,0,255)
CYAN = (0,255,255)

BGCOLOR = NAVBLUE
LIGHTBLUE = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE


DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined"

def main():
    global FPSCLOCK, DISPLAYSURF #global keyword helps us modify global variable from inside the main function
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) #creates a SURFACE window

    mousex = 0 #to store the x coordinate of mouse event
    mousey = 0 # to store the y coordinate of mouse event

    pygame.display.set_caption("Memory game") #for setting caption for the window

    main_board = get_randomized_board()
    revealed_boxes = generate_revealed_boxes_data(False)

    first_selection = None # stores the (x,y) of the first box clicked

    DISPLAYSURF.fill(BGCOLOR) #to fill color to the surface




### CHECK LOGIC
def get_randomized_board():

    icons = [] #list of every possible shape in every possible color
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape, color))

    random.shuffle(icons) #randomize the order of icons list
    num_icons_used = int(BOARDHEIGHT * BOARDWIDTH /2) # no of icons needed
    icons = icons[:num_icons_used] * 2 # make two of each
    random.shuffle(icons)

    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column) 
    return board


#if val is False, will return the board covered and vice versa
def generate_revealed_boxes_data(val):
    #returns the data structure that represents which boxes are covereed
    revealed_boxes = []
    for x in range(BOARDWIDTH):
        revealed_boxes.append([val] * BOARDHEIGHT)
    return revealed_boxes

## CHECK LOGIC
def start_game_animations(board):
    covered_boxes = generate_revealed_boxes_data(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x,y))

    random.shuffle(boxes)

## CHECK LOGIC
def split_into_groups(group_size, the_list):
    result = []
    for i in range(0, len(the_list), group_size):
        result.append(the_list[i:i+group_size])
    return result
