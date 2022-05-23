
ROW_NUM = 6
COL_NUM = 7

player_type = {
    "player1": "O", # Yellow, player
    "player2": "X" # Red, bot
}

def opponent_mark(mark):
        """ The mark indicates which player is active - player 1 or player 2. """
        if mark == player_type["player2"]:
            return player_type["player1"]
        return player_type["player2"]

def is_winning_move(board, color):
    # Check horizontal win
    for row in range(ROW_NUM):
        for col in range(COL_NUM-3):
            if board[row][col] == color and board[row][col+1] == color and board[row][col+2] == color and board[row][col+3] == color:
                return True

    # Check vertical win
    for col in range(COL_NUM):
        for row in range(ROW_NUM-3):
            if board[row][col] == color and board[row+1][col] == color and board[row+2][col] == color and board[row+3][col] == color:
                return True

    # Check right diagonal win /
    for row in range(ROW_NUM-3):
        for col in range(3, COL_NUM):
            if board[row][col] == color and board[row+1][col-1] == color and board[row+2][col-2] == color and board[row+3][col-3] == color:
                return True

    # Check left diagonal win \
    for row in range(ROW_NUM-3):
        for col in range(COL_NUM-3):
            if board[row][col] == color and board[row+1][col+1] == color and board[row+2][col+2] == color and board[row+3][col+3] == color:
                return True
    return False


def is_draw(board):
    for col in range(COL_NUM):
        if (board[0][col] == ' '):
            return False
    return True

def insert_disk(board, color, column):
    isFull, row = column_full(board, column)
    # if not isFull:
    board[row][column] = color

def column_full(board, column):
    for i in range(ROW_NUM-1, -1, -1):
        if board[i][column] == ' ':
            return False, i
    return True, -1




def remove_disk(board, color, column):
    # Remove inserted disk
    for row in range(ROW_NUM):
        if board[row][column] == color:
            board[row][column] = ' '
            return

def is_board_full(board):
    for col in range(COL_NUM):
        if not column_full(board, col):
            return False


def is_winning_move(board, color):
    # Check horizontal win
    for row in range(ROW_NUM):
        for col in range(COL_NUM-3):
            if board[row][col] == color and board[row][col+1] == color and board[row][col+2] == color and board[row][col+3] == color:
                return True

    # Check vertical win
    for col in range(COL_NUM):
        for row in range(ROW_NUM-3):
            if board[row][col] == color and board[row+1][col] == color and board[row+2][col] == color and board[row+3][col] == color:
                return True

    # Check right diagonal win /
    for row in range(ROW_NUM-3):
        for col in range(3, COL_NUM):
            if board[row][col] == color and board[row+1][col-1] == color and board[row+2][col-2] == color and board[row+3][col-3] == color:
                return True

    # Check left diagonal win \
    for row in range(ROW_NUM-3):
        for col in range(COL_NUM-3):
            if board[row][col] == color and board[row+1][col+1] == color and board[row+2][col+2] == color and board[row+3][col+3] == color:
                return True
    return False

def get_possible_moves(board):
    possible_cols = []
    for i in range(COL_NUM):
        is_full, row = column_full(board, i)
        if not is_full:
            possible_cols.append(i)
    return possible_cols

# Return color of winner or None if no winner
def is_winner(board, color1, color2):
    if is_winning_move(board, color1):
        return color1
    elif is_winning_move(board, color2):
        return color2
    else:
        return None