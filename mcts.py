import math
import random
import copy
from operator import attrgetter
from util import *


def opponent_mark(mark):
        """ The mark indicates which player is active - player 1 or player 2. """
        if mark == player_type["bot"]:
            return player_type["player"]
        return player_type["bot"]

def opponent_score(score):
    """ To backpropagate scores on the tree. """
    return 1 - score


def check_finish_and_score(board, mark):
    """ Returns a tuple where the first argument states whether game is finished and second argument returns score if game has finished. """
    if is_winning_move(board, mark):
        return (True, 1)
    if is_draw(board):
        return (True, 0.5)
    else:
        return (False, None)


def ucb_score(node_total_score, node_total_visits, parent_total_visits, Cp=2):
    """ UCB1 calculation. """
    if node_total_visits == 0:
        return math.inf
    return node_total_score / node_total_visits + Cp * math.sqrt(
        2 * math.log(parent_total_visits) / node_total_visits)


class State():
    
    def __init__(self, board, mark, parent=None, is_terminal=False, terminal_score=None, action_taken=None):
        self.board = copy.deepcopy(board)
        self.mark = mark
        self.children = []
        self.parent = parent
        self.node_total_score = 0
        self.node_total_visits = 0
        self.expandable_moves = get_possible_moves(self.board)
        self.is_terminal = is_terminal
        self.terminal_score = terminal_score
        self.action_taken = action_taken


    def is_expandable(self):
        """ Checks if the node has unexplored children. """
        return (not self.is_terminal) and (len(self.expandable_moves) > 0)

    def is_leaf(self):
        return len(self.children) == 0


    def select(self, Cp=2):
        
        children_scores = [ucb_score(child.node_total_score,
                                    child.node_total_visits,
                                    self.node_total_visits,
                                    Cp) for child in self.children]
        max_score = max(children_scores)
        best_child_index = children_scores.index(max_score)

        return self.children[best_child_index]

    def expand(self):
        # sam random izbereš izmed expandable moves in ga simuliraš
        column = random.choice(self.expandable_moves)
        child_board = copy.deepcopy(self.board)
        insert_disk(child_board, self.mark, column)
        is_terminal, terminal_score = check_finish_and_score(child_board, self.mark)

        child = State(child_board, opponent_mark(self.mark), parent=self, 
                    is_terminal=is_terminal, terminal_score=terminal_score, action_taken=column)
        self.children.append(child)

        self.expandable_moves.remove(column)


    def simulate(self):
        if self.is_terminal:
            return self.terminal_score

        """
        Run a random play simulation. Starting state is assumed to be a non-terminal state.
        Returns score of the game for the player with the given mark.
        """
        curr_mark = self.mark
        original_mark = self.mark
        board = copy.deepcopy(self.board)
        column = random.choice(get_possible_moves(board))
        insert_disk(board, curr_mark, column)
        is_finish, score = check_finish_and_score(board, curr_mark)
        while not is_finish:
            curr_mark = opponent_mark(curr_mark)
            column = random.choice(get_possible_moves(board))
            insert_disk(board, curr_mark, column)
            # print_board(board)
            is_finish, score = check_finish_and_score(board, curr_mark)

        if curr_mark == original_mark:
            return score

        return opponent_score(score)
    

    def backpropagate(self, simulation_score):
        """
        Backpropagates score and visit count to parents.
        """
        self.node_total_score += simulation_score
        self.node_total_visits += 1
        if self.parent is not None:
            self.parent.backpropagate(opponent_score(simulation_score))

    def tree_single_run(self):
        """
        A single iteration of the 4 stages of the MCTS algorithm.
        """
        # backpropagation
        if self.is_terminal:
            self.backpropagate(self.terminal_score)
            return
        # expansion and simulation
        if self.is_expandable():
            # if expandable, it means that there are children that have not yet been visited
            # print("expand")
            self.expand()
            # print("simulate")
            simulation_score = self.children[-1].simulate()
            # print("backpropagate")
            self.children[-1].backpropagate(simulation_score)
            return
        
        # selection
        self.select().tree_single_run()



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


# board = [[' ' for x in range(COL_NUM)] for y in range(ROW_NUM)]

# state = State(board, player_type['bot'])
# print_board(board)
# for _ in range(1000):
#     state.tree_single_run()
# next_board = max(state.children, key=attrgetter('node_total_score')).action_taken
# print(next_board)

def MCTS_agent(board):
    state = State(board, player_type['bot'])
    for _ in range(500):
        state.tree_single_run()
    next_move = max(state.children, key=attrgetter('node_total_score')).action_taken

    return next_move