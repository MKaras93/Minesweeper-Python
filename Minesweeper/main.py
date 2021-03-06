from random import *
from graphics import *
import time

def main():
    
    #Variables
    matrix = []
    h = 9
    w = 9
    bombs = 10
    plates = [] # Buttons on top of the numbers
    isPlaying = True
    
    win = drawWindow(w, h)
    win.update()
    
    #Start loading time...
    time_start = time.perf_counter()
    
    #Methods
    initBoard(matrix, w, h)
    addBombs(matrix, bombs, w, h)
    #addNumbers(matrix, w, h)
    #drawBoardNumbers(win, matrix, w, h)
    drawCoverPlates(win, matrix, w, h, plates)
    
    win.update()
    
    #End loading time
    time_end = time.perf_counter() - time_start
    print("Time to load:",time_end)
    
    #Main Game
    while isPlaying:
        click = win.checkMouse()
        clickPos = processClick(click)
        
        if clickPos != None:
            isPlaying = checkNumber(win, matrix, int(clickPos.getX()), int(clickPos.getY()), w, h)
            undrawCover(clickPos, plates, w)
            
        win.update()
        
    showAllBombs(win, matrix, plates, w)
    
##  All methods below this  ##

'''When the player loses the game all the bombs are revealed'''
def showAllBombs(win, matrix, plates, w):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "b":
                plates[int(j + w*i)].undraw()
                drawBomb(win, i, j)
    
'''Undraws the clicked button'''
def undrawCover(pos, plates, w):
    x = pos.getX()
    y = pos.getY()
    plates[int(x + (w * y))].undraw()

'''Transforms the clicked position to a grid position'''
def processClick(click):
    if click != None:
        x = click.getX()
        y = click.getY()
        x = int(x / 16)
        y = int(y / 16)
        return Point(x, y)
    return None

'''Draws the window, dynamic to the number of squares'''
def drawWindow(w, h):
    win = GraphWin("Minesweeper", w*16, h*16, autoflush=False) ## autoflush=False
    return win

'''Draws all the cover buttons of the grid'''
def drawCoverPlates(win, matrix, w, h, plates):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            plates.append(drawPlate(win, matrix, i, j))
            
'''Draws the cover button in the position retrieved'''
def drawPlate(win, matrix, i, j):
    pic = "../Resources/block.gif"
    cover = Image(Point(j*16+8, i*16+8), pic)
    cover.draw(win)
    return cover

# def drawBoardNumbers(win, matrix, w, h):
#     for i in range(len(matrix)):
#         for j in range(len(matrix[i])):
#             if matrix[i][j] != " ":
#                 drawNumber(win, matrix[i][j], i, j)
                
'''Draws the remaining bombs after the player lost the game'''
def drawBomb(win, i, j):
    pic = "../Resources/b.gif"
    pict = Image(Point(j*16+8, i*16+8), pic)
    pict.draw(win)

'''Draws the number on the screen (also applies for bombs)'''
def drawNumber(win, num, i, j):
    pic = "../Resources/" + num + ".gif"
    picture = Image(Point(j*16+8, i*16+8), pic)
    picture.draw(win)

'''Initializes the board array with empty values'''
def initBoard(matrix, w, h):
    for i in range(h):
        matrix.append([" "] * w)

'''Adds the bombs to random place in the board array'''
def addBombs(matrix, bombs, w, h):
    for i in range(bombs):
        y = randint(0, h)-1
        x = randint(0, w)-1
        while matrix[y][x] == "b":
            y = randint(0, h)-1
            x = randint(0, w)-1
        matrix[y][x] = "b"

'''Gets and draws the number in the position of the click'''
def checkNumber(win, matrix, x, y, w, h):
    if matrix[y][x] == " " or matrix[y][x] == "b":
        matrix[y][x] = checkAround(matrix, y, x, w, h)
        drawNumber(win, matrix[y][x], y, x)
        
        if matrix[y][x] == "exp":
            return False
        else:
            return True
            
    return True
        
# def addNumbers(matrix, w, h):
#     for i in range(len(matrix)):
#         for j in range(len(matrix[i])):
#             if matrix[i][j] == " ":
#                 matrix[i][j] = checkAround(matrix, i, j, w, h)
            
'''Checks around the clicked position for bombs (Gets values for Check())'''
def checkAround(matrix, i, j, w, h):
    bombsFound = 0
    w = w-1
    h = h-1
    
    #If its a bomb, explode
    if matrix[i][j] == "b":
        return "exp"
    
    #Checks the position of the clicked button
    if j > 0 and j < w:
        if i == 0:
            bombsFound += Check(matrix, i, j, 0, 2, -1, 2) #Top check
        elif i == h:
            bombsFound += Check(matrix, i, j, -1, 1, -1, 2) #Bottom Check
        else:
            bombsFound += Check(matrix, i, j, -1, 2, -1, 2) #Full Check
    else:
        if i == 0:
            if j == 0:
                bombsFound += Check(matrix, i, j, 0, 2, 0, 2) #Top Left Check
            else:
                bombsFound += Check(matrix, i, j, 0, 2, -1, 1) #Top Right Check
        elif i == h:
            if j == 0:
                bombsFound += Check(matrix, i, j, -1, 1, 0, 2) #Bottom Left Check
            else:
                bombsFound += Check(matrix, i, j, -1, 1, -1, 1) #Bottom Right Check
        else:
            if j == 0:
                bombsFound += Check(matrix, i, j, -1, 2, 0, 2) #Left Check
            else:
                bombsFound += Check(matrix, i, j, -1, 2, -1, 1) #Right Check
            
    return str(bombsFound)
    
'''Complement of checkAround (Actually checks around)'''
def Check(matrix, i, j, s1, e1, s2, e2):
    val = 0
    
    for line in range(s1, e1):
        for row in range(s2, e2):
            if matrix[int(i+line)][int(j+row)] == "b":
                val += 1
    return val
        
main()
