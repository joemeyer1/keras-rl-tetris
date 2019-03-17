
from tetris import Tetris

import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym import spaces
from gym.envs.toy_text import discrete
import numpy as np


class TetrisEnv(discrete.DiscreteEnv):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		self.t = Tetris()

		state_num = (self.t.height**self.t.width)*4*4*9*5  # 4x8 board [filled or not], 4*9 active-shape locations, 4 rotation positions, 5 shape types
		action_num = 4 # rotate, left, right, step
		#P = {s : {a : [] for a in range(action_num)} for s in range(state_num)}

		# init_state_dist = []
		# for x in range(4):
		# 	for rot in range(4):
		# 		for shape_type in range(5):
		# 			init_state_dist.append( encode([0, 0, x, rot, shape_type]) )

		# init_state_dist = np.array(init_state_dist)
		#init_state_dist /= init_state_dist.sum()

		#super(TetrisEnv, self).__init__(state_num, action_num, P, init_state_dist)


		self.action_space = spaces.Discrete(4) 

		self.observation_space = spaces.Tuple((spaces.Discrete(self.t.height), spaces.Discrete(self.t.height), spaces.Discrete(self.t.height), spaces.Discrete(self.t.height), spaces.Discrete(9), spaces.Discrete(4), spaces.Discrete(4), spaces.Discrete(5)))
		size = 8
		self.observation_space.shape = np.zeros(size, dtype=int)
		#np.concatenate([np.zeros(2**(4*8), dtype=float), np.zeros(4*9, dtype=float), np.zeros(4, dtype=float), np.zeros(5, dtype=float)]).flatten()

		#spaces.Discrete((2**(4*8))*4*4*9*5) # 4x8 board [filled or not], 4*9 active-shape locations, 4 rotation positions, 5 shape types
	
		# #(np.zeros(2**(4*8)), np.zeros(4*9), np.zeros(4), np.zeros(5))




	def step(self, action):
		og_score = self.t.score
		self.t.take_action(action)
		shape_y, shape_x = t.shape_loc
		# obs = (self.t.ground, shape_y, shape_x, t)
		obs = np.array([top_row(self.t)]+[shape_y, shape_x, shape_rot, shape_type])
		np.concatenate(np.array(self.t.ground), np.array(shape_y), np.array(shape_x), np.array(shape_rot), np.array(shape_type))
		reward = self.t.score - og_score
		done = (self.t.score is 0)
		return obs, reward, done, {}

		
	def reset(self):
		self.t.__init__()
		return 0
		
	def render(self, mode='human', close=False):
		self.t.print_board()

	def seed(self, seed=None):
		self.np_random, seed = seeding.np_random(seed)
		return [seed]


# encode/decode style based on gym's taxi example
def encode(obs, t):
	board, shape_y, shape_x, shape_rot, shape_type = obs
	i = shape_type
	i *= 5
	i += shape_rot
	i *= 4
	i += shape_x
	i *= 4
	i += shape_y
	i *= 9
	i += encode_top_row(board, t)
	return i

def decode(i, t):
	out = []
	out.append(decode_top_row(i % 9, t))
	i = i // 9
	out.append(i % 4)
	i = i // 4
	out.append(i % 4)
	i = i // 4
	out.append(i % 5)
	i = i // 5
	out.append(i)
	out.reverse()
	return out





def top_row(tetris):
	top = []
	for x in range(tetris.width):
		for y in range(tetris.height):
			if tetris.board[y][x]:
				top.append(y)
				break






def encode_top_row(top_row, tetris):
	ret = 0
	for x in range(tetris.width):
		ret += top_row[x]
		ret *= tetris.height

def decode_top_row(top_row, tetris):
	out = []
	for x in range(tetris.width):
		out.append(top_row%tetris.height)
		top_row // tetris.height
	return out













