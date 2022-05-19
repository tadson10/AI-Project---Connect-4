import random
from typing import Sequence
import numpy as np

class GameStep:
    def __init__(self, state, action, next_state, reward, done) -> None:
        self.state = state
        self.action = action
        self.next_state = next_state
        self.reward = reward
        self.done = done
    
    def __str__(self) -> str:
        s: str = "---------------------\n"
        s += "Start state:\n"
        s += f'{str(np.array(self.state).reshape(6,7))}\n'
        s += f'Action: {self.action}\n'
        s += f'End state: \n'
        s += f'{str(np.array(self.next_state).reshape(6,7))}\n'
        s += f'Reward: {self.reward}\n'
        s += f'---------------------\n'
        return s

class GameMemory:
    def __init__(self) -> None:
        self.game_states: Sequence[GameStep] = []

    def add_game_step(self, game_state: GameStep):
        self.game_states.append(game_state)

    def shuffle_game_steps(self):
        random.shuffle(self.game_states)
