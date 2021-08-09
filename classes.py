from config import *
import random

def CRP(pos): # Create Rect Pos
	return pos*cell_size+border_size*(pos+1)

class Table(object):
	def __init__(self):
		super(Table, self).__init__()
		self.cells = [[Cell(0, j, i) for j in range(cells_num)] for i in range(cells_num)]
		self = self.random_put(self)
		self.score = 0
		self.already_winned = False
		self.moves = [[[i, j, CRP(j), CRP(i), CRP(j), CRP(i), self.cells[i][j]] for j in range(cells_num)] for i in range(cells_num)]
		f = open('record.txt')
		readed = f.readline()
		self.record = 0
		if readed.isdigit():
			self.record = int(readed)
		f.close()

	def get(self, x, y):
		if x in range(cells_num) and y in range(cells_num):
			return self.cells[y][x]
		return Out_map

	def put(self, x, y, cell):
		self.cells[y][x] = cell
	def pop(self, x, y):
		self.cells[y][x] = Cell(0, x, y)

	def random_put(self, tab):
		if 0 != random.randint(0,3): # 0.25 Шансов что не завспавнится
			nulls = []
			for i in tab.cells:
				for j in i:
					if j.num == 0:
						nulls.append(j)
			if len(nulls) != 0:
				i = random.randint(0, len(nulls)-1)
				self.put(nulls[i].x, nulls[i].y, Cell(random.randint(1,2)*2, nulls[i].x, nulls[i].y))
		return tab

	def move(self, orien, tab):
		a = 1 if '-' in orien else -1
		for i in range(cells_num)[::a]:
			for j in range(cells_num)[::a]:
				cell = self.cells[i][j] if 'y' in orien else self.cells[j][i]
				tab = cell.move(orien, tab, (cell.x, cell.y))
		tab = self.random_put(tab)
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
			self.CELL_COLOR = WHITE
		self.x = x
		self.y = y

	def plus(self, tab):
		self.num *= 2
		tab.score += self.num
		if tab.score > tab.record:
			tab.record = tab.score
			f = open('record.txt', 'w')
			f.write(str(tab.record))
			f.close()
		if self.num in BG_COLOR:
			self.BG_COLOR = BG_COLOR[self.num]
			self.CELL_COLOR = CELL_COLOR[self.num]
		else:
			self.BG_COLOR = BLACK
			self.BG_COLOR = WHITE
		return tab

	def move(self, orien, tab, old_pos):
		orien_x, orien_y = 0, 0
		if 'x' in orien:  orien_x =   1 if orien == '+x' else -1
		else:             orien_y =   1 if orien == '+y' else -1
		cell = tab.get(self.x+orien_x, self.y+orien_y)
		if cell.num == 0:
			tab.pop(self.x, self.y)
			self.x += orien_x
			self.y += orien_y
			tab.put(self.x, self.y, self)
			tab = self.move(orien, tab, old_pos)
			tab.moves[old_pos[1]][old_pos[0]] = [
				self.x,
				self.y,
				CRP(self.x),
				CRP(self.y),
				CRP(old_pos[0]),
				CRP(old_pos[1]),
				self] #, tab.moves[old_pos[1]][old_pos[0]][2]

		elif cell.num == self.num:
			tab.pop(self.x, self.y)
			tab = tab.get(cell.x, cell.y).plus(tab)
			tab.moves[old_pos[1]][old_pos[0]] = [
				cell.x,
				cell.y,
				CRP(cell.x),
				CRP(cell.y),
				CRP(old_pos[0]),
				CRP(old_pos[1]),
				cell]

		return tab

	def isCanMove(self, tab):
		a = [0, self.num]
		up    = tab.get(self.x, self.y-1).num in a
		down  = tab.get(self.x, self.y+1).num in a
		left  = tab.get(self.x-1, self.y).num in a
		right = tab.get(self.x+1, self.y).num in a

		if up or down or left or right: return True
		return False

Out_map = Cell(3, 'wr', 'wr')