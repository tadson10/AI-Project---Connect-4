from abc import ABCMeta, abstractmethod

from RNN.sequential_model import SequentialModel
import numpy as np
from minimax import minimax_move

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
    def get_move(self, state):
        # epsilon = -1, we do not make random moves as we are not training the network
        return self.model.predict_action(self.__transform_state(state), -1)

    def __transform_state(self, state):
        state = np.array(state).flatten()
        state = np.array([state])
        state = np.where(state == ' ', 0,state)
        state = np.where(state == 'O', 2,state)
        state = np.where(state == 'X', 1,state)
        return state.astype(int)

class PlayerMiniMax(Player):
    
    def get_move(self, state):
        return minimax_move(state)
