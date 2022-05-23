from abc import ABCMeta, abstractmethod

from RNN.sequential_model import SequentialModel
import numpy as np
from mcts import MCTS_agent
from minimax import minimax_move
import random

from util import get_possible_moves, opponent_mark

class Player(object):
    def __init__(self, label):
        self.label = label

    @abstractmethod
    def get_move(self, state) -> int:
        """Get the column into which token should be placed based on the current state of the game
        
        Parameters
        ----------
        state: array
            Array that represents the current state of the board
            
        Returns
        -------
        int
            Integer that represents column into which token should be placed    
        """
        pass

class PlayerRNN(Player):

    def __init__(self, label, rnn_filepath: str):
        super().__init__(label)
        self.model = self.__import_model(rnn_filepath)

    def __import_model(self, rnn_filepath):
        return SequentialModel(filepath=rnn_filepath)

    #Override base class method
    def get_move(self, state, mark):
        # epsilon = -1, we do not make random moves as we are not training the network
        return self.model.predict_action(self.__transform_state(state, mark), -1)

    def __transform_state(self, state, mark):
        state = np.array(state).flatten()
        state = np.array([state])
        state = np.where(state == ' ', 0,state)
        state = np.where(state == mark, 1,state)
        state = np.where(state == opponent_mark(mark), 2,state)
        return state.astype(int)

class PlayerMiniMax(Player):
    
    def get_move(self, state, mark):
        return minimax_move(state, mark)


class PlayerMCTS(Player):
    
    def get_move(self, state, mark):
        # print(f"MCTS as {mark}")
        return MCTS_agent(state, mark)


class PlayerRandom(Player):

    def get_move(self, state, mark):
        return random.choice(get_possible_moves(state))