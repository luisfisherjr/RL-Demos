import math
import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding

def victory_condition_eval(board):
    
    # get unique elements in columns, rows, and diagonals and add them to a list
    
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

        if len(elements) is 1: # if only 1 unique element is in grouping

            if elements[0] != ' ': # if all elements are X or O
                return elements[0] # return winner

    return ' ' # no winner


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
        
        board = self.__state['board'] # get board
        player = self.__state['player'] # get player
        
        if board[row][col] != ' ': # illegal move
            done = True
            reward = -1000
            
        else: # legal move
            board[row][col] = player # place piece on board
            winner = victory_condition_eval(board) # check for victory
            if winner != ' ': # victory achieved if 1 or -1 achieved (self playing tictactoe)
                done = True
                reward = 1000
            else:
                if player == 'X':
                    self.__state['player'] = 'O'
                else:
                    self.__state['player'] = 'X'
                    
        observation = dict(self.__state) # copy of game state
        info = {} # empty info

        return observation, reward, done, info

    def reset(self):
        self.__state = {} # initalize state dictionary
        self.__state['board'] = np.full((3,3), ' ') # 0 is empty spot
        self.__state['player'] = 'X'
        
        initial_observation = dict(self.__state)
        
        return initial_observation

    def render(self, mode='human', close=False):
        for row in self.__state['board']: # for every row
            print(row) # print array
