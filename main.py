import pygame
from config import *
from classes import GAME

def main():
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: return
			if event.type == pygame.KEYDOWN and event.key in KEYS and not GAME.isBusy and GAME.active:
				GAME.onKeyDown(KEYS.index(event.key))
		GAME.draw()
		GAME.tick(24)

pygame.init()

screen = pygame.display.set_mode((sc.w, sc.h))
GAME = GAME(screen)

pygame.display.set_caption("2048 game")

KEYS = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN]

main()
pygame.quit()