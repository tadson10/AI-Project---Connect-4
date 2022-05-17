import tensorflow as tf
from tensorflow import keras
from keras import models
from keras.layers import Flatten, Dense
from keras.optimizers import Adam
from datetime import datetime
import numpy as np
import random

class SequentialModel:
    def __init__(self,  state_size: int, action_size: int, filepath: str = None) -> None:
        self.state_size = state_size
        self.action_size = action_size
        if filepath is None:
            self.model: models.Sequential = self.__build_model()
        else:
            self.model: models.Sequential = self.__import_model(filepath)

    def __build_model(self):
        model = models.Sequential()
        model.add(Flatten())
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
    
        model.compile(loss='mse', optimizer=Adam(learning_rate = 0.00001))

        return model
    
    def train_model(self, observations, actions, rewards):
        self.model.fit()


    def predict_action(self, state, epsilon):
        if np.random.rand() <= epsilon: # Exploration
            return random.choice([c for c in range(self.action_size) if state[:,c] == 0])
            #when exploring, I allow for "wrong" moves to give the agent a chance 
            #to experience the penalty of choosing full columns
        act_values = self.model.predict(state) # Exploitation
        action = np.argmax(act_values[0]) 
        return action

    def save_model(self, filepath, overwrite = False):
        self.model.save(filepath, overwrite=overwrite)
    
    def __import_model(self, filepath):
        return models.load_model(filepath)

    def reload_model(self, filepath):
        self.model = models.load_model(filepath)