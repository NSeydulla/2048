import pygame
import time
from config import *
from classes import *

tab = Table()

def text_speech(font, text, color, xy, bold=0):
	font.set_bold(bold)
	rendered_text = font.render(text, True, color)
	text_rect = rendered_text.get_rect(center=xy)
	sc.blit(rendered_text, text_rect)

def game_loop():
	global gamePlay, tab
	while 1:
		# Обработка ивентов(клик, вводить мышкой, нажатие клавиши и т.д)

		for event in pygame.event.get():
			# Выход
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and event.mod == 256):
				pygame.quit(); quit()

			if event.type == pygame.KEYDOWN and gamePlay:
				if event.key == K_LEFT:
					tab = tab.move('-x', tab)
					print('left')

				elif event.key == K_RIGHT:
					tab = tab.move('+x', tab)
					print('right')

				elif event.key == K_UP:
					tab = tab.move('-y', tab)
					print('up')

				elif event.key == K_DOWN:
					tab = tab.move('+y', tab)
					print('down')

			if (event.type == pygame.MOUSEBUTTONDOWN and
				event.button == 1 and
				sc_rect.collidepoint(event.pos) and
				not gamePlay):

				if not can_moves:
					tab = Table()
				gamePlay = True

		# Рисовальня
		can_moves = False
		win = False

		sc.fill(BG_GAME)
		for i in range(cells_num):
			for j in range(cells_num):
				cell = tab.get(i, j)
				cell_rect = pygame.Rect(i*cell_size+border_size*(i+1), j*cell_size+border_size*(j+1), cell_size, cell_size)
				cell_rect = pygame.draw.rect(sc, cell.BG_COLOR, cell_rect)

				text = font.render(str(cell.num), True, cell.CELL_COLOR)
				text_rect = text.get_rect(center=(cell_rect.width/2+cell_rect.x, cell_rect.height/2+cell_rect.y))
				sc.blit(text, text_rect)

				# Проверка на проигрыш
				if cell.isCanMove(tab):
					can_moves = True
				if cell.num == 2048 and not win:
					win = True

		text_speech(font_25, f'Score: {tab.score}', (99, 90, 81), (sc_w//2, sc_h-16))
		if not can_moves:
			gamePlay = False
			text_speech(font_25, 'Игра окончена!', (250, 85, 85), (sc_w//2, sc_h//2-13))
		if win:
			gamePlay = False
			text_speech(font_25, 'Вы выйграли!',       (50,120,50), (sc_w//2, sc_h//2-27))
			text_speech(font_25, 'Можете нажать и продолжить!', (50,120,50), (sc_w//2, sc_h//2-13))

		pygame.display.update()
		clock.tick(70)

pygame.init()
pygame.font.init()
sc = pygame.display.set_mode((sc_w, sc_h))
pygame.display.set_caption("2048 game")
clock = pygame.time.Clock()

font =    pygame.font.Font(None, 20)
font_25 = pygame.font.Font(None, 27)

game_loop()
pygame.quit()
quit()