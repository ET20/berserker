import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self,shift):
        self.rect.x += shift

class TileEstatico(Tile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image = surface

class Rocas(TileEstatico):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,pygame.image.load('../graphics/decoracion/level1/roca1.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))
    
class Fondo(TileEstatico):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,pygame.image.load('../graphics/fondos/fondotextura.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))
        
class Fondo2(TileEstatico):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,pygame.image.load('../graphics/fondos/fondotextura2.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

