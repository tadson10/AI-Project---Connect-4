from typing import Sequence
import tensorflow as tf
from tensorflow import keras
from keras import models
from keras.layers import Flatten, Dense
from keras.optimizers import Adam
from datetime import datetime
import numpy as np
import random
from game_memory import GameMemory

class SequentialModel:
    def __init__(self,  state_size: int, action_size: int, filepath: str = None) -> None:
        print('AADSDASDASDASDASDASDADIWUHFLIWEFJQLWIFE')
        self.state_size = state_size
        self.action_size = action_size
        if filepath is None:
            self.model: models.Sequential = self.__build_model()
        else:
            print('Importing model')
            self.model: models.Sequential = self.__import_model(filepath)

    def __build_model(self):
        print('Creating model')
        model = models.Sequential()
        model.add(Flatten())
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
    
        model.compile(loss='mse', optimizer=Adam(learning_rate = 0.00001))

        return model
    
    def batch_train(self, game_memory: GameMemory):
        game_memory.shuffle_game_steps()
        for game_step in game_memory.game_states:
            target = game_step.reward
            """ if not game_step.:
                target = gamereward + self.gamma * np.amax(self.model.predict(next_state)[0]) """
            target_f = self.model.predict(game_step.state)
            target_f[0][game_step.action] = target
            self.model.fit(np.array(game_step.state), target_f, epochs=1, verbose=0)


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
        print('Loadin model')
        return models.load_model(filepath)

    def reload_model(self, filepath):
        self.model = models.load_model(filepath)