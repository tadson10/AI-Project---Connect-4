from datetime import datetime
from kaggle_environments import make, evaluate, utils
import random
import numpy as np
import sys
from game_memory import GameMemory, GameStep
sys.path.insert(0, '/home/anze/faks/ui/AI-Project---Connect-4/')
from util import is_winner
from RNN.sequential_model import SequentialModel
import math

config = {'rows': 6, 'columns': 7, 'inarow': 4}
env = make("connectx", debug=True, configuration=config)
trainer = env.train([None,'negamax'])
print(list(env.agents))

model = SequentialModel(state_size=config['rows']*config['columns'], action_size=config['columns'])

TRAINING_GAMES = 1
EPSILON_CURVE = 0.9996546719
SAVE_INTERVAL = 500
MODEL_FILENAME = '2.h5'

i = 1
agent_wins = 0
opponent_wins = 0

# Clear logs
with open("./RNN/log.txt", 'r+') as file_object:
    file_object.truncate(0)

while(i <= TRAINING_GAMES):
    done = False
    game_memory = GameMemory()
    state = trainer.reset()['board']
    #print(observation)
    while not done:
        #action = agent_random(state, config)
        print("state")
        print(np.array([state]).astype(int))
        action = model.predict_action(np.array([state]).astype(int), -1)


        print("action", action)
        next_state, dummy, overflow, info = trainer.step(action)
        next_state = next_state['board']
        winner = is_winner(np.array(next_state).reshape(6,7), 1, 2)
        reward = 0
        if winner != None and winner == 2:
            # Oponent wins
            print("Oponnent wins")
            opponent_wins += 1
            reward = -1
            done = True
        elif winner != None and winner == 1:
            # Agent wins
            print("Agent wins")
            reward = 1
            agent_wins += 1
            done = True
        elif overflow and winner == None:
            # Inavlid move
            print("Invalid move")
            reward = -10
            done = True
        elif not overflow and winner == None:
            reward = 0
        
        
        state = next_state

    
    trainer.reset()
    done = False
    i += 1

