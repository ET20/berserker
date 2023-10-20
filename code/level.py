import pygame
from soporte import import_csv_layout, import_cut_graphics 
from settings import tamaño_tile, ancho_pantalla, alto_pantalla
from tiles import Tile, TileEstatico, Rocas, Fondo, Fondo2
from decoracion import Cielo
from player import Player
from particles import ParticleEffect
class Nivel:
    def __init__(self,level_data,surface):

        #configuracion general
        self.display_surface = surface
        self.world_shift = 0

        player_layout =  import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        self.dust_sprite = pygame.sprite.GroupSingle()
        
       
        #añadir terreno
        terreno_plano = import_csv_layout(level_data['terreno'])
        self.terreno_sprites = self.grupo_crea_tile(terreno_plano,'terreno')

        #añadir fondo terreno
        plano_fondo_terreno = import_csv_layout(level_data['fondoterreno'])
        self.fondoterreno_sprites = self.grupo_crea_tile(plano_fondo_terreno,'fondoterreno')
        
        #añadir rocas
        rocas_plano = import_csv_layout(level_data['rocas'])
        self.rocas_sprite = self.grupo_crea_tile(rocas_plano,'rocas')

        #añadir fondo
        fondo_plano = import_csv_layout(level_data['fondo'])
        self.fondo_sprite = self.grupo_crea_tile(fondo_plano,'fondo')

        #añadior fondo 2
        fondo_plano2 = import_csv_layout(level_data['fondo2'])
        self.fondo2_sprite = self.grupo_crea_tile(fondo_plano2,'fondo2')

    def grupo_crea_tile(self,layout,type):
        grupo_sprite = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tamaño_tile
                    y = row_index * tamaño_tile

                    if type =='terreno':
                        terreno_tile_lista = import_cut_graphics('../graphics/tiles/tile.png')
                        tile_surface = terreno_tile_lista[int(val)]
                        sprite = TileEstatico(tamaño_tile,x,y,tile_surface)
                        grupo_sprite.add(sprite)
                    if type =='fondoterreno':
                        fondoterreno_tile_lista = import_cut_graphics('../graphics/tiles/fondotiles.png')
                        tile_surface = fondoterreno_tile_lista[int(val)]
                        sprite = TileEstatico(tamaño_tile,x,y,tile_surface)
                    if type =='rocas':
                        sprite = Rocas(tamaño_tile,x,y)
                    if type =='fondo':
                        sprite = Fondo(tamaño_tile,x,y)
                    if type =='fondo2':
                        sprite = Fondo2(tamaño_tile,x,y)
                    grupo_sprite.add(sprite)

        return grupo_sprite
    
    
    
    
    def player_setup(self,layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tamaño_tile
                y = row_index * tamaño_tile
                if val == '0':
                    sprite = Player((x,y),self.display_surface,self.create_jump_particles)
                    self.player.add(sprite)
                if val == '1':
                    hat_surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
                    sprite = TileEstatico(tamaño_tile,x,y,hat_surface)
                    self.goal.add(sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < ancho_pantalla / 2 and direction_x < 0:
        	self.world_shift = 8
        	player.speed = 0
        elif player_x > ancho_pantalla - (ancho_pantalla / 2) and direction_x > 0:
        	self.world_shift = -8
        	player.speed = 0
        else:
        	self.world_shift = 0
        	player.speed = 8

    def create_jump_particles(self,pos):
        if self.player.sprite.facing_right:
	        pos -= pygame.math.Vector2(10,5)
        else:
        	pos += pygame.math.Vector2(10,-5)
        jump_particle_sprite = ParticleEffect(pos,'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terreno_sprites.sprites()
        for sprite in collidable_sprites:
        	if sprite.rect.colliderect(player.rect):
        		if player.direction.x < 0: 
        			player.rect.left = sprite.rect.right
        			player.on_left = True
        			self.current_x = player.rect.left
        		elif player.direction.x > 0:
        			player.rect.right = sprite.rect.left
        			player.on_right = True
        			self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
        	player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
        	player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terreno_sprites.sprites()

        for sprite in collidable_sprites:
        	if sprite.rect.colliderect(player.rect):
        		if player.direction.y > 0: 
        			player.rect.bottom = sprite.rect.top
        			player.direction.y = 0
        			player.on_ground = True
        		elif player.direction.y < 0:
        			player.rect.top = sprite.rect.bottom
        			player.direction.y = 0
        			player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
        	player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
        	player.on_ceiling = False

    def ejecutar(self):

         #añadir fondo
        self.fondo_sprite.update(self.world_shift)
        self.fondo_sprite.draw(self.display_surface)

        #añadir fondo 2
        self.fondo2_sprite.update(self.world_shift)
        self.fondo2_sprite.draw(self.display_surface)
        #fondo terreno añadir
        self.fondoterreno_sprites.update(self.world_shift)
        self.fondoterreno_sprites.draw(self.display_surface)

        #terreno añadir 
        self.terreno_sprites.update(self.world_shift)
        self.terreno_sprites.draw(self.display_surface)
        
        #añadir rocas
        self.rocas_sprite.update(self.world_shift)
        self.rocas_sprite.draw(self.display_surface)

       

        #personaje
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)   
        self.scroll_x() 
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        
        
         
            
        
       

        

       

        
        


        