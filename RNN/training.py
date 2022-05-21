from datetime import datetime
import random
from kaggle_environments import make
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

model = SequentialModel(state_size=config['rows']*config['columns'], action_size=config['columns'], filepath='./RNN/models/5.h5')

TRAINING_GAMES = 20000
EPSILON_CURVE = 0.999769768
SAVE_INTERVAL = 500
MODEL_FILENAME = '5.h5'

i = 1
agent_wins = 0
opponent_wins = 0

action_hist = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0
}

# Clear logs
with open("./RNN/log1.txt", 'r+') as file_object:
    file_object.truncate(0)

while(i <= TRAINING_GAMES):
    done = False
    game_memory = GameMemory()
    state = trainer.reset()['board']
    #epsilon = math.pow(EPSILON_CURVE,i)
    epsilon = 0.01
    #print(observation)
    while not done:
        #action = agent_random(state, config)
        action = model.predict_action(np.array([state]).astype(int), epsilon)
        action_hist[action] += 1
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
        
        game_memory.add_game_step(GameStep(np.array([state]).astype(int), action, np.array([next_state]).astype(int), reward, done))
        
        state = next_state

    # Train RNN after the game
    model.batch_train(game_memory)

    # Save model
    if(i % SAVE_INTERVAL == 0):
        model.save_model(f'./RNN/models/{MODEL_FILENAME}', overwrite=True)
        with open("./RNN/log1.txt", "a") as file_object:
            file_object.write(f'{str(datetime.now())}: Saved model to {MODEL_FILENAME}\n')
            file_object.write(f'Games played: {i}, agent wins: {agent_wins}, oppoennt wins: {opponent_wins}\n')
            file_object.write(f'epsilon: {epsilon}\n')
            file_object.write(f'=====================================\n')
        print(f'Saving model, games played {i}')
    
    trainer.reset()
    done = False
    i += 1

with open("./RNN/log1.txt", "a") as file_object:
    file_object.write(f'0: {action_hist[0]}, 1: {action_hist[1]}, 2: {action_hist[2]}, 3: {action_hist[3]}, 4: {action_hist[4]}, 5: {action_hist[5]}, 6: {action_hist[6]}')
