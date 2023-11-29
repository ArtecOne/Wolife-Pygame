import pygame , os , sys , time
from numpy import random
from debug import debug
import support
import settings
from data import MAPA_MATRIX
from new_necesidad import HAMBRE, HIGIENE , ENERGIA , DIVERSION

pygame.init()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Tile(pygame.sprite.Sprite):
    def __init__(self , tamaño_tile : int , x : int, y : int , superficie : pygame.Surface):
        super().__init__()
        
        self.image = superficie
        self.rect = self.image.get_rect(topleft = (x , y))
    
    def update(self, offset = None) -> None:
        pass 


class Cosa(pygame.sprite.Sprite):
    def __init__(self, necesidad , imagen, grupos):
        super().__init__(*grupos)
        self.necesidad = necesidad
        
        self.seleccion_x = random.randint(0 , settings.ANCHURA_PANTALLA) // settings.TILE_SIZE 
        self.seleccion_y = random.randint(0 , settings.ALTURA_PANTALLA) // settings.TILE_SIZE
        
        if MAPA_MATRIX[self.seleccion_y][self.seleccion_x] != -1:
            self.seleccion_x , self.seleccion_y = [random.randint(0 , settings.ANCHURA_PANTALLA) // settings.TILE_SIZE , random.randint(0 , settings.ALTURA_PANTALLA) // settings.TILE_SIZE]
        
        self.image = pygame.image.load(resource_path(imagen)).convert_alpha()
        self.rect = self.image.get_rect(center = (self.seleccion_x * 32 , self.seleccion_y * 32))
    
    def usar(self):
        if not self.necesidad:
            return
        
        self.necesidad.puntos += 0.3
        


class Mapa:
    def __init__(self, data : dict , superficie : pygame.Surface , grupo_cosas , grupo_todos) -> None:
        self.pantalla = superficie
        self.movimiento_camara = 0
        self.data = data
        
        self.lista_terrenos = support.import_graficos(self.data["sprites"])
        
        # suelo
        self.suelo = self.crear_grupo_tiles(support.import_csv_layout(self.data["suelo"]))
        
        # paredes
        self.paredes = self.crear_grupo_tiles( support.import_csv_layout(self.data["muros"]))
        
        # cosas
        Cosa(HIGIENE , "assets\\img\\cosas\\bañera.png" , (grupo_cosas , grupo_todos))
        Cosa(HAMBRE , "assets\\img\\cosas\\cocina.png" , (grupo_cosas , grupo_todos))
        Cosa(DIVERSION , "assets\\img\\cosas\\libreria.png" , (grupo_cosas , grupo_todos))
        Cosa(ENERGIA , "assets\\img\\cosas\\cama.png" , (grupo_cosas , grupo_todos))
    
    def crear_sprite_tiles(self , x : int, y : int, tile : str):
        xx = x * settings.TILE_SIZE
        yy = y * settings.TILE_SIZE
        
        
        superficie = self.lista_terrenos[int(tile)]
        sprite = Tile(settings.TILE_SIZE , xx , yy, superficie)
        
        return sprite
    
    def crear_grupo_tiles(self , data : list[list]):
        grupo = pygame.sprite.Group()
        
        for fila_indice , fila in enumerate(data):
            for columna_indice , columna in enumerate(fila):
                if columna != '-1':
                    grupo.add(self.crear_sprite_tiles(columna_indice , fila_indice , columna))
                    
        return grupo
    
    def mostrar(self):
        self.suelo.draw(self.pantalla)
        self.suelo.update()
        
        self.paredes.draw(self.pantalla)
        self.paredes.update()