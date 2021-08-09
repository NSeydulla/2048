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
	global gamePlay, tab, win
	pressed='+x'
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and event.mod == 256):
				pygame.quit(); quit()

			if event.type == pygame.KEYDOWN and gamePlay and event.key in KEYS and pressed == '':
				tab = tab.move(KEYS[event.key], tab)
				pressed = KEYS[event.key]

			if (event.type == pygame.MOUSEBUTTONDOWN and
				event.button == 1 and
				sc_rect.collidepoint(event.pos) and
				not gamePlay):

				if not can_moves:
					tab = Table()
				gamePlay = True
				win = False


		can_moves = False
		for i in range(cells_num):
			for j in range(cells_num):
				cell = tab.get(i, j)
				if cell.num != 0:
					if cell.isCanMove(tab):
						can_moves = True
					if cell.num == 2048 and not tab.already_winned:
						win = True
						gamePlay = False
						tab.already_winned = True

		# Рисовальня
		if pressed!='':
			sc.fill(BG_COLOR[0])
			for i in range(cells_num+1):
				coord = (cell_size+border_size)*i
				pygame.draw.rect(sc, BG_GAME, (coord, 0, border_size, sc_w))
				pygame.draw.rect(sc, BG_GAME, (0, coord, sc_w, border_size))
				if i == cells_num:
					pygame.draw.rect(sc, BG_GAME, (0, coord, sc_w, sc_h-coord))

			text_speech(font_25, f'Score: {tab.score}', (99, 90, 81), (sc_w//4, sc_h-16))
			text_speech(font_25, f'record: {tab.record}', (99, 90, 81), (sc_w//2+sc_w//4, sc_h-16))
			if not can_moves:
				gamePlay = False
				text_speech(font_25, 'Игра окончена!', (250, 85, 85), (sc_w//2, sc_h//2-13))
			if win:
				text_speech(font_25, 'Вы выйграли!',       (50,120,50), (sc_w//2, sc_h//2-27))
				text_speech(font_25, 'Можете нажать и продолжить!', (50,120,50), (sc_w//2, sc_h//2-13))


			a = -1 if '+' in pressed else 1
			for b in range(int((cell_size+border_size)*4/speed)):
				for i in range(cells_num)[::a]:
					for j in range(cells_num)[::a]:
						for g in range(cells_num+1):
							coord = (cell_size+border_size)*g
							pygame.draw.rect(sc, BG_GAME, (coord, 0, border_size, sc_w))
							pygame.draw.rect(sc, BG_GAME, (0, coord, sc_w, border_size))
							if g == cells_num:
								pygame.draw.rect(sc, BG_GAME, (0, coord, sc_w, sc_h-coord))

						x, y = (j, i) if 'y' in pressed else (i, j)
						moving_cell = tab.moves[y][x]
						
						pygame.draw.rect(sc, BG_COLOR[0], pygame.Rect(moving_cell[4], moving_cell[5], cell_size, cell_size))
						
						x_or_y = 1 if 'y' in pressed else 0
						if moving_cell[4+x_or_y] != moving_cell[2+x_or_y]:
							moving_cell[4+x_or_y] += speed if '+' in pressed else -speed

						cell_rect = pygame.Rect(moving_cell[4], moving_cell[5], cell_size, cell_size)
						cell_rect = pygame.draw.rect(sc, moving_cell[6].BG_COLOR, cell_rect)
						text_speech(font, str(moving_cell[6].num), moving_cell[6].CELL_COLOR, (cell_rect.width//2+cell_rect.x, cell_rect.height//2+cell_rect.y))

						pygame.display.update()
						pygame.time.delay(1)
			tab.moves = [[[i, j, CRP(j), CRP(i), CRP(j), CRP(i), tab.cells[i][j]] for j in range(cells_num)] for i in range(cells_num)]

			pressed = ''
			pygame.display.update()
		clock.tick(30)

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