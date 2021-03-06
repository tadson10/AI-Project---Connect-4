from contextlib import redirect_stdout
import random
from sys import maxsize

from scipy import rand
import minimax
import os
import pygame
import random
import itertools
import math
import sys
import pygame_menu
from player import PlayerMiniMax, PlayerRNN, PlayerMCTS, PlayerRandom
from util import *


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

field_size = 100

board = [[' ' for x in range(COL_NUM)] for y in range(ROW_NUM)]
algorithm = "Minimax"
ai_player = PlayerMiniMax("Minimax")

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
    insert_disk(board, player_type["player1"], column)
    return


def draw_board(board, screen):
    pygame.draw.rect(screen, BLACK, (0, 0, COL_NUM*field_size, field_size))
    for row in range(ROW_NUM):  # ROW_NUM
        for col in range(COL_NUM):  # COL_NUM
            # (surface, color, (left, top, width, height))
            pygame.draw.rect(screen, BLUE, (col*field_size,
                             row*field_size+field_size, field_size, field_size))
            if board[row][col] == player_type["player2"]:
                # (surface, color, center (x,y), radius)
                pygame.draw.circle(
                    screen, RED, (col*field_size+field_size/2, row*field_size+field_size+field_size/2), 40)
            elif board[row][col] == player_type["player1"]:
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
                        insert_disk(board, player_type["player1"], col)
                        draw_board(board, screen)
                        pygame.draw.rect(
                            screen, BLACK, (0, 0, COL_NUM*field_size, field_size))
                        turn *= -1

                        if is_winning_move(board, player_type["player1"]):
                            game_over_screen("Player", font, screen)
                            turn = 0

        if turn == 1:
            insert_disk(board, player_type["player2"], ai_player.get_move(board, player_type["player2"]))
            draw_board(board, screen)
            turn *= -1
            if is_winning_move(board, player_type["player2"]):
                game_over_screen("AI (Minimax)", font, screen)
                turn = 0

        if is_draw(board):
            game_over_screen("Tie", font, screen)

        clock.tick(60)


def set_ai_algorithm(value, index):
    global algorithm
    algorithm = value[0][0]

    global ai_player
    if algorithm == "Minimax":
        ai_player = PlayerMiniMax("Minimax")
    elif algorithm ==  "Neural network":
        ai_player = PlayerRNN('Neural network', './RNN/models/4.h5')
    elif algorithm == "MCTS":
        ai_player = PlayerMCTS("MCTS")


def start_the_game(args):
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
        ('Minimax', 1), ('MCTS', 2), ('Neural network', 3)], onchange=set_ai_algorithm)
    menu.add.button('Play', start_the_game, [board, clock, screen, font])
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)

# init_game(board)

# while True:  # not is_winning_move():
#     bot_move(board)
#     player_move(board)
# print(get_possible_moves(board))

def play_ai_game(ai1, ai2):
    board = [[' ' for x in range(COL_NUM)] for y in range(ROW_NUM)]
    play = True
    turn = random.choice([-1, 1])

    while play:
        if turn == -1:
            insert_disk(board, player_type["player1"], ai1.get_move(board, player_type["player1"]))
        
        elif turn == 1:
            insert_disk(board, player_type["player2"], ai2.get_move(board, player_type["player2"]))

        turn *= -1

        if is_winning_move(board, player_type["player1"]):
            turn = 0
            return 0

        if is_winning_move(board, player_type["player2"]):
            turn = 0
            return 2

        if is_draw(board):
            turn = 0
            return 1

def ai_competition(iters):

    # Disable
    def blockPrint():
        sys.stdout = open(os.devnull, 'w')

    # Restore
    def enablePrint():
        sys.stdout = sys.__stdout__


    minimax_player = PlayerMiniMax("Minimax")
    RNN_player = PlayerRNN('Neural network', './RNN/models/4.h5')
    MCTS_player  = PlayerMCTS("MCTS")
    random_player = PlayerRandom("Random")

    ai_pairs = itertools.combinations([minimax_player, RNN_player, MCTS_player, random_player], 2)
    for ai1, ai2 in ai_pairs:
        print()
        print(f"*****{ai1.label} vs {ai2.label}*****")
        res = [0, 0, 0]
        for i in range(iters):
            blockPrint()
            res[play_ai_game(ai1, ai2)] += 1
            enablePrint()
            print(f"Game {i+1} finished!")
        print(res)

ai_competition(10)
