from csv import reader
import numpy as np
import pygame
import settings

def import_csv_layout(path : str):
    
    mapa_suelo = []
    
    with open(path) as map:
        mapa = reader(map , delimiter= ",")
        
        for fila in mapa:
            mapa_suelo.append(list(fila))
    
    return mapa_suelo

def import_graficos(path : str):
        surface = pygame.image.load(path).convert_alpha()
        
        tile_num_x : int = surface.get_width() // settings.TILE_SIZE
        tile_num_y : int = surface.get_height() // settings.TILE_SIZE
        
        tiles_cortados = []
        for fila in np.arange(tile_num_y):
            for columna in np.arange(tile_num_x):
                x = columna * settings.TILE_SIZE
                y = fila * settings.TILE_SIZE
                
                nueva_surf = pygame.Surface((settings.TILE_SIZE , settings.TILE_SIZE)).convert_alpha()
                nueva_surf.blit(surface , (0 , 0) , pygame.Rect(x , y , settings.TILE_SIZE , settings.TILE_SIZE))
                nueva_surf.set_colorkey((0 , 0 , 0) , pygame.BLEND_RGB_MULT)
                tiles_cortados.append(nueva_surf)
                
        return tiles_cortados