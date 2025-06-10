################################################################################################
#
#
#           Name: Cardona, Alissha Mae A.
#           Section: WX2L
#           Program: implements bfs, dfs, and A* search in 8-puzzle game. allows user to choose file for initial board
#
#           References:
#           - https://fedingo.com/how-to-open-file-dialog-box-in-python/
#               (for file dialogue)
#
###############################################################################################

import pygame
from _collections import deque
import pyautogui
import tkinter as tk
from tkinter import filedialog
import time

pygame.init() #initialize pygame


#constants
TILESIZE = 100
TOP_MARGIN = 100
LEFT_MARGIN = 47
TOTAL_ROWS = 3
TOTAL_COLS = 3
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 650


dark_blue = (59,89,152)
light_blue = (173,185,211)
white = (255,255,255)
black = (0,0,0)


#images and resize
S1 = pygame.image.load('images/1.png')
S1 = pygame.transform.smoothscale(S1, (TILESIZE, TILESIZE))
S2 = pygame.image.load('images/2.png') 
S2 = pygame.transform.smoothscale(S2, (TILESIZE, TILESIZE))
S3 = pygame.image.load('images/3.png')
S3 = pygame.transform.smoothscale(S3, (TILESIZE, TILESIZE))
S4 = pygame.image.load('images/4.png')
S4 = pygame.transform.smoothscale(S4, (TILESIZE, TILESIZE))
S5 = pygame.image.load('images/5.png')
S5 = pygame.transform.smoothscale(S5, (TILESIZE, TILESIZE))
S6 = pygame.image.load('images/6.png')
S6 = pygame.transform.smoothscale(S6, (TILESIZE, TILESIZE))
S7 = pygame.image.load('images/7.png')
S7 = pygame.transform.smoothscale(S7, (TILESIZE, TILESIZE))
S8 = pygame.image.load('images/8.png')
S8 = pygame.transform.smoothscale(S8, (TILESIZE, TILESIZE))


#set window details
window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("8-puzzle Game (Cardona, WX2L)")
pygame.font.init()
font = pygame.font.SysFont('Arial ',22)




def make_board(file):

    board = []
        
    if file == '':
        input = open('puzzle.in', 'r')
    else:
        input = open(file, 'r')

    # initialize board
    rows = input.readlines()

    for i in rows:
        row = i.strip().split()
        temp = []
        temp.append(int(row[0]))
        temp.append(int(row[1]))
        temp.append(int(row[2]))
        board.append(temp)

    return board



##################################     FOR GAME PROPER     #########################################



def draw_board(board):                                                          #for tile display
    for row in range(TOTAL_ROWS):
        for col in range(TOTAL_COLS):
            if int(board[row][col]) == 1 :
                window.blit(S1,((col*TILESIZE),(row*TILESIZE)))
            elif int(board[row][col]) == 2 :
                window.blit(S2,((col*TILESIZE),(row*TILESIZE)))
            elif int(board[row][col]) == 3 :
                window.blit(S3,((col*TILESIZE),(row*TILESIZE)))
            elif int(board[row][col]) == 4 :
                window.blit(S4,((col*TILESIZE),(row*TILESIZE)))
            elif int(board[row][col]) == 5 :
                window.blit(S5,((col*TILESIZE),(row*TILESIZE)))
            elif int(board[row][col]) == 6 :
                window.blit(S6,((col*TILESIZE),(row*TILESIZE)))
            elif int(board[row][col]) == 7 :
                window.blit(S7,((col*TILESIZE),(row*TILESIZE)))
            elif int(board[row][col]) == 8 :
                window.blit(S8,((col*TILESIZE),(row*TILESIZE)))
            

#move blank tile
def move_right(row,col,board):
    board[row][col-1] = board[row][col]
    board[row][col] = 0

def move_left(row,col,board):
    board[row][col+1] = board[row][col]
    board[row][col] = 0

def move_down(row,col,board):
    board[row-1][col] = board[row][col]
    board[row][col] = 0

def move_up(row,col,board):
    board[row+1][col] = board[row][col]
    board[row][col] = 0


def move_tile(row,col,board):

    if row>2 or col>2:
        pass
    elif col>0 and board[row][col-1] == 0:
        move_right(row,col,board)

    elif col<2 and board[row][col+1] == 0 :
        move_left(row,col,board)

    elif row>0 and board[row-1][col] == 0:
        move_down(row,col,board)

    elif row<2 and board[row+1][col] == 0:
        move_up(row,col,board)

    else:
        pass


def mouse_position(pos):
    x,y = pos
    row = (y//TILESIZE)
    col = (x//TILESIZE)
    return row,col

def solvable_board(board):
    temp = []
    inversions = 0
    for row in range(3):                        #transfer board values to single array
        for col in range(3):
            temp.append(board[row][col])
    
    for i in range(9):                          #count inversions
        for j in range(i,9):
            if temp[i] == 0 or temp[j] == 0:
                pass
            elif temp[i] > temp[j]:
                inversions= inversions+ 1
    print(inversions)
    if (inversions%2) == 0:                    #if inversions are even, solvable
        return True
    else:
        return False


def check_for_win(board,winning_board):

    for row in range(TOTAL_ROWS):
        for col in range(TOTAL_COLS):
            if board[row][col] != winning_board[row][col]:
                return False
    return True


############################################################     START OF EXER2 ADDITIONS    ##########################################################################



def emptyTileCoor(board):                                                   #checks empty tile position
    for row in range(TOTAL_ROWS):
        for col in range(TOTAL_COLS):
            if board[row][col] == 0:
                return row, col


def reverseList(temp):                                                      #reverses any list
    finalList = []
    length = len(temp)
    decrement = 1
    for i in range(length):
        finalList.append(temp[length-decrement])
        decrement += 1
    
    return finalList




def printWin(win, solvable, sol, cost, next_counter, open):
    if win is True:
        message = font.render('You Win!', False, (0, 0, 0))\

        if sol == 1 and next_counter==cost:                                         #pop up to show path cost after all moves are done             
            pyautogui.alert(text = ("path cost: " + str(cost)))
            open = False                                                            #close window

    else:                                         #check if solvable
        if solvable is True:
            message = font.render('Solvable!', False, (0, 0, 0))
        else:
            message = font.render('Impossible!', False, (0, 0, 0))


    window.blit(message, (110,330))
    return open




def draw_moves(moves_list, font, next_counter):
    done = ''
    waiting = ''

    count = 1
    for i in range(len(moves_list)-1):
        if count <= next_counter:
            done = done + moves_list[count] + " "                       #add move to done list(string) to highlight the move
        waiting = waiting + moves_list[count] + " "                     #all moves
        count += 1


    moves_waiting = font.render(waiting, False, light_blue)
    moves_done = font.render(done, False, dark_blue)


    window.blit(moves_waiting, ((WINDOW_WIDTH/2 - 7*count),580))       #display all moves in light color first
    window.blit(moves_done, ((WINDOW_WIDTH/2 - 7*count),580))          #display finished moves in a dark color over the light color




    
def writeFile(actions):                                                  #writes/overwrites actions to puzzle.out
    count = 1
    text = ''
    f = open("puzzle.out", "w")
    for i in range(len(actions)-1):
        text = text + actions[count] + " "
        count += 1
    
    f.write(text)
    f.close()

def openFile():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()

    return file_path


#####################################     NODE CLASS     ###################################################
class Node:
    children = []
    parent = []
    action = ''
    g = 0
    h = 0
    f = 0

    def __init__(self, state):
        self.state = state

    def addChild(self, n):
        self.children.append(n)

    def setParent(self,n):
        self.parent = n

    def getParent(self):
        return self.parent

    def setAction(self,a):
        self.action = a
    
    def getAction(self):
        return self.action
    def setG(self,g):
        self.g = g

    def getG(self):
        return self.g
    def setF(self,g,h):
        self.f = g + h
    
    def getF(self):
        return self.f


##########################################################   FOR BFS AND DFS SEARCH   ##############################################################################


def actions(s):
    #iterate all possible positions of blank tile
    #append each possible move to some node?

    if s[0][0] == 0:          #upper left
        #right,down
        actions = ['R','D']
        
    elif s[0][1] == 0:        #upper center
        #left,down,right
        actions = ['R','D','L']
        
    elif s[0][2] == 0:        #upper right
        #left,down
        actions = ['D','L']
        


    elif s[1][0] == 0:        #mid left
        #up,right,down
        actions = ['U','R','D']
        
    elif s[1][1] == 0:        #mid center
        #down,right,left,up
        actions = ['U','R','D','L']
        
    elif s[1][2] == 0:        #mid right
        #down,left,up
        actions = ['U','D','L']
        


    elif s[2][0] == 0:        #lower left
        #up,right
        actions = ['U','R']
        
    elif s[2][1] == 0:        #lower center
        #right,up,left
        actions = ['U','R','L']
        
    elif s[2][2] == 0:        #lower right
        #left,up
        actions = ['U','L']
        


    else:
        pass
    
    return actions

    

def result(s,a):
    next_state = []

    for row in range(3):
        next_state.append([])
        for col in range(3):
            next_state[row].append(s[row][col])
    
    row,col = emptyTileCoor(next_state)

    if a == 'L'and col>0:
        next_state[row][col] = next_state[row][col-1]
        next_state[row][col-1] = 0

    elif a == 'R'and col<2:
        next_state[row][col] = next_state[row][col+1]
        next_state[row][col+1] = 0

    elif a == 'U' and row>0:
        next_state[row][col] = next_state[row-1][col]
        next_state[row-1][col] = 0
        

    elif a == 'D'and row<2:
        next_state[row][col] = next_state[row+1][col]
        next_state[row+1][col] = 0

    else:
        pass

    return Node(next_state)
    


def goal_test(s):
    winning_board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    if s == winning_board:                      #evaluate if current state is the winning state
        return True
    else:
        return False


def path_cost(path):
    cost = 0
    while path.getParent():                     #counts moves until parent is empty
        cost = cost+1
        path = path.getParent()
    
    return cost

def get_sol_nodes(node):
    finalStates = [node.state]                  #starting value of list is the winning state
    finalMoves = [node.getAction()]             #starting value of list is the last action

    while node.getParent():
        node = node.getParent()                 #evaluate node parent

        finalStates.append(node.state)          #append state to list
        finalMoves.append(node.getAction())     #append action to list
    
    finalStates = reverseList(finalStates)      #reverse both lists
    finalMoves = reverseList(finalMoves)

    return finalStates,finalMoves

    



def in_explored(n,explored):            #deteremine if node state is in explored
    check = False
    for a in explored:
        if a.state == n.state:
            check = True
    
    return check

def in_frontier(n,frontier):           #determine if node state is in frontier
    check = False
    for a in frontier:
        if a.state == n.state:
            check = True
    
    return check

#   queue = list
#   enqueue = append
#   dequeue = pop(0)


def bfsearch(board):

    #change lists to dictionaries please
    frontier = deque([Node(board)])
    explored = []


    while len(frontier)>0:
        currentState = frontier.popleft()
        explored.append(currentState)
        actionsList = actions(currentState.state)

        if goal_test(currentState.state) == True:
            cost = path_cost(currentState)
            print("path: ", cost)
            print("explored: ", len(explored))
            
            finalStates, finalActions = get_sol_nodes(currentState)
            
            return finalStates, finalActions, cost
        else:
            for a in actionsList:
                res = result(currentState.state, a)
                if  in_explored(res,explored)==False and in_frontier(res,frontier) == False:
                    #set up new node
                    res.setParent(currentState)
                    res.setAction(a)

                    #add new node as child to parent
                    currentState.addChild(res)

                    frontier.append(res)
                else:
                    pass
    




#initializations
#   stack = list
#   push = append
#   pop = pop()

def dfsearch(board):
      #change lists to dictionaries please
    frontier = deque([Node(board)])
    explored = []


    while len(frontier)>0:
        currentState = frontier.pop()
        explored.append(currentState)
        actionsList = actions(currentState.state)

        if goal_test(currentState.state) == True:
            cost = path_cost(currentState)
            print("path: ", cost)
            print("explored: ", len(explored))

            finalStates, finalActions = get_sol_nodes(currentState)
            
            return finalStates, finalActions, cost
        else:
            for a in actionsList:
                res = result(currentState.state, a)
                if  in_explored(res,explored)==False and in_frontier(res,frontier) == False:
                    #set up new node
                    res.setParent(currentState)
                    res.setAction(a)

                    #add new node as child to parent
                    currentState.addChild(res)

                    frontier.append(res)
                else:
                    pass
    


############################################   FOR A* SEARCH ################################################################

def man_distance(board):
    win_board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    h = 0

    for win_row in range(3):
        for win_col in range(3):                #row and col for winning board
            for row in range(3): 
                for col in range(3):            #row and col for current board
                    if win_board[win_row][win_col] > 0 and win_board[win_row][win_col] == board[row][col]:      #value on winning board and current board are the same
                        distance = abs(win_col - col) + abs(win_row - row)              #calculate distance
                        h = h + distance                                                #add to h
                    else:
                        pass
    return h



def removeMinF(list):

    least = list[0].getF()
    index = 0
    count = 0

    for i in range(len(list)):
        if list[i].getF() < least:
            least = list[i].getF()
            index = i
        count = count+1
    
    return index

    






def Asearch(board):

    #change lists to dictionaries please
    openList = [Node(board)]
    closedList = []
    openList[0].setG(0)
    openList[0].setF(0,man_distance(board))
    

    while len(openList)>0:  

        bestNode = openList.pop(removeMinF(openList))       #remove minimum F
        closedList.append(bestNode)
        actionsList = actions(bestNode.state)

        if goal_test(bestNode.state) == True:
            cost = path_cost(bestNode)
            print("path: ", cost)
            print("explored: ", len(closedList))
            
            finalStates, finalActions = get_sol_nodes(bestNode)
            
            return finalStates, finalActions, cost

        else:
            for a in actionsList:
                res = result(bestNode.state, a)

                if  in_explored(res,closedList)==False and in_frontier(res,openList) == False:

                    #compute for h per state
                    h = man_distance(res.state)
                    #set up new node
                    res.setParent(bestNode)
                    res.setG(bestNode.getG() + 1)
                    res.setAction(a)
                    res.setF(bestNode.getG()+1,h)

                    #add new node as child to parent
                    bestNode.addChild(res)

                    openList.append(res)
                else:
                    pass
       

############################################   BUTTONS   #####################################################################

def draw_file():
    pygame.draw.rect(window,light_blue,[((WINDOW_WIDTH/2) - 55),365,100,30])
    window.blit(font.render("Select File",True, white), (((WINDOW_WIDTH/2) - 45),365))

def draw_sol():
    pygame.draw.rect(window,light_blue,[160,420,100,30])
    window.blit(font.render("Solution",True, white), (178,421))

def draw_next():
    pygame.draw.rect(window,dark_blue,[160,420,100,30])
    window.blit(font.render("Next",True, white), (190,421))

def draw_bfs():
    pygame.draw.rect(window,light_blue,[40,420,100,30])
    window.blit(font.render("BFS",True, white), (75,421))

def draw_bfs_clicked():
    pygame.draw.rect(window,dark_blue,[40,420,100,30])
    window.blit(font.render("BFS",True, white), (75,421))
    

def draw_dfs():
    pygame.draw.rect(window,light_blue,[40,470,100,30])
    window.blit(font.render("DFS",True, white), (75,471))

def draw_dfs_clicked():
    pygame.draw.rect(window,dark_blue,[40,470,100,30])
    window.blit(font.render("DFS",True, white), (75,471))

def draw_astar():
    pygame.draw.rect(window,light_blue,[40,520,100,30])
    window.blit(font.render("A star",True, white), (67,521))

def draw_astar_clicked():
    pygame.draw.rect(window,dark_blue,[40,520,100,30])
    window.blit(font.render("A star",True, white), (67,521))


def draw_buttons(search, sol_button):
    if sol_button == 0 and search == 0:     #if solution button is not clicked
        draw_sol()
        draw_bfs()
        draw_dfs()
        draw_astar()

    elif sol_button == 0 and search == 1:   #bfs but sol not clicked
        draw_sol()
        draw_bfs_clicked()
        draw_dfs()
        draw_astar()
     

    elif sol_button == 0 and search == 2:   #dfs but sol not clicked
        draw_sol()
        draw_bfs()
        draw_dfs_clicked()
        draw_astar()

    elif sol_button == 0 and search == 3:   #astar but sol not clicked
        draw_sol()
        draw_bfs()
        draw_dfs()
        draw_astar_clicked()
       

    elif sol_button == 1 and search == 1:   #solution button clicked + bfs
        draw_next()
        draw_bfs_clicked()
        draw_dfs()
        draw_astar()

    elif sol_button == 1 and search == 2:   #solution button clicked + bfs
        draw_next()
        draw_bfs()
        draw_dfs_clicked()
        draw_astar()

    else:                                   #solution button clicked + astar
        draw_next()
        draw_bfs()
        draw_dfs()
        draw_astar_clicked()


    draw_file()                             #draw file button always
   

def click_sol(x,y,board,search):
    if (x>160 and x<260) and (y>420 and y<450):
        print("solution clicked")
        if  search == 1:
            print("loading bfs...")
            sol_board,sol_moves,cost = bfsearch(board)
        elif search == 2:
            print("loading dfs...")
            sol_board,sol_moves,cost = dfsearch(board)
        else:
            print("loading Astar...")
            sol_board,sol_moves,cost = Asearch(board)
        writeFile(sol_moves)
        return 1, sol_board, sol_moves,cost
    else:
        return 0,[],[],0

def click_next(x,y,count):
    if (x>160 and x<260) and (y>420 and y<450):
        count = count + 1
        print("next clicked")
    return count

def click_bfs(x,y,s):
    if (x>40 and x<140) and (y>420 and y<450):
        print("bfs clicked")
        return 1
    else:
        return s

def click_dfs(x,y,s):
    if x>40 and x<140 and y>470 and y<500:
        print("dfs clicked")
        return 2
    else:
        return s

def click_astar(x,y,s):
    if x>40 and x<140 and y>520 and y<550:
        print("astar clicked")
        return 3
    else:
        return s

def click_file(x,y,file):
    if x>95 and x<195 and y>365 and y<395:
        print("file dialogue clicked")
        return openFile(),1
    else:
        return file,0




######################################   DEFINE MAIN   ################################################ 

def main(board):
    
    open = True
    sol_button = 0      #solution button checker
    search = 0          #search option checker
    file_button = 0     #open file button
    next_counter = 0
    next = 0

    file = 'puzzle.in'

    initial = make_board(file)
    winning_board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    solvable = solvable_board(board)

    win = False

    while open:
        for event in pygame.event.get():                                                               #checks for events that have happened
            if event.type==pygame.QUIT:                                                                #if exit button pressed
                open = False

            if event.type == pygame.MOUSEBUTTONDOWN:                                                   #if mouse button clicked
                pos = pygame.mouse.get_pos()                                                           #get mouse position
                x,y = pos
                row, col = mouse_position(pos)                                                         #get x and y values from position
                man_distance(board)
                
                if file_button == 0:                                                                   #search file button is pressed
                    file,file_button = click_file(x,y,file)

                if file_button == 1:
                    board = make_board(str(file))
                    initial = make_board(str(file))
                    solvable = solvable_board(board)
                    file_button = 0
                
                
                if sol_button == 0 and search == 0:                                                    #if solution button + search buttons not clicked
                    move_tile(row,col,board)                                                           #move tile accordingly

                    search = click_dfs(x,y,search)
                    search = click_bfs(x,y,search)
                    search = click_astar(x,y,search)

                elif sol_button == 0 and search == 1:                                                  #bfs but sol not clicked
                    move_tile(row,col,board)
                    start_time = time.perf_counter()
                    sol_button, sol_board, sol_moves,cost = click_sol(x,y,initial,search)              #allow clickage of solution only
                    print(time.perf_counter() - start_time, "seconds")
                    search = click_dfs(x,y,search)
                    search = click_astar(x,y,search)
                    next = 1
                    

                elif sol_button == 0 and search == 2:                                                  #dfs but sol not clicked
                    move_tile(row,col,board)
                    start_time = time.perf_counter()
                    sol_button, sol_board, sol_moves,cost = click_sol(x,y,initial,search)              #allow clickage of solution only
                    print(time.perf_counter() - start_time, "seconds")
                    search = click_bfs(x,y,search)
                    search = click_astar(x,y,search)
                    next = 1

                elif sol_button == 0 and search == 3:                                                  #A* but sol not clicked
                    move_tile(row,col,board)
                    start_time = time.perf_counter()
                    sol_button, sol_board, sol_moves,cost = click_sol(x,y,initial,search)              #allow clickage of solution only
                    print(time.perf_counter() - start_time, "seconds")
                    search = click_bfs(x,y,search)
                    search = click_dfs(x,y,search)
                    next = 1

                elif next == 1:
                    next_counter = click_next(x,y,next_counter)                                        #allow clickage of next only
                    
                     
                else:
                    pass
        
        window.fill(white)                                                                     #white background color

        if sol_button == 0:
            draw_board(board)                                                                  #display tiles
            win = check_for_win(board, winning_board)
            printWin(win,solvable,sol_button,0,next_counter,open) 

        elif sol_button == 1:
            open = printWin(win,solvable,sol_button,cost,next_counter,open)                    #printwin first to update board before pop up appears

            if next_counter <= cost:
                draw_board(sol_board[next_counter])
                draw_moves(sol_moves, font, next_counter)
                win = check_for_win(sol_board[next_counter], winning_board)                    #check for win
             


        draw_buttons(search,sol_button)
 
        

        pygame.display.update()


################################    EXECUTE MAIN()    ###############################################

main(make_board('puzzle.in'))
