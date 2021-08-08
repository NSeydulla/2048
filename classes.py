from config import *
import random

class Table(object):
	def __init__(self):
		super(Table, self).__init__()
		self.cells = [[Cell(0, i, j) for j in range(cells_num)] for i in range(cells_num)]
		self.random_put()
		self.score = 0

	def get(self, x, y):
		if x in range(cells_num) and y in range(cells_num):
			return self.cells[y][x]
		return Out_map

	def put(self, x, y, cell):
		self.cells[y][x] = cell
	def pop(self, x, y):
		self.cells[y][x] = Cell(0, x, y)

	def random_put(self, min_cells=0, max_cells=3, trying=True):
		for i in range(random.randint(0,3)):
			x = random.randint(0,cells_num-1)
			y = random.randint(0,cells_num-1)
			new_cell = Cell(random.randint(1,2)*2, x, y)
			cell = self.get(x,y)
			if cell.num == 0:
				self.put(x,y, new_cell)
			else:
				if trying:
					self.random_put(1,1,False)

	def move(self, orien, tab):
		a = 1 if '-' in orien else -1
		for i in range(cells_num)[::a]:
			for j in range(cells_num)[::a]:
				cell = self.cells[i][j] if 'y' in orien else self.cells[j][i]
				tab = cell.move(orien, tab)
		self.random_put()
		return tab

class Cell(object):
	def __init__(self, num, x, y):
		super(Cell, self).__init__()
		self.num = num
		if num in BG_COLOR:
			self.BG_COLOR = BG_COLOR[num]
			self.CELL_COLOR = CELL_COLOR[num]
		else:
			self.BG_COLOR = BLACK
			self.BG_COLOR = WHITE
		self.x = x
		self.y = y

	def transformation(self, tab):
		self.num *= 2
		tab.score += self.num
		if self.num in BG_COLOR:
			self.BG_COLOR = BG_COLOR[self.num]
			self.CELL_COLOR = CELL_COLOR[self.num]
		else:
			self.BG_COLOR = BLACK
			self.BG_COLOR = WHITE
		return tab

	def move(self, orien, tab):
		orien_x, orien_y = 0, 0
		if 'x' in orien:  orien_x =   1 if orien == '+x' else -1
		else:             orien_y =   1 if orien == '+y' else -1
		cell = tab.get(self.x+orien_x, self.y+orien_y)
		if cell.num == 0:
			tab.pop(self.x, self.y)
			self.x += orien_x
			self.y += orien_y
			tab.put(self.x, self.y, self)
			self.move(orien, tab)
		elif cell.num == self.num:
			tab.pop(self.x, self.y)
			tab = tab.get(self.x+orien_x, self.y+orien_y).transformation(tab)
		return tab

	def isCanMove(self, tab):
		a = [0, self.num]
		up   =  tab.get(self.x, self.y-1).num
		down =  tab.get(self.x, self.y+1).num
		left =  tab.get(self.x-1, self.y).num
		right = tab.get(self.x+1, self.y).num

		if (up   in a or
			down in a or
			left in a or
			right in a):
			return True
		return False



class Out_map(object):
	def __init__(self):
		super(Out_map, self).__init__()
		self.num = 3
		self.x = 'wr'
		self.y = 'wr'

Out_map = Out_map()