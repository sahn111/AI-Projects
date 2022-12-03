import os, copy
"""

Mahmut Ali Sahin
Dogukan Catal

OTELLO GAME

"""

class Board:
    """
        This is the board class, our game will play on this board object, we will use the advantages of OOP in this assignment.

        There are a few functions to play on it or get information from it.
    
        We first initialize our board when we define Board object, the default size is 8.
    """
    def __init__(
        self,
        size : int = 8
    ):
        self.size = size
        self.board = [["0" for x in range(size)] for y in range(size)]
        self.board[3][3] = "2"
        self.board[3][4] = "1"
        self.board[4][3] = "1"
        self.board[4][4] = "2"
        self.possible_x = [-1, 0, 1, -1, 1, -1, 0, 1]
        self.possible_y = [-1, -1, -1, 0, 0, 1, 1, 1]


    def get_board(self):
        """
            This function has one job which is returning the 2D array of board
        """
        return self.board

    def print_play_board(self):
        """
            This is where we print our board.
        """
        mainrow ="     0   1   2   3   4   5   6   7\n   +---+---+---+---+---+---+---+---+\n"
        for i in range(self.size):
            row=" "
            row+=str(i)+" |"
            for j in range(self.size):
                if self.board[i][j]!="0":
                    if self.board[i][j]=="2":
                        row+=" w "
                    else:
                        row+=" b "
                else:
                    row+="   "
                row+="|"
            mainrow+=row+"\n   +---+---+---+---+---+---+---+---+\n"
        return mainrow

    def is_possible_move(self, player):
        """
            By using this function, we check for possible moves. 
            If there is a possible move, this function will return True, otherwise we can understand that
            the game is finished.

            To find possible moves, our algorithm uses other functions of Board class. 
        """
        for y in range(8):
            for x in range(8):
                if self.is_valid(self.board, x, y, player):
                    return False
        return True

    def get_score(self, player):
        """
            There are a few types of scoring for otello game, we picked the one with different 
            scores.

            When you get the corner, you will get more point than edges. 

            In this function we calculate the scores of our table, each Board object has its own functions and
            this improve the functionality of object.
        """
        score = 0
        for y in range(self.size):
            
            for x in range(self.size):
                
                if self.board[y][x] == player:
                
                    if (x == 0 or x == self.size - 1) or (y == 0 or y == self.size - 1):
                        score += 2 
                
                    elif (x == 0 or x == self.size - 1) and (y == 0 or y == self.size - 1):
                        score += 4 
                
                    else:
                        score += 1
        return score

    def is_valid(self, copy_board, x, y, player):
        """
            This function is a tool for othr functions, we use it to add another layer to our control operation.

            It will check if given coordinate is empty or not.

            First it will control the validity of coordinates, then it will use another function of object
            to see if it is a valid move or not.
        """
        if copy_board[y][x] != '0':
            #print("hey1")
            return False

        if x < 0 or x > self.size - 1 or y < 0 or y > self.size - 1:
            #print("hey2")
            return False

        (boardTemp, total_score) = self.play(copy.deepcopy(copy_board), x, y, player, 0)

        if total_score == 0:
            #print("hey3",str(player),str(x),str(y))
            return False
        else:
            return True
    
    def play(self, copy_board, x, y, player, obj): 
        """
            This is the place we do our changes on board, board have to be changed by using this function only.

            This function get the coordinates and player, then it completes the move. While returning it, there are two different
            option

            Moreover, by using this function, we check validations. If the total changed
            cell is zero, it means it is not validate move.
        """
        copy_board[y][x] = player
        total = 0 
        for d in range(self.size): 
            
            ctr = 0
            
            for i in range(self.size):
                x_coordinate = x + self.possible_x[d] * (i + 1)
                y_coordinate = y + self.possible_y[d] * (i + 1)
                
                if x_coordinate < 0 or x_coordinate > self.size - 1 or y_coordinate < 0 or y_coordinate > self.size - 1:
                    ctr = 0; break
                
                elif copy_board[y_coordinate][x_coordinate] == player:
                    break
                
                elif copy_board[y_coordinate][x_coordinate] == '0':
                    ctr = 0; break
                
                else:
                    ctr += 1
            for i in range(ctr):

                x_coordinate = x + self.possible_x[d] * (i + 1)
                y_coordinate = y + self.possible_y[d] * (i + 1)
                copy_board[y_coordinate][x_coordinate] = player

            total += ctr
            
        # Create new board to continue to operations.
        nBoard = Board()
        nBoard.board = copy_board
        if (obj == 1):
            return (nBoard, total)
        else:
            return (nBoard.board, total)

visit=0

def MiniMaxAlphaBeta(board : Board, player, depth, alpha, beta, use_maximize):
    """
        This is the critical algorithm of our assignment.

        Here we make minimalize our workload with Alpha Beta Puridity algorithm.

        This function gets board object, player, depth, and alpha beta.

        These two alpha and beta helps us to filtering. These will stop us to use unecessary possibilities.
        
        It is a simple function in basic, we feed this function with recursive and other check functions of 
        board object.
    """
    global visit
    if depth == 0 or board.is_possible_move(player):
        return board.get_score(player)

    if use_maximize:
        current_value= -9999
        for y in range(board.size):
            for x in range(board.size):
                if board.is_valid(board.board, x, y, player):
                    visit += 1
                    copy_board_object, total = board.play(copy.deepcopy(board.board), x, y, player, 1)
                    current_value= max(current_value, MiniMaxAlphaBeta(copy_board_object, player, depth - 1, alpha, beta,False))
                    alpha = max(alpha, current_value)
                    
                    if beta <= alpha:
                        break
        

        return current_value

    
    else: 
        current_value= 9999
        for y in range(board.size):
            for x in range(board.size):
                if board.is_valid(board.board, x, y, player):
                    visit += 1
                    copy_board_object, total = board.play(copy.deepcopy(board.board), x, y, player, 1)
                    current_value= min(current_value, MiniMaxAlphaBeta(copy_board_object, player, depth - 1, alpha, beta,True))
                    beta = min(beta, current_value)
                    
                    if beta <= alpha:
                        break 

        return current_value

def get_optimum_move(board, player):
    """
        This is a function which we calculate our moves for agency.

        We check for every possibility here by using for loops.

        We either calculate score or possible move, then our agency apply the move. 

        Until the end of the game, we will continue to use same system to win.
            1- Find the optimum move,
            2- Appyle the move,
            3- Check the game status, finish is there is no valid move,
            4- Do it again.
    """
    maxScore= 0
    possible_x = -1; possible_y = -1
    for y in range(board.size):
        for x in range(board.size):
            if board.is_valid(board.board, x, y, player):
                if algorithm == 1:
                    score = MiniMaxAlphaBeta(board, player, 4, -9999, 9999, True)
                if score > maxScore:
                    maxScore= score
                    possible_x = x; possible_y = y
    global visit
    print("Number of visited nodes: {}".format(visit))
    visit = 0
    return (possible_x, possible_y)


if __name__ == '__main__':
    """
        In the main first get user's choices which are :
            1) User vs AI
            2) AI vs AI
        Then ask for the heuristic function :
            1)
            2) Minimax Alpha-Beta Pruning
    """
    print ('Welcome to our OTHELLO GAME')
    print("1: User(Player 1) vs AI(Player 2)")
    print("2: AI(Player 1) vs AI(Player 2)")
    choose = int(input('Choose: '))
    
    print ('\n1: Minimax Alpha-Beta Pruning')
    algorithm = int(input('Select AI Algorithm: '))
    """
        At last, create the Board object.

        Complete operations on Board object.
    """
    board = Board()

    while True:

        if (choose == 1):
            for player in range(2):
                
                print(board.print_play_board())
                
                player = str(player + 1)
                print ("PLAYER {} is playing".format(player))
                
                if board.is_possible_move(player):
                    
                    if player == 1:
                        if not board.is_possible_move(2):
                            print("Player 1 has no any valid move for now. Its PLAYER 2's turn")
                            continue
                    
                    else:
                        if not board.is_possible_move(1):
                            print("Player 2 has no any valid move for now. Its PLAYER 1's turn")
                            continue

                    print ("Game can not continue anymore\nThere are no possible moves")
                    print("Scores :")
                    print ("User: " + str(board.get_score('1')))
                    print ("AI-2 : " + str(board.get_score('2')))
                    if board.get_score("1") > board.get_score("2"):
                        print("WINNER IS USER !!!")
                    elif board.get_score("2") > board.get_score("1"):
                        print("WINNER IS AI !!!")
                    else:
                        print("DRAW !!!")
                    os._exit(0)
                
                if player == '1': 
                    while True:
                        x = y = None
                        x = int(input("X coordinate(column) :"))
                        y = int(input("Y coordinate(row) :"))

                        if x == None or y == None:
                            os._exit(0)

                        if board.is_valid(board.board, x, y, player):
                            (play_board, total) = board.play(board.board, x, y, player, 0)
                            break
                        else:
                            print ('Invalid move! Try again!')
                
                else: 
                    (x, y) = get_optimum_move(board, player)
                    if not (x == -1 and y == -1):
                        (play_board, total) = board.play(board.board, x, y, player, 0)
                        print ('AI played (X Y): ' + str(x) + ' ' + str(y))
       
        else:
            for player in range(2):
                print(board.print_play_board())
                  
                player = str(player + 1)
                print ("PLAYER {} is playing".format(player))
                    
                if board.is_possible_move(player):

                    if player == "1":
                        if not board.is_possible_move("2"):
                            print("Player 1 has no any valid move for now. Its PLAYER 2's turn")
                            continue
                    
                    else:
                        if not board.is_possible_move("1"):
                            print("Player 2 has no any valid move for now. Its PLAYER 1's turn")
                            continue
                    
                    print ("Game can not continue anymore\nThere are no possible moves for each PLAYER")
                    print("Scores :")
                    print ("PLAYER-1: " + str(board.get_score('1')))
                    print ("PLAYER-2 : " + str(board.get_score('2')))
                    if board.get_score("1") > board.get_score("2"):
                        print("WINNER IS PLAYER-1 !!!")
                    elif board.get_score("2") > board.get_score("1"):
                        print("WINNER IS PLAYER-2 !!!")
                    else:
                        print("DRAW !!!")
                    os._exit(0)            
              
                if player == '1': # AI 1 turn
                    (x, y) = get_optimum_move(board, player)
                    if not (x == -1 and y == -1):
                        (play_board, total) = board.play(board.board, x, y, player, 0)
                        print ('AI-1 played (X Y): ' + str(x) + ' ' + str(y))
                
                else: # AI 2 turn
                    (x, y) = get_optimum_move(board, player)
                    if not (x == -1 and y == -1):
                        (play_board, total) = board.play(board.board, x, y, player, 0)
                        print ('AI-2 played (X Y): ' + str(x) + ' ' + str(y))

