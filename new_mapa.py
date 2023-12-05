import pygame , os , sys , time
from numpy import asarray
from debug import debug
import support
import settings
from new_cosas import Cama, Estanteria, Habitacion

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
    """
    Un Tile es una cuadrilla del mapa, esta clase sirve para instaciar objetos Cuadrilla
    con esto creo los suelos y los muros por capas
    """
    
    def __init__(self  , x : int, y : int , superficie : pygame.Surface):
        super().__init__()
        
        self.image = superficie
        self.rect = self.image.get_rect(topleft = (x , y))
    

class Mapa:
    def __init__(self, data : dict , superficie : pygame.Surface,) -> None:
        """
        Clase que crea el Mapa mediante capas.
        
        Las capas son archivos CSV, matrices.
        
        Tengo una capa del suelo y los muros
        
        Aquí llamo los metodos de mi archivo Soporte,
        los cuales:
        
        1. Recortan el Sprite Sheet
        2. Leo los csv y los convierto en una matriz que pueda usar
        3. Por cada valor de FILA y COLUMNA, creo un TILE con una posicion y un sprite
        4. El Sprite es agregado al grupo y dibujado en pantalla junto a sus demás compañeros de grupo
        """
        
        self._pantalla = superficie
        self._data = data
        
        self._lista_terrenos = support.import_graficos(self._data["sprites"])
        
        # suelo
        self._suelo = self.crear_grupo_tiles(support.import_csv_layout(self._data["suelo"]))
        
        # paredes
        self._paredes = self.crear_grupo_tiles( support.import_csv_layout(self._data["muros"]))
    
    def crear_cosas(self , grupos_a_pertenecer : list , necesidades):
        cositas = [
                Habitacion().crear_cocina(necesidades , 2 , "assets/img/cosas/cocina.png").crear_horno(),
                Habitacion().crear_baño(necesidades , 1 , "assets/img/cosas/bañera.png").crear_bañera(),
                Cama(necesidades , 2 ,"assets/img/cosas/cama.png"),
                Estanteria(necesidades , 1 , "assets/img/cosas/libreria.png")
                ]
        
        for grupo in asarray(grupos_a_pertenecer):
            for cosa in cositas:
                grupo.add(cosa)
    
    def crear_sprite_tiles(self , x : int, y : int, tile : str):
        xx = x * settings.TILE_SIZE
        yy = y * settings.TILE_SIZE
        
        
        superficie = self._lista_terrenos[int(tile)]
        sprite = Tile(xx , yy, superficie)
        
        return sprite
    
    def crear_grupo_tiles(self , data : list[list]):
        grupo = pygame.sprite.Group()
        
        for fila_indice , fila in enumerate(data):
            for columna_indice , columna in enumerate(fila):
                if columna != '-1':
                    grupo.add(self.crear_sprite_tiles(columna_indice , fila_indice , columna))
                    
        return grupo
    
    def mostrar(self):
        self._suelo.draw(self._pantalla)
        
        self._paredes.draw(self._pantalla)