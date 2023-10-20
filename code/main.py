import pygame, sys
from settings import *
from level import Nivel
from gamedata import level_1

# Pygame setup
pygame.init()

screen = pygame.display.set_mode((ancho_pantalla,alto_pantalla))
clock = pygame.time.Clock()
nivel = Nivel(level_1,screen)
pygame.display.set_caption('juegocolegio')

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill('white')
	nivel.ejecutar()

	pygame.display.update()
	clock.tick(60)