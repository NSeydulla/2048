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
		self.startTime = 0

		#background
		self.background = pygame.Surface((sc.w, sc.h))
		self.background.fill(sc.BG_COLOR)
		for x in range(sc.cells_num):
			for y in range(sc.cells_num):
				pygame.draw.rect(self.background, sc.CELL_COLOR[0], (CRP(x), CRP(y), sc.cell_size, sc.cell_size))

		#main params
		self.sc = screen
		self.cells = [None for _ in range(sc.cells_num**2)]
		self.spawn()

	def animate(self):
		t = time()-self.startTime
		if t<sc.animate_time: # min or max : (sx + dx*t/at, end_x) #sx-start_x
			dt = (t/sc.animate_time)
			for cell in self.cells:
				cell.animate(dt)

	def draw(self):
		self.sc.blit(self.background, (0,0))
		for cell in self.cells:
			if cell is not None: cell.draw(self.sc)
		pygame.display.update()

	def onKeyDown(self, key):
		for cell in self.cells[::-1 if key>=2 else 1]:
			if cell is not None: cell.move(key)
		self.spawn()

	def sort(self):
		self.cells.sort(key=lambda cell: cell.y*sc.cells_num+cell.x)

	def spawn(self):
		for i in range(2):
			x, y = rint(0,sc.cells_num-1), rint(0,sc.cells_num-1)
			if self.cells[y*sc.cells_num+x] is None:
				cell = Cell(2, x, y)
				self.cells.append(cell)
				if rint(0,3)==0:cell.double()
		self.sort()

class Cell(object):
	def __init__(self, num, x, y):
		self.x, self.y = x, y
		self.num = num
		self.update()
		self.rect = pygame.Rect(CRP(x), CRP(y), sc.cell_size, sc.cell_size)

	def update(self):
		self.CELL_COLOR = sc.CELL_COLOR.get(self.num, (0,0,0))
		self.TEXT_COLOR = sc.TEXT_COLOR.get(self.num, (255,255,255))

	def double(self):
		pass

	def move(self, key):
		pass

	def draw(self, screen):
		pygame.draw.rect(screen, self.CELL_COLOR, self.rect)
		text_speech(screen, str(self.num), self.TEXT_COLOR, self.rect.center)