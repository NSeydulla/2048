import pygame
from config import sc
from time import time, sleep
from random import randint as rint

def CRP(pos): # Create Rect Pos
	return pos*sc.cell_size+(pos+1)*sc.border_size

pygame.font.init()
font = pygame.font.Font(None, int(sc.cell_size*0.8))

def text_speech(sc, text, color, pos):
	rendered_text = font.render(text, True, color)
	sc.blit(rendered_text, rendered_text.get_rect(center=pos))

class Game():
	def __init__(self, screen):
		#animate params
		self.active = True
		self.isBusy = False
		self.lastTime = 0

		#main params
		self.sc = screen
		self.cells = [[Cell(self, 0, x, y) for y in range(sc.cells_num)] for x in range(sc.cells_num)]
		self.spawn()

	def animate(self):
		t = time()-self.lastTime
		if t<sc.animate_time:
			dt = (t/sc.animate_time)
			self.x = self.cells[self.animatingCell].x+self.dx * dt
			self.y = self.cells[self.animatingCell].y+self.dy * dt
			self.cells[self.animatingCell].blit(self.sc, self.x, self.y)
		else:
			self.animatingCell = None
			self.isBusy = False

	def draw(self):
		self.sc.fill(sc.BG_COLOR)
		for row in self.cells:
			for cell in row:
				cell.draw(self.sc)
		pygame.display.update()

	def onKeyDown(self, key):
		for row in self.cells[::-1 if key == 2 else 1]:
			for cell in row[::-1 if key == 3 else 1]:
				if cell.num == 0: continue
				cell.move(key)
		self.spawn()

	def spawn(self):
		for i in range(2):
			x, y = rint(0,sc.cells_num-1), rint(0,sc.cells_num-1)
			if self.cells[x][y].num == 0:
				self.cells[x][y].double()
				if rint(0,3)==0:self.cells[x][y].double()

class Cell(object):
	def __init__(self, Game, num, x, y):
		self.x, self.y = x, y
		self.Game = Game
		self.num = num
		self.CELL_COLOR = sc.CELL_COLOR.get(num, (0,0,0))
		self.TEXT_COLOR = sc.TEXT_COLOR.get(num, (255,255,255))
		self.rect = pygame.Rect(CRP(x), CRP(y), sc.cell_size, sc.cell_size)

	def update(self):
		self.CELL_COLOR = sc.CELL_COLOR.get(self.num, (0,0,0))
		self.TEXT_COLOR = sc.TEXT_COLOR.get(self.num, (255,255,255))

	def set(self, num=0):
		self.num = num
		self.update()

	def double(self, num=2):
		if self.num == 0: self.num=num
		else: self.num *= 2
		self.update()

	def move(self, key):
		xl = [-1,0,1,0]
		yl = [0,-1,0,1]
		x = self.x+xl[key]
		y = self.y+yl[key]
		if (not 0<=x<sc.cells_num) or (not 0<=y<sc.cells_num): return
		if self.Game.cells[x][y].num in [self.num, 0]:
			self.Game.cells[x][y].double(self.num)
			self.set()
			self.Game.cells[x][y].move(key)

	def draw(self, screen):
		pygame.draw.rect(screen, self.CELL_COLOR, self.rect)
		if self.num != 0:
			text_speech(screen, str(self.num), self.TEXT_COLOR, self.rect.center)