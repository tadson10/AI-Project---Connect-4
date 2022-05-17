from kaggle_environments import make, evaluate, utils
import random
import numpy as np
import sys
sys.path.insert(0, '/home/anze/faks/ui/AI-Project---Connect-4/')
from util import is_winner
from RNN.sequential_model import SequentialModel


def agent_random(obs, config):
    valid_moves = [col for col in range(config['columns']) if obs[col] == 0]
    return random.choice(valid_moves)

config = {'rows': 6, 'columns': 7, 'inarow': 4}
env = make("connectx", debug=True, configuration=config)


model = SequentialModel(config['rows']*config['columns'], config['columns'])

iters = 0
trainer = env.train([None,'random'])

while(iters < 10):
    done = False    
    state = trainer.reset()['board']
    #print(observation)
    i = 0
    while not done:
        action = agent_random(state, config)
        action = 1
        next_state, dummy, overflow, info = trainer.step(action)
        next_state = next_state['board']
        winner = is_winner(np.array(next_state).reshape(6,7), 1, 2)
        reward = 0
        if winner != None and winner == 2:
            # Oponent wins
            print("Oponnent wins")
            reward = -1
        elif winner != None and winner == 1:
            # Agent wins
            print("Agent wins")
            reward = 1
        elif overflow and winner == None:
            # Inavlid move
            print(overflow)
            print(np.array(state).reshape(6,7))
            print(action)
            print(np.array(next_state).reshape(6,7))
            reward = -10
        
        state = next_state
    
    trainer.reset()
    iters += 1

