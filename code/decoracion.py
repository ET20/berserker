from settings import tile_verticales, tamaño_tile, ancho_pantalla, a
import pygame

class Cielo:
    def __init__(self,horizonte):
        self.arriba = pygame.image.load('../graphics/fondos/fondo2.png').convert()
        self.fondo = pygame.image.load('../graphics/fondos/fondo22.png').convert()
        self.fondo222 = pygame.image.load('../graphics/fondos/fondo222.png').convert()
        self.horizonte = horizonte

        self.arriba = pygame.transform.scale(self.arriba,(ancho_pantalla,a))
        self.fondo = pygame.transform.scale(self.fondo,(ancho_pantalla,a))
        self.fondo222 = pygame.transform.scale(self.fondo222,(ancho_pantalla,a))
    def draw(self,surface):
        for row in range(tile_verticales):
            y = row * a
            surface.blit(self.arriba,(0,y))
            surface.blit(self.fondo,(0,y))
            surface.blit(self.fondo222,(0,y))