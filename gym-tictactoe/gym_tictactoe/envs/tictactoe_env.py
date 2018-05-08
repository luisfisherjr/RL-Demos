
# coding: utf-8

# In[1]:


import numpy as np
import random
import gym
from gym import error, spaces, utils
from gym.utils import seeding


# In[2]:


class TicTacToeEnv(gym.Env):
    
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = spaces.Discrete(9) # 9 possible moves always including illegal moves
        self.observation_space = spaces.Discrete(pow(3, 9)) # possible combinations is 3^9

    def step(self, action):
        
        done = False # set default to not done
        reward = 0 # set default to 0
        
        # actions are [0,1,2,3,4,5,6,7,8]
        row_p, col_p = np.int8(action / 3), np.int8(action % 3) # get row and column of move
        
        board = self.__state['board'] # get board
        player = self.__state['player'] # get player
        opponent = self.__state['opponent'] # get opponent
        
        if board[row_p][col_p] != ' ': # illegal move
            done = True
            reward = -1000
            
        else: # legal move
            
            possible_win_move_p = victory_move(board, (row_p, col_p)) # check for victory
            board[row_p][col_p] = player # place piece on board
            
            if player in possible_win_move_p:
                
                done = True
                reward = 1000
            
            elif not get_empty_spaces(board):
                
                done = True
                reward = 0   
            
            else:
                
                row_o, col_o = tictactoe_solver(board, opponent)

                possible_win_move_o = victory_move(board, (row_o, col_o))
                board[row_o][col_o] = opponent
                         
                if opponent in possible_win_move_o:
                    
                    done = True
                    reward = -1000
                    
                elif not get_empty_spaces(board):
                    done = True
                    reward = 0 
                    
        observation = dict(self.__state) # copy of game state
        info = {} # empty info

        return observation, reward, done, info

    def reset(self, player = 'X'):
        self.__state = {} # initalize state dictionary
        self.__state['board'] = np.full((3,3), ' ') # 0 is empty spot
        
        if player == 'X':
        
            self.__state['player'] = 'X'
            self.__state['opponent'] = 'O'
            
        else:
            
            self.__state['player'] = 'O'
            self.__state['opponent'] = 'X'
            
            row, col = tictactoe_solver(self.__state['board'], self.__state['opponent'])
            self.__state['board'][row][col] = self.__state['opponent']       
        
        initial_observation = dict(self.__state)
        
        return initial_observation

    def render(self, mode='human', close=False):
        for row in self.__state['board']: # for every row
            print(row) # print array


# In[3]:


def get_empty_spaces(board):
    
    empty_spaces = []
    for row in range(3):
        for column in range(3):
            if board[row][column] == ' ':
                empty_spaces.append((row, column))
            
    return empty_spaces


# In[4]:


def victory_move(board, possible_move):
    
    victors = []
    
    (row, col) = possible_move
    
    maj_diag = [(0,0), (1,1), (2,2)]
    min_diag = [(0,2), (1,1), (2,0)]
    
    to_check = []
    to_check.append(board[row].tolist())
    to_check.append(board[:, col].tolist())
    
    if possible_move in maj_diag:
        to_check.append(board.diagonal().tolist())
      
    if possible_move in min_diag:
        to_check.append(np.rot90(board).diagonal().tolist()) # minor diag

    for lists in to_check:
        
        if lists.count('X') is 2:
            victors.append('X')  # winner possible from this move
        if lists.count('O') is 2:
            victors.append('O') # winner possible from this move
    
    return victors


# In[5]:


def tictactoe_solver(board, solver):
    
    """
    board: 3x3 np.array of chars ' ', 'X', and 'O'
    solver: 'X' or 'O'
    """
    
    opponent = 'X'
    
    if solver is 'X':
        opponent = 'O'

    win_moves = {'X': [], 'O': []}
    
    possible_moves = get_empty_spaces(board)

    for move in possible_moves:

        winners = victory_move(board, move)
        
        if 'X' in winners:
            win_moves['X'].append(move)

        if 'O' in winners:
            win_moves['O'].append(move)
            
    # try to win if possible
    if win_moves[solver]:
        return random.choice(win_moves[solver])

    # denny win if possible
    if win_moves[opponent]:
        return random.choice(win_moves[opponent])
    
    """
    possible_moves_set = set(possible_moves) 
    corner_moves_set = {(0,0), (0,2), (2,0), (2,2)}
    center_move = (1,1)
    

    # get center if its open
    if center_move in possible_moves_set:
        return center_move
    
    possible_corners = corner_moves_set & possible_moves_set
    
    # get a corner if any are open
    if possible_corners:
        return possible_corners.pop()
    """
    
    # get any possible
    return random.choice(possible_moves)

