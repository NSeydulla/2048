import pygame
from config import sc
from time import time
from random import randint

def CRP(pos): # Create Rect Pos
	return pos*sc.cell_size+(pos+1)*sc.border_size

class GAME():
	def __init__(self, screen):
		#animate params
		self.active = True
		self.isBusy = False
		self.startTime = 0
		self.clock = pygame.time.Clock()
		self.tick = self.clock.tick

		#background
		self.BG = pygame.Surface((sc.w, sc.h))
		self.BG.fill(sc.BG_COLOR)
		for x in range(sc.cells_num):
			for y in range(sc.cells_num):
				pygame.draw.rect(self.BG, sc.CELL_COLOR[0], (CRP(x), CRP(y), sc.cell_size, sc.cell_size))

		#main params
		self.SC = screen
		self.cells = []
		self.spawn()

	def onKeyDown(self, key):
		self.isBusy = True
		for _ in range(sc.cells_num-1):
			moved = False
			print('MOVE WAVE')
			for cell in self.cells[::-1 if key>=2 else 1]:
				moved = cell.move(key) or moved
			self.sort()
			if not moved: break
		self.startTime=time()
		self.spawn()

	def draw(self):
		self.SC.blit(self.BG, (0,0))
		self.animate()
		for i, cell in enumerate(self.cells):
			cell.draw()
			if cell.destroy:
				print(cell, 'destroyed')
				self.cells = self.cells[0:i]+self.cells[i+1:sc.cells_num**2]
		pygame.display.update()

	def animate(self):
		t = time()-self.startTime
		animated = False
		dt = t/sc.animate_time
		for cell in self.cells:
			animated = cell.animate(dt) or animated
		self.isBusy = animated

	def spawn(self):
		for _ in range(2):
			x, y = randint(0,sc.cells_num-1), randint(0,sc.cells_num-1)
			if self.getCell(x, y) is None:
				self.cells.append(Cell(self, 2, x, y))
				if randint(0,3)==0:self.cells[-1].double()
		self.sort()

	def sort(self):
		self.cells.sort(key=lambda cell: cell.y*sc.cells_num+cell.x)

	def getCell(self,x,y):
		for i in range(min(y*sc.cells_num+x, len(self.cells)-1), -1, -1):
			cell = self.cells[i]
			cx = cell.x
			cy = cell.y
			if cx==x and cy==y: return i
			if cy<y: return

class Cell(object):
	def __init__(self, GAME, val, x, y):
		self.x, self.y = x, y #target x, y
		self.lx, self.ly = x, y #last x, y
		self.sx, self.sy = CRP(x), CRP(y) #surface x, y
		self.GAME = GAME
		self.val = val
		self.destroy = False

	def move(self, key):
		x, y = self.x, self.y
		if key in [1,3]: y += (key-2)
		elif key in [0,2]: x += (key-1)
		if not (0<=x<sc.cells_num and 0<=y<sc.cells_num): return False

		CID = self.GAME.getCell(x,y)
		if CID is not None:
			cell = self.GAME.cells[CID]
			if cell.val != self.val: return False
			cell.double()
			print(f'{cell.x}, {cell.y} doubled. {self.x}, {self.y} destroyed.')
			self.destroy = True
		print(f'moved {self.lx}, {self.ly} to {x}, {y}')
		self.x, self.y = x, y
		return True

	def animate(self, dt):
		axis = 0 if self.lx!=self.x else 1
		SAx = [CRP(self.lx), CRP(self.ly)][axis] # surf axis
		TAx = [CRP(self.x ), CRP(self.y )][axis] # target axis

		dxy = sc.animate_xy*dt

		if SAx<TAx: SAx = min(SAx+dxy, TAx)
		else: SAx = max(SAx-dxy, TAx)

		if axis == 0: self.sx = SAx
		else: self.sy = SAx

		if SAx==TAx:
			self.lx=self.x
			self.ly=self.y
			return False
		return True

	def double(self, val=None):
		if val is None: val = self.val*2
		self.val = val

	def draw(self):
		self.GAME.SC.blit(sc.SURFACES.get(self.val, sc.SURFACES[0]), (self.sx, self.sy))