import tensorflow as tf
from tensorflow import keras
from keras import models
from keras.layers import Flatten, Dense

class NeuralNetwork:
    def __init__(self) -> None:
        self.model = self.__build_model()

    def __build_model(self):
        model = models.Sequential()
    
        model.add(Flatten())
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
    
        model.add(Dense(7))

        return model

    def __compute_loss(logits, actions, rewards): 
        neg_logprob = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=actions)
        loss = tf.reduce_mean(neg_logprob * rewards)
        return loss
    
    def train_step(self, optimizer, observations, actions, rewards):
        with tf.GradientTape() as tape:
        # Forward propagate through the agent network
            
            logits = self.model(observations)
            loss = self.__compute_loss(logits, actions, rewards)
            grads = tape.gradient(loss, self.model.trainable_variables)
            
            optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
