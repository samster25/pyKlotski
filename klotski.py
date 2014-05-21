
import random, pygame, sys
from pygame.locals import *
from time import sleep

WINDOWWIDTH = 800 # size of window's width in pixels
WINDOWHEIGHT = 600 # size of windows' height in pixels
BORDER = 2

BOARDWIDTH = 4 # number of columns of icons
BOARDHEIGHT = 5 # number of rows of icons
GAPSIZE = 5 # size of gap between boxes in pixels
BOXSIZE = (WINDOWHEIGHT-5*BORDER)//5 # size of box height & width in pixels

#            R    G    B
GRAY     = (50,   50,  50)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)

tiles = {}

for row in range(5):
    for col in range(4):
        tiles[(row,col)] = None

total_moves = 0

class Piece:
    def __init__(self, r, c, w, h, color,winner=False):
        self.r = r
        self.c = c
        self.w = w
        self.h = h
        self.winner = winner
        self.color = color
        self.selected = False


        if w > 1 or h > 1:
            self.multi = True
        else:
            self.multi = False

    @property   
    def is_empty(self):
        return False

    def __repr__(self):
        for typ in (TallPiece, WidePiece, SmallPiece, BigPiece, EmptyPiece):
            if isinstance(self, typ):
                form = typ
                break

        return str(form) + " @ (" + str(self.r) +", " + str(self.c) +")"

    def check_col(self, dr, dc):
        if abs(dr) > 1 and abs(dc) > 1:
            return False
        if self.r + dr + self.h > 5 or self.r + dr < 0:
            return False
        if self.c + dc + self.w > 4 or self.c + dc < 0:
            return False 


        if dr and dc:   
            if not isinstance(self, SmallPiece):
                return False
            if not tiles[(self.r+dr,self.c+dc)].is_empty:
                return False
            if not (tiles[(self.r+dr,self.c)].is_empty or tiles[(self.r,self.c+dc)].is_empty):
                return False

        elif dr:
            if dr > 0:
                for row in range(self.r, self.r + dr):
                    for col in range(self.c, self.c+self.w):
                        if not tiles[(row+self.h,col)].is_empty:
                            return False
            else:
                for row in range(self.r+dr, self.r):
                    for col in range(self.c, self.c+self.w):
                        if not tiles[(row,col)].is_empty:
                            return False 
        elif dc:
            if dc > 0:
                for col in range(self.c, self.c + dc):
                    for row in range(self.r, self.r+self.h):
                        if not tiles[(row,col+self.w)].is_empty:
                            return False
            else:
                for col in range(self.c+dc, self.c):
                    for row in range(self.r, self.r+self.h):
                        if not tiles[(row,col)].is_empty:
                            return False

        print("Can swap!     ")
        return True

    def update_lo(self, r, c):
        self.r = r
        self.c = c
        updateTiles(self)       


class TallPiece(Piece):
    def __init__(self, r, c):
        Piece.__init__(self, r, c, 1, 2, YELLOW)
        updateTiles(self)

class WidePiece(Piece):
    def __init__(self, r, c):
        Piece.__init__(self, r, c, 2, 1, GREEN)
        updateTiles(self)

class SmallPiece(Piece):
    def __init__(self, r, c):
        Piece.__init__(self, r, c, 1, 1, PURPLE)
        updateTiles(self)

class BigPiece(Piece):
    def __init__(self, r, c):
        Piece.__init__(self, r, c, 2, 2, RED, True)
        updateTiles(self)

class EmptyPiece(Piece):
    def __init__(self, r, c):
        Piece.__init__(self, r, c, 1, 1, GRAY)
        updateTiles(self)

    @property   
    def is_empty(self):
        return True


def updateTiles(piece):
    for row in range(piece.h):
        for col in range(piece.w):
            tiles[(piece.r+row, piece.c+col)] = piece

def move(start,to):
    r0 = start[0]
    c0 = start[1]
    r1 = to[0]
    c1 = to[1]

    dr = r1-r0
    dc = c1-c0

    sel_piece = tiles[start]
    emp_piece = tiles[to]

    ori_row = sel_piece.r
    ori_col = sel_piece.c
    if not sel_piece.check_col(dr,dc):
        return False
    
    if isinstance(sel_piece, EmptyPiece):
        return False

    elif dr and dc:
        sel_piece.update_lo(r1,c1)
        emp_piece.update_lo(r0,c0)

    elif dr:
        
        if dr > 0:
            for row in range(dr):
                for col in range(sel_piece.c, sel_piece.c+sel_piece.w):
                    tiles[(ori_row+sel_piece.h+row,col)].update_lo(ori_row + row ,col)

        else:
            for row in range(abs(dr)):
                for col in range(sel_piece.c, sel_piece.c+sel_piece.w):
                    tiles[(ori_row - row -1,col)].update_lo(ori_row+sel_piece.h-row-1,col)                  
        sel_piece.update_lo(sel_piece.r + dr, sel_piece.c)

    else:

        if dc > 0:
            for col in range(dc):
                for row in range(sel_piece.r, sel_piece.r+sel_piece.h):
                    tiles[(row, ori_col+sel_piece.w+col)].update_lo(row, ori_col+col)

        else:
            for col in range(abs(dc)):
                for row in range(sel_piece.r, sel_piece.r+sel_piece.h):
                    tiles[(row, ori_col-col-1)].update_lo(row, ori_col+sel_piece.w-col-1)

        sel_piece.update_lo(sel_piece.r, sel_piece.c+dc)

    global total_moves
    total_moves += 1
    return True

def setup():
    global pieces
    pieces = {
        "tall_1": TallPiece(0,0),
        "big_1": BigPiece(0,1),
        "tall_2": TallPiece(0,3),
        "tall_3": TallPiece(2,0),
        "wide_1": WidePiece(2,1),
        "tall_4": TallPiece(2,3),
        "small_1": SmallPiece(3,1),
        "small_2": SmallPiece(3,2),
        "small_3": SmallPiece(4,0),
        "small_4": SmallPiece(4,3),
        "empty_1": EmptyPiece(4,1),
        "empty_2": EmptyPiece(4,2)
    }

def print_tiles():
    a = tiles.items()
    a.sort()
    for item in a:
        print item


def main():
    global DISPLAYSURF, total_moves
    total_moves = 0
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    last_sel = None
    setup()
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('pyKlotski')
    win_tile = pieces["big_1"]
    myfont = pygame.font.SysFont("Arial", 36)

    while True: # main game loop

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mousex, mousey = pygame.mouse.get_pos()
                col = mousex // BOXSIZE
                row = mousey // BOXSIZE
                if 4 > col and 5 > row:
                    print(row,col)
                    print(repr(tiles[(row,col)]))

                    if last_sel is not None and last_sel is not tiles[(row,col)]:
                        contin = True
                        dr = row - l_r
                        dc = col - l_c
                        if dr < 0:
                            l_r = last_sel.r
                        else:
                            l_r = last_sel.r+last_sel.h-1

                        if dc > 0:
                            l_c = last_sel.c+last_sel.w-1
                        else:
                            l_c = last_sel.c

                        if not move((l_r, l_c), (row,col)):
                            for _r in range(last_sel.r,last_sel.r+last_sel.h):
                                for _c in range(last_sel.c, last_sel.c+last_sel.w):

                                    if move((_r, _c), (row,col)):
                                        contin = False
                                        break
                        
                        last_sel.selected = False

                    if not isinstance(tiles[(row,col)], EmptyPiece):
                        last_sel = tiles[(row,col)]
                        last_sel.selected = True
                        l_r,l_c = row,col
                        print(last_sel)

        if (win_tile.r, win_tile.c) == (3,1):
            DISPLAYSURF.fill(BLACK)
            win_label = myfont.render("WINNER", 1, WHITE)
            DISPLAYSURF.blit(win_label, (400,300))
            sleep(10)
            break


        DISPLAYSURF.fill(BLACK)


        label = myfont.render("Total Moves: "+ str(total_moves), 1, WHITE)
        sammy_name = myfont.render("Sammy Sidhu",1, GREEN)
        darshan_name = myfont.render("Darshan Parajuli",1 , (0,150,255))
        sheng_name = myfont.render("Sheng Xi", 1, RED)

        for num, lab in enumerate((label,sammy_name,darshan_name,sheng_name)):
            DISPLAYSURF.blit(lab,(4*BOXSIZE + 20, 50*num+50))

        for name,pic in pieces.items():
            pygame.draw.rect(DISPLAYSURF, pic.color, (BOXSIZE*pic.c+BORDER,BOXSIZE*pic.r+BORDER,BOXSIZE*pic.w-2*BORDER,BOXSIZE*pic.h-2*BORDER))
        if last_sel is not None:
            pygame.draw.rect(DISPLAYSURF, WHITE, (BOXSIZE*last_sel.c+BORDER,BOXSIZE*last_sel.r+BORDER,BOXSIZE*last_sel.w-2*BORDER,BOXSIZE*last_sel.h-2*BORDER), 5)
        pygame.display.update()

        sleep(.01)


main()

if __name__ == "__main__":
    main()
