# from connect4 import is_winning_move, player_type, is_board_full, get_possible_moves, insert_disk, remove_disk, ROW_NUM, COL_NUM
from sys import maxsize
from util import *

WIN_SIZE = 5

# maxmin: MIN: -1, MAX: 1
def minmax(board, depth, maxmin, alpha, beta):
    if is_winning_move(board, player_type["bot"]):
        return 100000 + depth
    elif is_winning_move(board, player_type["player"]):
        return -100000 - depth
    elif is_board_full(board):
        return 0
    elif depth == 0:
        return eval_board(board, player_type["bot"])

    # MAX
    if (maxmin == 1):
        bestScore = -maxsize
        for col in get_possible_moves(board):
            insert_disk(board, player_type["bot"], col)
            score = minmax(board, depth-1, -1, alpha, beta)
            remove_disk(board, player_type["bot"], col)
            if score > bestScore:
                bestScore = score

            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return bestScore

    # MIN
    else:
        bestScore = maxsize
        for col in get_possible_moves(board):
            insert_disk(board, player_type["player"], col)
            score = minmax(board, depth-1, 1, alpha, beta)
            remove_disk(board, player_type["player"], col)
            if (score < bestScore):
                bestScore = score

            beta = min(beta, score)
            if beta <= alpha:
                break

        return bestScore



# Gledamo okno velikosti 5:
    # 3R + 2 prazna - 300
    # 3R + 1 prazen + 1B - 150
    # 2R + 3 prazni - 120
    # 2R + 2 prazna + 1B - 100
def eval_horizontal(board, color):
    score = 0
    for row in range(ROW_NUM):
        for col in range(COL_NUM-4):
            window = board[row][col:col+WIN_SIZE]
            color_count = window.count(color)
            empty_count = window.count(' ')

            consecutive_count = count_consecutive(window, color)

            if color_count == 3:
                if empty_count == 2:
                    score += consecutive_count + 300
                elif empty_count == 1:
                    score += consecutive_count + 150
            elif color_count == 2:
                if empty_count == 3:
                    score += consecutive_count + 120
                elif empty_count == 2:
                    score += consecutive_count + 100
    return score

# Okno velikosti 4
def eval_vertical(board, color):
    score = 0
    opponent = player_type["bot"]
    if color == opponent:
      opponent = player_type["player"]
        
    for col in range(COL_NUM):
      for row in range(ROW_NUM):
          # We look only at the upper most pieces
          if board[row][col] != ' ':
              end_index = row+WIN_SIZE if row < ROW_NUM-3 else ROW_NUM
              window = [row[col] for row in board[row:end_index]]

              piece = board[row][col]
              piece_count = 0 #consecutive count
              # Count consecutive pieces of the same color on the top
              for i in range(len(window)):
                  if window[i] == piece:
                      piece_count += 1
                  else:
                      break
              
              # If pieces are the right color - add score
              if board[row][col] == color:
                  score += piece_count*10
              # Opponent pieces - subtract score
              elif board[row][col] == opponent:
                  score -= piece_count*10
              break

    return score

def eval_right_diag(board, color):
    score = 0
    for row in range(ROW_NUM-4):
        for col in range(4, COL_NUM):
            window = []
            for i in range(WIN_SIZE):
                window.append(board[row+i][col-i])

            color_count = window.count(color)
            empty_count = window.count(' ')
            consecutive_count = count_consecutive(window, color)

            if color_count == 3:
                if empty_count == 2:
                    score += consecutive_count + 300
                elif empty_count == 1:
                    score += consecutive_count + 150
            elif color_count == 2:
                if empty_count == 3:
                    score += consecutive_count + 120
                elif empty_count == 2:
                    score += consecutive_count + 100
    return score

def eval_left_diag(board, color):
    score = 0
    for row in range(ROW_NUM-4):
        for col in range(COL_NUM-4):
            window = []
            for i in range(WIN_SIZE):
                window.append(board[row+i][col+i])
            
            color_count = window.count(color)
            empty_count = window.count(' ')
            consecutive_count = count_consecutive(window, color)

            if color_count == 3:
                if empty_count == 2:
                    score += consecutive_count + 300
                elif empty_count == 1:
                    score += consecutive_count + 150
            elif color_count == 2:
                if empty_count == 3:
                    score += consecutive_count + 120
                elif empty_count == 2:
                    score += consecutive_count + 100
    return score

def eval_board(board, color):
    score = 0
    score += eval_horizontal(board, color)
    score += eval_vertical(board, color)
    score += eval_right_diag(board, color)
    score += eval_left_diag(board, color)
    return score

def count_consecutive(window, color):
    consecutive_count = 0
    curr_count = 0
    # Count consecutive pieces of the same color
    for i in range(WIN_SIZE):
        if window[i] == color:
            curr_count += 1
        else:
            if curr_count > consecutive_count:
                consecutive_count = curr_count
            curr_count = 0

    return consecutive_count