from contextlib import redirect_stdout
import random
from sys import maxsize
from attr import field
import minimax
import pygame
import random
import math
import sys
import pygame_menu
from util import *


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

field_size = 100

board = [[' ' for x in range(COL_NUM)] for y in range(ROW_NUM)]
algorithm = "Minimax"


# algorithms = {"Minimax": minimax.minmax(board, 2, -1, -maxsize, maxsize), "MCTS": print("Not implemented")}


def print_board(board):
    for i in range(ROW_NUM):
        for j in range(ROW_NUM):
            print(board[i][j] + '|', end="")
        print(board[i][ROW_NUM])
        if i < ROW_NUM-1:
            print('-+-+-+-+-+-+-')
        else:
            print('-------------')
    print("\n")
print_board(board)


def player_move(board):
    print("PLAYER")
    print_board(board)
    column = int(input("Enter the row for 'O':  "))
    insert_disk(board, player_type["player"], column)
    return


def bot_move(board):
    scores = []
    best_score = -maxsize
    best_column = -1
    for col in get_possible_moves(board):
        insert_disk(board, player_type["bot"], col)
        score = 0
        if algorithm == "Minimax":
            score = minimax.minmax(board, 4, -1, -maxsize, maxsize)
        elif algorithm == "MCTS":
            print("Not implemented")
            exit()
        remove_disk(board, player_type["bot"], col)
        print(col, score)
        if (score >= best_score):
            scores.append((score, col))
            best_score = score
            best_column = col

    # If there are more possible moves with the same max score - pick random
    max_cols = []
    for score, col in scores:
        if score == best_score:
            max_cols.append(col)

    best_column = random.choice(max_cols)
    print(best_score, best_column)
    insert_disk(board, player_type["bot"], best_column)
    return


def draw_board(board, screen):
    pygame.draw.rect(screen, BLACK, (0, 0, COL_NUM*field_size, field_size))
    for row in range(ROW_NUM):  # ROW_NUM
        for col in range(COL_NUM):  # COL_NUM
            # (surface, color, (left, top, width, height))
            pygame.draw.rect(screen, BLUE, (col*field_size,
                             row*field_size+field_size, field_size, field_size))
            if board[row][col] == player_type["bot"]:
                # (surface, color, center (x,y), radius)
                pygame.draw.circle(
                    screen, RED, (col*field_size+field_size/2, row*field_size+field_size+field_size/2), 40)
            elif board[row][col] == player_type["player"]:
                # (surface, color, center (x,y), radius)
                pygame.draw.circle(
                    screen, YELLOW, (col*field_size+field_size/2, row*field_size+field_size+field_size/2), 40)
            else:
                # (surface, color, center (x,y), radius)
                pygame.draw.circle(
                    screen, WHITE, (col*field_size+field_size/2, row*field_size+field_size+field_size/2), 40)

    pygame.display.update()


def game_over_screen(winner, font, screen):
    pygame.time.wait(3000)
    text = font.render(winner + " wins!", True, WHITE)
    for row in range(ROW_NUM+1):  # ROW_NUM
        for col in range(COL_NUM):  # COL_NUM
            # (surface, color, (left, top, width, height))
            pygame.draw.rect(screen, BLACK, (col*field_size,
                             row*field_size, field_size, field_size))

    text_rect = text.get_rect()
    text_x = screen.get_width() / 2 - text_rect.width / 2
    text_y = screen.get_height() / 2 - text_rect.height / 2
    screen.blit(text, [text_x, text_y])


def play_game(board, clock, screen, font):
    play = True
    draw_board(board, screen)
    pygame.display.update()
    turn = random.choice([-1, 1])  # -1 player, 1 AI
    print(turn)
    while play:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                # Draws over yellow piece, so there is always just one yellow piece
                pygame.draw.rect(
                    screen, BLACK, (0, 0, COL_NUM*field_size, field_size))
                col = math.floor(event.pos[0]/field_size)
                # print((col*field_size+field_size/2, field_size/2))
                if turn == -1:
                    # (surface, color, center (x,y), radius)
                    pygame.draw.circle(
                        screen, YELLOW, (col*field_size+field_size/2, field_size/2), 40)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == -1:
                    col = math.floor(event.pos[0]/field_size)
                    isFull, row = column_full(board, col)
                    if not isFull:
                        insert_disk(board, player_type["player"], col)
                        draw_board(board, screen)
                        pygame.draw.rect(
                            screen, BLACK, (0, 0, COL_NUM*field_size, field_size))
                        turn *= -1

                        if is_winning_move(board, player_type["player"]):
                            game_over_screen("Player", font, screen)
                            turn = 0

        if turn == 1:
            bot_move(board)
            draw_board(board, screen)
            turn *= -1
            if is_winning_move(board, player_type["bot"]):
                game_over_screen("AI (Minimax)", font, screen)
                turn = 0

        if is_draw(board):
            game_over_screen("Tie", font, screen)

        clock.tick(60)


def set_ai_algorithm(value, index):
    # Do the job here !
    print(value, index)
    global algorithm
    algorithm = value[0][0]
    print(algorithm)
    pass


def start_the_game(args):
    # Do the job here !
    board = args[0]
    clock = args[1]
    screen = args[2]
    font = args[3]
    play_game(board, clock, screen, font)
    pass


def init_game(board):
    pygame.init()
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    size = (COL_NUM*field_size, (ROW_NUM+1)*field_size)
    screen = pygame.display.set_mode(size)

    menu = pygame_menu.Menu('Welcome', COL_NUM*field_size, (ROW_NUM+1)*field_size,
                            theme=pygame_menu.themes.THEME_BLUE)

    menu.add.selector('AI algorithm:', [
        ('Minimax', 1), ('MCTS', 2)], onchange=set_ai_algorithm)
    menu.add.button('Play', start_the_game, [board, clock, screen, font])
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)

init_game(board)

# while True:  # not is_winning_move():
#     bot_move(board)
#     player_move(board)
# print(get_possible_moves(board))
