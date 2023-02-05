import pygame
from config import *
from classes import Game

def main():
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: return
			if event.type == pygame.KEYDOWN and event.key in KEYS and not Game.isBusy and Game.active:
				Game.onKeyDown(KEYS.index(event.key))
		Game.draw()
		clock.tick(30)

pygame.init()
screen = pygame.display.set_mode((sc.w, sc.h))
pygame.display.set_caption("2048 game")

Game = Game(screen)
clock = pygame.time.Clock()

KEYS = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN]

main()
pygame.quit()