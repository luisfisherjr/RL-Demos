
# coding: utf-8

# In[7]:


import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding


# In[63]:


def victory_condition_eval(board):

    uniques = []
    uniques.append(np.unique(board[0])) # row 1
    uniques.append(np.unique(board[1])) # row 2
    uniques.append(np.unique(board[2])) # row 3
    uniques.append(np.unique(board[:, 0:1])) # column 1
    uniques.append(np.unique(board[:, 1:2])) # column 2
    uniques.append(np.unique(board[:, 2:3])) # column 3
    uniques.append(np.unique(board.diagonal())) # major diag
    uniques.append(np.unique(np.rot90(board).diagonal())) # minor diag

    for elements in uniques:

        if len(elements) is 1: # if all elements are the same

            if elements[0] is not 0: # if all elements are not 0
                return elements[0]

    return 0 # no winner


# In[70]:


class TicTacToeEnv(gym.Env):
    
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = spaces.Discrete(9) # 9 possible moves always including illegal moves
        self.observation_space = spaces.Discrete(math.pow(3, 9)) # possible combinations is 3^9

    def step(self, action):
        
        done = False # set default to not done
        reward = 0 # set default to 0
        
        # actions are [0,1,2,3,4,5,6,7,8]
        row, col = np.int8(action / 3), np.int8(action % 3) # get row and column of move
        
        board = self.state['board'] # get board
        player = self.state['on_move'] # get player X = 1, O = -1
        
        if board[row][col] is not 0: # illegal move
            done = True
            reward = -1000
            
        else: # legal move
            board[row][col] = player # place piece on board
            winner = victory_condition_eval(board) # check for victory
            if winner is not 0: # victory achieved if 1 or -1 achieved (self playing tictactoe)
                done = True
                reward = 1000
            else:
                self.state['on_move'] = -player # turns X to O and O to X

    def reset(self):
        self.state = {} # initalize state dictionary
        self.state['board'] = np.zeros((3,3), dtype=np.int8) # 0 is empty spot
        self.state['on_move'] = 1 # 1 is X -1 is O

    def render(self, mode='human', close=False):
        for row in self.state['board']: # for every row
            print(row) # print array

