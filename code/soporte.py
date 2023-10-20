import pygame
from csv import reader
from settings import tamaño_tile
from os import walk

def import_csv_layout(path):
    terreno_mapa = []
    with open(path) as map:
        nivel = reader(map,delimiter = ',')
        for row in nivel:
            terreno_mapa.append(list(row))
        return terreno_mapa

def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tamaño_tile)
    tile_num_y = int(surface.get_size()[1] / tamaño_tile)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tamaño_tile
            y = row * tamaño_tile
            nueva_surface = pygame.Surface((tamaño_tile,tamaño_tile),flags = pygame.SRCALPHA)
            nueva_surface.blit(surface,(0,0),pygame.Rect(x,y,tamaño_tile,tamaño_tile))
            cut_tiles.append(nueva_surface)

    return cut_tiles

def import_folder(path):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

