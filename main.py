import pygame, sys, math, random
from collections import deque

pygame.init()
screen = pygame.display.set_mode((540,540))
pygame.display.set_caption('ULTIMATETICTACTOE')
clock = pygame.time.Clock()
#####################################################################################
#SPECIFIC RULES
#If the previous player's small square's corresponding big square on the board has a finished game, 
# the current player is free to move where they want HEADACHE RULE UGHHHH

game_surf = pygame.Surface((540,540))
game_rect = game_surf.get_rect(topleft = (0,0))

pygame.Surface.fill(game_surf, "White")

pygame.draw.line(game_surf, "Black", (174,10), (174,530), 8)
pygame.draw.line(game_surf, "Black", (354,10), (354,530), 8)
pygame.draw.line(game_surf, "Black", (10,174), (530,174), 8)
pygame.draw.line(game_surf, "Black", (10,354), (530,354), 8)

board = [
    pygame.Rect(0,0,180,180),
    pygame.Rect(180,0,180,180),
    pygame.Rect(360,0,180,180),
    pygame.Rect(0,180,180,180),
    pygame.Rect(180,180,180,180),
    pygame.Rect(360,180,180,180),
    pygame.Rect(0,360,180,180),
    pygame.Rect(180,360,180,180),
    pygame.Rect(360,360,180,180),
]

def getSquare(mouse):
    bigx = mouse[0] // 180
    bigy = mouse[1] // 180

    smallx = mouse[0] % 180
    smally = mouse[1] % 180
    if smallx > 5 and smallx < 56:
        x = bigx * 3 
    elif smallx > 56 and smallx < 116:
        x = bigx * 3 + 1
    elif smallx > 116 and smallx < 166:
        x = bigx * 3 + 2
    else: return -1, -1

    if smally > 5 and smally < 56:
        y = bigy * 3
    elif smally > 56 and smally < 116:
        y = bigy * 3 + 1
    elif smally > 116 and smally < 166:
        y = bigy * 3 + 2
    else: return -1, -1

    return y, x
    

def valid(pos, grid, biggrid):
    coord = getSquare(pos)
    bigx = coord[0] // 3
    bigy = coord[1] // 3
    if biggrid[bigx][bigy] != 0: #array cartesian discrepancy
        return False
    if grid[bigx][bigy][coord[0] % 3][coord[1] % 3] != 0:
        return False
    return True

def rule(pos, last):
    coord = getSquare(pos)
    bigx = coord[0] // 3
    bigy = coord[1] // 3
    if last != [-1,-1]:
        if last[0] != bigx or last[1] != bigy:
            return False
    return True
    
def tictactoe(grid):
    if (grid[0][0] == -1 and grid[0][1] == -1 and grid[0][2] == -1) or (grid[1][0] == -1 and grid[1][1] == -1 and grid[1][2] == -1) or (grid[2][0] == -1 and grid[2][1] == -1 and grid[2][2] == -1):
        return -1
    if (grid[0][0] == -1 and grid[1][0] == -1 and grid[2][0] == -1) or (grid[0][1] == -1 and grid[1][1] == -1 and grid[2][1] == -1) or (grid[0][2] == -1 and grid[1][2] == -1 and grid[2][2] == -1):
        return -1
    if (grid[0][0] == -1 and grid[1][1] == -1 and grid[2][2] == -1) or (grid[2][0] == -1 and grid[1][1] == -1 and grid[0][2] == -1):
        return -1
    
    if (grid[0][0] == 1 and grid[0][1] == 1 and grid[0][2] == 1) or (grid[1][0] == 1 and grid[1][1] == 1 and grid[1][2] == 1) or (grid[2][0] == 1 and grid[2][1] == 1 and grid[2][2] == 1):
        return 1
    if (grid[0][0] == 1 and grid[1][0] == 1 and grid[2][0] == 1) or (grid[0][1] == 1 and grid[1][1] == 1 and grid[2][1] == 1) or (grid[0][2] == 1 and grid[1][2] == 1 and grid[2][2] == 1):
        return 1
    if (grid[0][0] == 1 and grid[1][1] == 1 and grid[2][2] == 1) or (grid[2][0] == 1 and grid[1][1] == 1 and grid[0][2] == 1):
        return 1
    return 0

# FLASHY GAMEOVER SCREEN

initialize = 1
Game = True
while Game:
    if initialize:
        biggrid = [
            [0 , 0 , 0], [0 , 0 , 0], [0 , 0 , 0]
        ]
        grid = [
            [[[0 , 0 , 0], [0 , 0 , 0], [0 , 0 , 0]],[[0 , 0 , 0], [0 , 0 , 0], [0 , 0 , 0]],[[0 , 0 , 0], [0 , 0 , 0], [0 , 0 , 0]]],
            [[[0 , 0 , 0], [0 , 0 , 0], [0 , 0 , 0]],[[0 , 0 , 0], [0 , 0 , 0], [0 , 0 , 0]],[[0 , 0 , 0], [0 , 0 , 0], [0 , 0 , 0]]],
            [[[0 , 0 , 0], [0 , 0 , 0], [0 , 0 , 0]],[[0 , 0 , 0], [0 , 0 , 0], [0 , 0 , 0]],[[0 , 0 , 0], [0 , 0 , 0], [0 , 0 , 0]]]
        ]
        turn = 1
        last = [-1,-1]
        all = 1
        initialize = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        mouse = pygame.mouse.get_pos()
        pos = getSquare(mouse)
        if event.type == pygame.MOUSEBUTTONDOWN and valid(mouse, grid, biggrid) and rule(mouse, last) and getSquare(mouse) != (-1,-1):
            grid[pos[0] // 3][pos[1] // 3][pos[0] % 3][pos[1] % 3] = turn
            last[0] = pos[0] % 3; last[1] = pos[1] % 3
            turn = 0 - turn

        elif event.type == pygame.MOUSEBUTTONDOWN and tictactoe(grid[last[0]][last[1]]) != 0:
            grid[pos[0] // 3][pos[1] // 3][pos[0] % 3][pos[1] % 3] = turn
            last[0] = pos[0] % 3; last[1] = pos[1] % 3
            turn = 0 - turn

    if tictactoe(grid[last[0]][last[1]]) != 0:
        all = 1
    else: all = 0

    for i in range(3):
        for j in range(3):
            if tictactoe(grid[i][j]) != 0:
                biggrid[i][j] = tictactoe(grid[i][j])

    #####################################################################################
    ##################################################################################### DISPLAY
    screen.blit(game_surf, game_rect)

    for i in board:
        pygame.draw.line(game_surf, "Black", (i[0]+54,i[1]+6), (i[0]+54,i[1]+166), 4)
        pygame.draw.line(game_surf, "Black", (i[0]+114,i[1]+6), (i[0]+114,i[1]+166), 4)
        pygame.draw.line(game_surf, "Black", (i[0]+6,i[1]+54), (i[0]+166,i[1]+54), 4)
        pygame.draw.line(game_surf, "Black", (i[0]+6,i[1]+114), (i[0]+166,i[1]+114), 4)
    ##################################################################################### fancy selected highlight
    if valid(mouse, grid, biggrid) and all == 1 or valid(mouse, grid, biggrid) and rule(mouse, last) :
        ex = ((pos[0] // 3) * 180) + ((pos[0] % 3) * 60)
        why = ((pos[1] // 3) * 180) + ((pos[1] % 3) * 60)
        highlight = pygame.Surface((50,50))
        if turn == 1:
            highlight.fill("Red")
        else:
            highlight.fill("Blue")
        highlight.set_alpha(150)
        screen.blit(highlight, (why,ex))
    ##################################################################################### NORMAL O AND X'S
    for n in range(3):
        for i in range(3):
            for j in range(3):
                for k in range(3):

                    y = n*180 + j*60
                    x = i*180 + k*60
                    if grid[n][i][j][k] == 1:
                        pygame.draw.line(screen, "Red", (x, y), (x+48, y+48), 8)
                        pygame.draw.line(screen, "Red", (x+48, y), (x, y+48), 8)
                    if grid[n][i][j][k] == -1:
                        pygame.draw.circle(screen, "Blue", (x+24, y+24), 24, 8)
    #####################################################################################  INVALID BIG GRIDS
    for i in range(3):
        for j in range(3):
            if (i != last[0] or j != last[1]) and last[0] != -1 and all == 0:
                invalid = pygame.Surface((180,180)) 
                invalid.fill("Black")
                invalid.set_alpha(90)
                screen.blit(invalid, (j*180, i*180))
    #####################################################################################  BIG O AND X'S        
    for i in range(3):
        for j in range(3):
            if biggrid[i][j] == 1:
                pygame.draw.line(screen, "Red", (j*180, i*180), (j*180+170,i*180+170), 16)
                pygame.draw.line(screen, "Red", (j*180+170, i*180), (j*180,i*180+170), 16)
            if biggrid[i][j] == -1:
                pygame.draw.circle(screen, "Blue", (j*180+85, i*180+85), 85, 16)
    #####################################################################################
    ### LOSE/WIN CONDITION
    if tictactoe(biggrid) == 1:
        redwins = pygame.Surface((520,520))
        redwins.fill("Red")
        redwins.set_alpha(60)
        screen.blit(redwins, (10,10))
        pygame.draw.line(screen, "Red", (10,10), (530,530), 24)
        pygame.draw.line(screen, "Red", (530,10), (10,530), 24)
        pygame.display.flip()
        pygame.time.wait(5000)
        initialize = 1

    if tictactoe(biggrid) == -1:
        bluewins = pygame.Surface((520,520))
        bluewins.fill("Blue")     
        bluewins.set_alpha(60)
        screen.blit(bluewins, (10,10))
        pygame.draw.circle(screen, "Blue", (270,270), 260, 24)
        pygame.display.flip()
        pygame.time.wait(5000)
        initialize = 1

    pygame.display.flip()
    clock.tick(60)
