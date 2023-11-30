from numpy import random
import pygame
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
class Necesidad:
    def __init__(self , nombre : str , velocidad_degrade : "function" , prioridad : int , pos_ui : tuple):
        """
        Clase necesidad, obtiene:
        
        nombre que es usado para asignar correctamente la necesidad a una cosa
        
        una velocidad de degrade que es una funcion (en mi caso, la hice de valores aleatorios)
        
        obtiene un nivel de prioridad para aumentar la atención del Wosim sobre el nivel de necesidad
        
        Por ultimo la posicion de la UI
        """
        
        self._nombre = nombre
        self._puntos = 25
        self._tiempo = velocidad_degrade
        self._multiplicador_prioridad = prioridad
        self._prioridad = 0
        
        self._sprite = lambda i: pygame.image.load(resource_path(f"assets\\img\\UI\\indicador ({i}).png"))
        self.image = self._sprite(25)
        self.rect = self.image.get_rect(center = pos_ui)
        
        self._cosas_que_aumentan_esto = []
        
    def aumentar(self , cant : int):
        self._puntos += cant
        
        if self._puntos > 25:
           self._puntos = 25
           self._prioridad = self._multiplicador_prioridad * (25 - self._puntos)
           return True
       
        self._prioridad = self._multiplicador_prioridad * (25 - self._puntos)
        return False
        
    def decrecer(self):
        self._puntos += -self._tiempo()
        
        self._prioridad = self._multiplicador_prioridad * (25 - self._puntos)
    
    def cuantos_puntos(self):
        return self._puntos
    
    def añadir_cosas(self , cosa : object):
        self._cosas_que_aumentan_esto.append(cosa) # añado cosas, como su nombre lo dice
    
    def seleccionar_una_cosa(self):
        return self._cosas_que_aumentan_esto[random.randint(0 , len(self._cosas_que_aumentan_esto))]
    
    @property # esto es un getter, setter y deleter
    def nombre(self):
        return self._nombre
    
    @property
    def prioridad(self):
        return self._prioridad
    
    def mostrar_UI(self): 
        if 20 < self._puntos <= 25:
            self.image = self._sprite(25)
        
        if 15 < self._puntos <= 20:
            self.image = self._sprite(20)
        
        if 10 < self._puntos <= 15:
            self.image = self._sprite(15)
        
        if 5 < self._puntos <= 10:
            self.image = self._sprite(10)
        
        if 0 < self._puntos <= 5:
            self.image = self._sprite(5)
        
        if self._puntos <= 0:
            self.image = self._sprite(0)
        
        return (self.image , self.rect)