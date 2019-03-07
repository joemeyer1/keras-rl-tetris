
# code by Joe Meyer




import numpy as np
import random

# to take (optional) width as sys arg
import sys


class Tetris:

	# tetris shape-type map
	TYPE_MAP = {	0 : "line",
					1 : "square",
					2 : "T",
					3 : "bkwd_L",
					4 : "fwd_L",}




	# make board + a shape
	def __init__(self, width = 4):

		assert width>3, "width must be > 3"

		random.seed()
		self.width = width
		self.height = width*2
		self.make_ground()
		self.new_shape()
		self.score = 0

		self.ACTION_MAP = {	'a': self.left,
						'd': self.right,
						'w': self.rotate,
						's': self.step,
						'p': self.print_board}


	# USER FUNCTIONS:

	def print_board(self):
		print(self.full_board())


	# moves time fwd 1 step
	def step(self):
		# reward for staying alive
		self.score += 1
		if self.bottom_reached():
			self.update_ground()
			removed_rows = self.check_lines()
			if self.check_death(removed_rows):
				print ("GAME OVER")
				print ("Score: ", self.score)
				return self.__init__(self.width)
			self.new_shape()
		else:
			# move shape down 1
			self.shape_loc[0] += 1
		self.print_board()

	def take_action(self, action):
		self.ACTION_MAP[action]()
		self.step()



	# rotates active shape
	def rotate(self):
		# rotate shape
		self.shape_position = (self.shape_position + 1) % 4
		# check if rotation is valid ...
		for (y,x) in self.active_squares():
			# ... if rotation invalid undo rotation
			if (not 0 <= x < self.width) or (y >= 0 and self.ground[y][x]):
				self.shape_position = (self.shape_position - 1) % 4
				break
		self.print_board()

	# moves shape left 1
	def left(self):
		self.move('left')

	# moves shape right 1
	def right(self):
		self.move('right')




	# HELPER FUNCTIONS:

	# helper for left/right
	# moves shape if legal
	def move(self, direction):
		if direction is 'left':
			direction_offset = -1
			edge = 0
		elif direction is 'right':
			direction_offset = 1
			edge = self.width-1
		else:
			print("direction must be 'left' or 'right'")
			raise Exception("direction '{}' not recognized".format(direction))

		can_move = True
		for (y,x) in self.active_squares():
			if x == edge or (y >= 0 and self.ground[y][x + direction_offset]):
				can_move = False
				break
		if can_move:
			self.shape_loc[1] += direction_offset
		self.print_board()

	# returns ground+active_squares
	def full_board(self):
		board = self.ground.copy()
		for (y, x) in self.active_squares():
			if y >= 0:
				board[y][x] = 1
		return board

	# creates new active shape
	def new_shape(self, shape_type=None):
		if not shape_type:
			# leaving this in fn argument yields repetetive results
			shape_type = random.randint(0,4)
		self.shape_type = shape_type
		shape_width = 3
		if self.TYPE_MAP[self.shape_type] is 'square':
			shape_width = 2
		elif self.TYPE_MAP[self.shape_type] is 'line':
			shape_width = 4

		# shape coordinates (bottom-left corner of shape)
		self.shape_loc = [-1, random.randint(0,self.width-shape_width)]
		# shape rotations
		self.shape_position = random.randint(0,3)


	# returns array of coordinates of active shape
	def active_squares(self):

		left_corner = self.shape_loc
		shape_before_offset = np.array([left_corner]*4)


		if self.TYPE_MAP[self.shape_type] is "line":
			offset = self.line_offset()

		elif self.TYPE_MAP[self.shape_type] is "square":
			offset = self.sq_offset()

		elif self.TYPE_MAP[self.shape_type] is "T":
			offset = self.T_offset()

		elif self.TYPE_MAP[self.shape_type] is "fwd_L":
			offset = self.fwdL_offset()
			
		elif self.TYPE_MAP[self.shape_type] is "bkwd_L":
			offset = self.bkwdL_offset()

		else:
			raise Exception("Shape not recognized.")

		shape = shape_before_offset + offset
		shape_set = {(y,x) for (y,x) in shape}
		return shape_set
		

	# helper for __init__
	# initializes ground
	def make_ground(self):
		# ground[0][0] is top left corner 
		# 1 indiciates sq is part of ground
		self.ground = np.zeros((self.height, self.width), dtype=int)



	# helper for step
	# ->True iff current shape is at bottom
	def bottom_reached(self):
		active_squares = self.active_squares()
		for (y,x) in active_squares:
			if y > -2 and (y+1,x) not in active_squares:
				if (y+1 == self.height) or (self.ground[y+1][x]):
					return True
		return False

	# helper for step
	# removes any full lines/shift top down
	def check_lines(self):
		row = self.height-1
		removed_rows = 0
		while row >= 0:
			while self.row_all_ones(row):
				self.score += 100
				self.remove_row(row, removed_rows)
				removed_rows += 1
			row -= 1
		return removed_rows

	# helper for check_lines
	# ->True iff row all ones
	def row_all_ones(self, row):
		for element in self.ground[row]:
			if not element:
				return False
		return True

	# helper for check_lines
	# removes row, shifts top down
	def remove_row(self, row, removed_rows):

		new_top_row = np.zeros(self.width)
		for square in self.active_squares():
			if square[0]+removed_rows+1 == 0:
				new_top_row[square[1]] = 1
		ground_above_row = [line for line in self.ground[:row] ]
		self.ground[:row+1] = np.array([ new_top_row] + ground_above_row)


	# helper for step
	# ->True iff active-square above board
	def check_death(self, removed_rows):
		for (y, x) in self.active_squares():
			if y + removed_rows < 0:
				return True
		return False

	# helper for step
	# adds active_squares to ground
	def update_ground(self):
		for (y,x) in self.active_squares():
			if y >= 0:
				self.ground[y][x] = 1



	# all below is helpers for active_squares()
	# returns line pattern
	def line_offset(self):
		if self.shape_position % 2:
			# horizontal
			return np.array([	(0,i) for i in range(4)	])
		else:
			# vertical
			return np.array([	(i-3,0) for i in range(4)	])

	# returns sq pattern
	def sq_offset(self):
		return np.array([ (y,x) for y in [-1,0] for x in [0,1]])

	# returns T pattern
	def T_offset(self):
		if self.shape_position is 0:
			return np.array([	(-1,1)] + 
						[(0,i) for i in range(3)	])

		elif self.shape_position is 1:
			return np.array([	(-2,1),
						(-1,0), (-1,1),
								(0, 1)	])

		elif self.shape_position is 2:
			return np.array([	(-1,i) for i in range(3)] +
										[(0,1)	])

		elif self.shape_position is 3:
			return np.array([	(-2,0),
								(-1,0), (-1,1),
								(0, 0)	])

	# returns fwdL pattern
	def fwdL_offset(self):
		if self.shape_position is 0:
			return np.array([	(-1,0)] +
								[[0,i] for i in range(3)])

		elif self.shape_position is 1:
			return np.array([	(-2,1),
								(-1,1),
						 (0,0), (0,1)])

		elif self.shape_position is 2:
			return np.array([	(-1,0), (-1,1), (-1,2),
												(0, 2)	])

		elif self.shape_position is 3:
			return np.array([	(-2,0), (-2,1),
								(-1,0),
								(0, 0)					])

	# returns bkwdL pattern
	def bkwdL_offset(self):
		if self.shape_position is 0:
			return np.array([					(-1,2)] +
								[(0,i) for i in range(3)])

		elif self.shape_position is 1:
			return np.array([	(-2,0), (-2,1),
										(-1,1),
										(0, 1)	])

		elif self.shape_position is 2:
			return np.array([	(-1,0), (-1,1), (-1,2),
								(0, 0) ])

		elif self.shape_position is 3:
			return np.array([	(-2,0),
								(-1,0),
								(0, 0), (0,1)	])


	# SHORTCUTS

	def a(self):
		self.left()

	def d(self):
		self.right()

	def w(self):
		self.rotate()

	def s(self):
		self.step()

	def p(self):
		self.print_board()






