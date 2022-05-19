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
trainer = env.train([None,'random'])

model = SequentialModel(config['rows']*config['columns'], config['columns'])

TRAINING_GAMES = 20000
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
    epsilon = math.pow(EPSILON_CURVE,i)
    #print(observation)
    while not done:
        #action = agent_random(state, config)
        action = model.predict_action(np.array(state).reshape(6,7).astype(int), epsilon)
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
        
        game_memory.add_game_step(GameStep(np.array(state).reshape(6,7).astype(int), action, np.array(next_state).reshape(6,7).astype(int), reward))
        
        state = next_state

    # Train RNN after the game
    model.batch_train(game_memory)

    # Save model
    if(i % SAVE_INTERVAL == 0):
        model.save_model(f'./RNN/models/{MODEL_FILENAME}', overwrite=True)
        with open("./RNN/log.txt", "a") as file_object:
            # Append 'hello' at the end of file
            file_object.write(f'{str(datetime.now())}: Saved model to {MODEL_FILENAME}\n')
            file_object.write(f'Games played: {i}, agent wins: {agent_wins}, oppoennt wins: {opponent_wins}\n')
            file_object.write(f'epsilon: {epsilon}\n')
            file_object.write(f'=====================================\n')
        print(f'Saving model, games played {i}')
    
    trainer.reset()
    done = False
    i += 1

