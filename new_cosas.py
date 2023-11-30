import pygame
import os
import sys
from numpy import random
from numpy import asarray
from data import MAPA_MATRIX
import settings

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Cosa(pygame.sprite.Sprite):
    def __init__(self , necesidades : list , puntos, imagen):
        """
        Clase superior de todas las cosas, metodos generales se encuentran aquí,
        como el usar ; yo_relleno ; crearse
        """
        super().__init__()
        
        for need in asarray(necesidades):
            need.añadir_cosas(self)
        
        self._necesidades = necesidades
        
        self._pts = puntos
        
        self.image = pygame.image.load(resource_path(imagen)).convert_alpha()
        self.rect = self.image.get_rect(center = self.crearse())
    
    def crearse(self):
        seleccion_x = random.randint(0 , settings.ANCHURA_PANTALLA) // settings.TILE_SIZE 
        seleccion_y = random.randint(0 , settings.ALTURA_PANTALLA) // settings.TILE_SIZE
        
        if MAPA_MATRIX[seleccion_y][seleccion_x] != -1:
            return self.crearse()
        
        return (seleccion_x * settings.TILE_SIZE , seleccion_y * settings.TILE_SIZE)
    
    def yo_relleno(self):
        return self._necesidades
    
    def usar(self , necesidad_a_rellenar):
        
        return necesidad_a_rellenar.aumentar(self._pts) # debido a que hay varios personajes, debo pasarle a la cosa la necesidad a Aumentar, de igual forma compruebo ante si existe en este objeto
        
class Cama(Cosa):
    def __init__(self , necesidad , puntos , imagen):
        super().__init__([need for need in asarray(necesidad) if need.nombre == "sueño"] , puntos , imagen)
        
    def hacer_noche(self):
        """
        funcion especializada de ejemplo para la cama
        """ 
        pass
    
class Estanteria(Cosa):
    def __init__(self , necesidad , puntos , imagen):
        super().__init__([need for need in asarray(necesidad) if need.nombre == "diversion"] , puntos , imagen)
    
    def aprender(self):
        """
        funcion especializada de ejemplo para la estanteria
        """
        pass

class Habitacion:
    def __init__(self) -> None:
        pass
    
    def crear_cocina(self , necesidad, puntos , imagen):
        return Cocina(necesidad , puntos , imagen)
    
    def crear_baño(self , necesidad , puntos , imagen):
        return Baño(necesidad , puntos , imagen)

class Cocina:
    def __init__(self , necesidad , puntos , imagen):
        """
        Esta es una clase que devuelve el objeto que quiero de la zona Cocina
        """
        
        self._necesidad = [need for need in asarray(necesidad) if need.nombre == "hambre"]
        self._puntos = puntos
        self._imagen = imagen
    
    def crear_horno(self):
        return Horno(self._necesidad , self._puntos , self._imagen)
        
class Baño:
    def __init__(self , necesidad , puntos , imagen):
        """
        Esta es una clase que devuelve un objeto que quiero de la zona Baño
        """
    
        self._necesidad = [need for need in asarray(necesidad) if need.nombre == "higiene"]
        self._puntos = puntos
        self._imagen = imagen
    
    def crear_bañera(self):
        return Bañera(self._necesidad , self._puntos , self._imagen)

class Horno(Cosa):
    def __init__(self , necesidad , puntos , imagen):
        super().__init__(necesidad , puntos , imagen)
       
class Bañera(Cosa):
    def __init__(self , necesidad , puntos , imagen):
        super().__init__(necesidad , puntos , imagen)