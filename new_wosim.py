import pygame
import os
import sys
from debug import debug
from numpy import random
import settings
from data import MAPA_MATRIX
from pathfinding.core.grid import Grid
from pathfinding.finder.bi_a_star import BiAStarFinder as BiAstar
from new_necesidad import HAMBRE, HIGIENE , ENERGIA , DIVERSION

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Wosim (pygame.sprite.Sprite):
    def __init__(self , grupos):
        super().__init__(*grupos)
        self.pantalla = pygame.display.get_surface()
        self.necesidades = [HAMBRE , HIGIENE , ENERGIA , DIVERSION]
        
        self.puntos = -5
        
        self.estado = Esperando(self)
        
        self.grupo_todos : pygame.sprite.Group = grupos[1]
        
        
        self.inicio_x = self.pantalla.get_width()//2 // 32
        self.inicio_y = self.pantalla.get_height()//2 // 32
        
        self.rect = self.image.get_rect(center = (self.inicio_x * 32 , self.inicio_y * 32))
        
        self.objetivo = pygame.image.load(resource_path("assets\\img\\UI\\selection.png")).convert_alpha()
        self.objetivo_rect = pygame.Rect(self.rect.topleft, (settings.TILE_SIZE , settings.TILE_SIZE))

    def update(self , delta):
        self.estado.main(delta)
        self.pantalla.blit(self.objetivo , self.objetivo_rect)
        debug(f"hambre {int(HAMBRE.puntos)} , higiene {int(HIGIENE.puntos)} , energia {int(ENERGIA.puntos)} , diversion {int(DIVERSION.puntos)}" , self.pantalla.get_width()//2)
        
class Esperando:
    def __init__(self , jugador : Wosim):
        self.humano = jugador
        
        self.humano.image = pygame.image.load(resource_path("assets\\img\\player\\idle.png")).convert_alpha()
        
        self.objetivo = 0
        
        self.seleccion_x = 0
        self.seleccion_y = 0
        
        self.need = 0
        
        
    def actualizar(self):
        for necesidad in self.humano.necesidades:
            if necesidad.puntos < 5:
                self.need = necesidad
        
        for cosa in self.humano.grupo_todos.sprites():
            if cosa == self.humano:
                continue
            
            if self.need == cosa.necesidad:
                self.objetivo = cosa
                
                self.seleccion_x = self.objetivo.rect.centerx // 32
                self.seleccion_y = self.objetivo.rect.centery // 32
                break
                
        
        
    def main(self , delta):
        self.actualizar()
        
        if self.objetivo:
            self.humano.objetivo_rect.topleft = (self.seleccion_x * settings.TILE_SIZE, self.seleccion_y * settings.TILE_SIZE)
            
            self.humano.estado = Movimiento(self.humano, (self.humano.objetivo_rect.centerx // 32, self.humano.objetivo_rect.centery // 32), self.objetivo)
            
class Movimiento:
    def __init__(self , jugador : Wosim, destino : tuple, objeto) -> None:
        self.humano = jugador
        self.objeto = objeto
        self.pantalla = pygame.display.get_surface()
        self.direccion = pygame.math.Vector2(0 , 0)
        self.pos = self.humano.rect.center
        
        self.inicio = (self.humano.rect.centerx // settings.TILE_SIZE , self.humano.rect.centery // settings.TILE_SIZE)
        
        self.grafo = Grid(matrix= MAPA_MATRIX , inverse= True)
        
        self.nodo_inicio = self.grafo.node(*self.inicio)
        self.nodo_final = self.grafo.node(*destino)
        
        self.path =  []
        self.puntos = []
        self.colisiones = []
        
        self.index = 1
        self.sprite = lambda i , image: pygame.image.load(resource_path(image.format(int(i)))).convert_alpha()
        self.humano.image = self.sprite(self.index , "assets\\img\\player\\front_run ({}).png")
        
        self.crear_camino()
    
    def crear_camino(self):
        finder = BiAstar(diagonal_movement= True)
        
        camino , pasos = finder.find_path(self.nodo_inicio , self.nodo_final , self.grafo)
        
        self.path = [(obj.x , obj.y) for obj in camino]
        
        self.puntos = [((x * 32) + 16, (y * 32) + 16) for x,y in self.path]
        
        self.colisiones = [pygame.Rect((x -2 , y - 2) , (4 , 4)) for x , y in self.puntos[1 : -1]]
    
    def ir(self, delta):
        if not self.colisiones:
            return
        
        self.index += 6 * delta
        
        if self.index > 4:
            self.index = 1
            
        inicio = pygame.math.Vector2(self.humano.rect.center)
        
        final = pygame.math.Vector2(self.colisiones[0].center)
        
        self.direccion = (final - inicio).normalize()
        
        self.pos += self.direccion * 70 * delta
        self.humano.rect.center = self.pos
        
        
        for rect in self.colisiones:
            if rect.collidepoint(self.pos):
                del self.colisiones[0]
        
        if not self.colisiones:
            return
        
        if self.colisiones[0].centery > self.humano.rect.centery: 
            self.humano.image = self.sprite(self.index, "assets\\img\\player\\front_run ({}).png")
        
        elif  self.colisiones[0].centery < self.humano.rect.centery:
            self.humano.image = self.sprite(self.index, "assets\\img\\player\\back_run ({}).png")
            
        elif  self.colisiones[0].centerx > self.humano.rect.centerx:
            self.humano.image = self.sprite(self.index, "assets\\img\\player\\der_run ({}).png")
            
        elif  self.colisiones[0].centerx < self.humano.rect.centerx:
            self.humano.image = self.sprite(self.index, "assets\\img\\player\\izq_run ({}).png")
        
        
    def main(self, delta):
        self.ir(delta)
        
        if not self.puntos:
            return
        
        if not self.colisiones:
            self.humano.estado = Satisfaciendo(self.humano , self.objeto)
            
            
class Satisfaciendo:
    def __init__(self , jugador : Wosim, objeto) -> None:
        self.humano = jugador
        
        self.obj = objeto
        
        self.humano.image = pygame.image.load(resource_path("assets\\img\\player\\idle.png")).convert_alpha()
        
    def main(self , delta = None):
        
        self.obj.usar()
        
        if self.obj.necesidad.puntos >= 10:
            self.humano.estado = Esperando(self.humano)