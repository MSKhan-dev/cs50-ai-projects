"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = 0
    count_o = 0

    for i in range(3):
        for j in range(3):
            if(board[i][j] ==  "X"):
                count_x +=1
            elif(board[i][j] ==  "O"):
                count_o +=1

    if(count_o < count_x):
        return O
    return X

    #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i,j))
    return actions


   # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if(action not in actions(board)):
        raise ValueError("Invalid action.")
    else:
        p = player(board)
        board_copy = copy.deepcopy(board)
        board_copy[action[0]][action[1]] = p
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    count_x_row =0
    count_o_row =0

    count_x_col = 0
    count_o_col = 0

    count_x_diag = 0
    count_o_diag = 0

    count_x_diag_1 = 0
    count_o_diag_1 = 0
    for i in range(3):
        for j in range(3):
            if(board[i][j] == X):
                count_x_row +=1
            elif(board[i][j] == O):
                count_o_row +=1

            if(board[j][i] == X):
                count_x_col +=1
            elif (board[j][i] == O):
                count_o_col +=1

            if(i == j and board[i][j] == X):
                count_x_diag +=1
            elif (i == j and board[i][j] == O):
                count_o_diag += 1

            if (i+j ==2 and board[i][j] == X):
                count_x_diag_1 +=1
            elif (i+j ==2 and board[i][j] == O):
                count_o_diag_1 +=1

        if (count_o_row == 3 or count_o_col ==3):
            return O
        elif (count_x_row == 3 or count_x_col == 3):
            return X

        #reset lại biến đếm
        count_x_row = 0
        count_x_col = 0
        count_o_row = 0
        count_o_col = 0

    if (count_o_diag == 3 or count_o_diag_1 ==3):
        return O
    elif(count_x_diag == 3 or count_x_diag_1 ==3):
        return X
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    count =0
    for i in range(3):
        for j in range(3):
            if(board[i][j] != EMPTY):
                count +=1

    #Khi màng game bị đầy và không ai thắng
    if(count == 9 and (winner(board) == None)): #bị sót trường hợp
        return True

    #Khi một trong hai người thắng
    if(winner(board) == X or winner(board) == O):
        return True

    #Các trường hợp còn lại fail hết
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    p = player(board)

    if(p==X):
        #Chọn action có giá trị lớn nhất
        value = float("-inf")
        action_select = None

        for action in actions(board):
            minValueResult = minValue(result(board, action))

            if minValueResult > value:
                value = minValueResult
                action_select = action

    elif(p==O):
        #chọn action có giá trị nhỏ nhất
        value = float("inf")
        action_select = None

        for action in actions(board):
            maxValueResult = maxValue(result(board, action))

            if maxValueResult < value:
                value = maxValueResult
                action_select = action

    return action_select
    #raise NotImplementedError

def maxValue(board):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        v = max(v,minValue(result(board, action)))
    return v


def minValue(board):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v,maxValue(result(board, action)))
    return v