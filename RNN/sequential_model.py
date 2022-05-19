from typing import Sequence
import tensorflow as tf
from tensorflow import keras
from keras import models
from keras.layers import Flatten, Dense
from keras.optimizers import Adam
from datetime import datetime
import numpy as np
import random
from RNN.game_memory import GameMemory, GameStep

class SequentialModel:
    def __init__(self, gamma = 0.9,  state_size: int = 6*7, action_size: int = 7, filepath: str = None) -> None:
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        if filepath is None:
            self.model: models.Sequential = self.__build_model()
        else:
            print('Importing model')
            self.model: models.Sequential = self.__import_model(filepath)

    def __build_model(self):
        print('Creating model')
        model = models.Sequential()
        model.add(Dense(20, input_dim=self.state_size, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
    
        model.compile(loss='mse', optimizer=Adam(learning_rate = 0.00001))

        return model
    
    def batch_train(self, game_memory: GameMemory):
        game_memory.shuffle_game_steps()
        for game_step in game_memory.game_states:
            target = game_step.reward
            if not game_step.done:
                target = game_step.reward + self.gamma * np.amax(self.model.predict(game_step.next_state)[0])
            target_f = self.model.predict(game_step.state)
            target_f[0][game_step.action] = target
            self.model.fit(game_step.state, target_f, epochs=1, verbose=0)


    def predict_action(self, state, epsilon):
        if np.random.rand() <= epsilon: # Exploration
            return random.choice([c for c in range(self.action_size) if (state[:,c] == 0).any()])
            #when exploring, I allow for "wrong" moves to give the agent a chance 
            #to experience the penalty of choosing full columns
        act_values = self.model.predict(state) # Exploitation
        action = np.argmax(act_values[0]).item()
        return action

    def save_model(self, filepath, overwrite = False):
        self.model.save(filepath, overwrite=overwrite)
    
    def __import_model(self, filepath):
        print('Loading model')
        return models.load_model(filepath)

    def reload_model(self, filepath):
        self.model = models.load_model(filepath)