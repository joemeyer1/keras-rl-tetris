
from tetris import Tetris

import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym import spaces
from gym.envs.toy_text import discrete


class TetrisExtraHardEnv(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		self.t = Tetris()
		self.action_space = spaces.Discrete(5)

		self.observation_space = spaces.Tuple((
			spaces.Discrete(32),
			spaces.Discrete(4)))
		self.seed()
		#act_space = [k for k in self.t.ACTION_MAP]
		#self.observation_space = (self.t.full_board(), self.t.active_squares())

	def step(self, action):
		og_score = self.t.score
		self.t.take_action(action)
		obs = [move for move in self.t.ACTION_MAP]
		reward = self.t.score - og_score
		done = (self.t.score is 0)
		return obs, reward, done, {}

		
	def reset(self):
		self.t.__init__()
		
	def render(self, mode='human', close=False):
		self.t.print_board()

	def seed(self, seed=None):
		self.np_random, seed = seeding.np_random(seed)
		return [seed]