import pygame, random, sys
from pygame.locals import *

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
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

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
    print(f"main board is {main_board}")
    print(f"revealed boxes are {revealed_boxes}")
    
    first_selection = None # stores the (x,y) of the first box clicked

    DISPLAYSURF.fill(BGCOLOR) #to fill color to the surface
    start_game_animations(main_board)

    while True:
        mouse_clicked = False
        DISPLAYSURF.fill(BGCOLOR)

        draw_board(main_board, revealed_boxes) 

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP: #mouse button was pressed erlier and now the button was let up
                mousex, mousey = event.pos
                mouse_clicked = True

        boxx, boxy = get_box_at_pixel(mousex, mousey)
        print(boxx, boxy)
        if boxx != None and boxy != None:
            #mouse currently over a box
            if not revealed_boxes[boxx][boxy]:
                draw_highlight_box(boxx, boxy)
            if not revealed_boxes[boxx][boxy] and mouse_clicked:
                reveal_box_animations(main_board, [(boxx, boxy)])
            

        pygame.display.update()
        FPSCLOCK.tick(FPS)




def draw_highlight_box(boxx, boxy):
    left, top = left_top_coords_box(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left-5, top-5, BOXSIZE+10, BOXSIZE+10), 4)





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
def split_into_groups(group_size, the_list):
    # splits a list into a list of lists where the inner list will have group size number of items in them
    result = []
    for i in range(0, len(the_list), group_size):
        result.append(the_list[i:i+group_size])
    return result


def left_top_coords_box(boxx, boxy):
    #converts the board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return left, top


def get_shape_and_color(board, boxx, boxy):
    # shape for x,y spot --> board[x]board[y][0]
    #color for x,y spot --> board[x]board[y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1] 


def draw_icon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) 
    half = int(BOXSIZE * 0.5)

    left, top =  left_top_coords_box(boxx, boxy) #getting pixel coords from board coords
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter-5)

    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))

    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE -1 , top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))

    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE -1) , (left + BOXSIZE -1 , top + i))

    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


## CHECK LOGIC
def draw_board(board, revealed):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = left_top_coords_box(boxx, boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                shape, color = get_shape_and_color(board, boxx, boxy)
                draw_icon(shape, color, boxx, boxy)


## CHECK LOGIC
def draw_box_cover(board, boxes, coverage):
    for box in boxes:
        left, top = left_top_coords_box(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = get_shape_and_color(board, box[0], box[1])
        draw_icon(shape, color, box[0], box[1])
        if coverage > 0: #only draw the cover if there is a coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
        pygame.display.update()
        FPSCLOCK.tick(FPS)



## CHECK LOGIC
def reveal_box_animations(board, box_to_cover):
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, - REVEALSPEED):
        draw_box_cover(board, box_to_cover, coverage)

##CHECK LOGIC
def cover_box_animations(board, box_to_cover):
    for coverage in range(0, BOXSIZE+REVEALSPEED, REVEALSPEED):
        draw_box_cover(board, box_to_cover, coverage)

## CHECK LOGIC
def start_game_animations(board):
    covered_boxes = generate_revealed_boxes_data(False)
    print(f"covered_boxes are {covered_boxes}")
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x,y))

    random.shuffle(boxes)
    group_size = 8
    box_groups = split_into_groups(group_size, boxes)
    print(f"box groups are {box_groups}")
    draw_board(board, covered_boxes)
    for box_group in box_groups:
        reveal_box_animations(board, box_group)
        cover_box_animations(board, box_group)    



def get_box_at_pixel(x,y):
    #returns the box coordinates from where mouse moved
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = left_top_coords_box(boxx, boxy)
            box_rect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if box_rect.collidepoint(x,y):
                return boxx, boxy
    return None, None


main()





