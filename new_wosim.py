import pygame
import os
import sys
from debug import debug
import settings
from data import MAPA_MATRIX
from numpy import random
from numpy import asarray
from pathfinding.core.grid import Grid
from pathfinding.finder.bi_a_star import BiAStarFinder as BiAstar
from new_necesidad import Necesidad

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Wosim (pygame.sprite.Sprite):
    def __init__(self , nombre : str , grupos : list, ui_pos : tuple):
        """
        Recibe el nombre
        Grupo al que pertenece
        Posicion de su UI
        """
        
        super().__init__(*grupos)
        self._nombre = nombre
        self._pantalla = pygame.display.get_surface() # obtiene la superficie del display
        
        x , self.yy = ui_pos # desempaqueto el la posicion del UI para....
        
        self._necesidades = [Necesidad("hambre",  lambda: random.randint(0 , 3), 6 , (x , self.yy)), # hacer esto...
                            Necesidad("higiene", lambda: random.randint(0 , 3), 2 , (x + 100 , self.yy)),
                            Necesidad("sueño", lambda: random.randint(0 , 3), 4, (x + 200 , self.yy)),
                            Necesidad("diversion", lambda: random.randint(0 , 3), 2 , (x + 300 , self.yy))]
        
        self._estado = Esperando(self) # cerebro
        # Estado inicial, cuando termina su tarea, ese Self se lo pasa al siguiente Estado antes de destruirse ( basicamente  self._humano.siguiente_estado(self._humano , args) cada que comete una transicion)
        
        self._grupo_todos : pygame.sprite.Group = grupos[1] # GRUPO_TODOS , en i = 0 está GRUPO_JUGADOR
        
        self._inicio_x = self._pantalla.get_width()//2 // 32
        self._inicio_y = self._pantalla.get_height()//2 // 32
        
        self.rect = self.image.get_rect(center = (self._inicio_x * 32 , self._inicio_y * 32)) # RECT es una propiedad de pygame.Sprite al igual que IMAGE
        
        self._objetivo = pygame.image.load(resource_path("assets\\img\\UI\\selection.png")).convert_alpha()
        self._objetivo_rect = pygame.Rect(self.rect.topleft, (settings.TILE_SIZE , settings.TILE_SIZE))

    @property
    def me_llamo(self) -> str:
        return self._nombre
    
    @property
    def necesidades(self) -> list:
        return self._necesidades
    
    @property
    def rectangulo_objetivo(self):
        return self._objetivo_rect
    
    @property
    def grupo_todos(self):
        return self._grupo_todos

    def set_estado(self , state):
        self._estado = state
    
    def decrementar_necesidades(self):
        [need.decrecer() for need in asarray(self._necesidades)] # jugador.decrementar_necesidades()  sujeto y predicado
    
    def update(self , delta): # metodo polimorfico de todos los sprites, el grupo al cual pertenece llama este metodo para todos sus sprites
        self._estado.main(delta)
        
        for need in asarray(self._necesidades):
            self._pantalla.blit(*need.mostrar_UI())
        
        self._pantalla.blit(self._objetivo , self._objetivo_rect)
        
        debug(f"Nombre {self._nombre} , hambre {int(self._necesidades[0].prioridad)} , higiene {int(self._necesidades[1].prioridad)} , energia {int(self._necesidades[2].prioridad)} , diversion {int(self._necesidades[3].prioridad)}" , self._pantalla.get_width()//2 - 80, self.yy + 10)
        
class Esperando:
    def __init__(self , jugador : Wosim):
        self._humano = jugador
        
        self._humano.image = pygame.image.load(resource_path("assets\\img\\player\\idle.png")).convert_alpha() # image es una propieda de pygame.Sprite
        
        self._donde_ir = 0 # esto se convierte en una Cosa
        
        self._seleccion_x = 0
        self.seleccion_y = 0
        
        self._need = 0
    
    def priorizar(self):
        necesidades = sorted(self._humano.necesidades , key= lambda nece: nece.prioridad , reverse= True) # ordeno una lista de necesidades en base a su prioridad
        return necesidades[random.randint(2)]
    
    def asignar_need_y_donde_ir(self, necesidad):
        self._need = necesidad
            
        self._donde_ir = self._need.seleccionar_una_cosa() # aquí selecciono random una Cosa que satisfazca la necesidad
                
        self.seleccion_x = self._donde_ir.rect.centerx // settings.TILE_SIZE # Obtengo la posicion de la cosa para posicionar mi rectangulo Objetivo
        self.seleccion_y = self._donde_ir.rect.centery // settings.TILE_SIZE
    
    def buscar(self):
        
        necesidad = self.priorizar()
        
        if necesidad.cuantos_puntos() < random.randint(10 , 21): # La personaje elige aleatoriamente cuando es necesario ir a satisfacerse
            self.asignar_need_y_donde_ir(necesidad)
        
        
        
    def main(self , delta = None):
        self.buscar()
        
        if self._donde_ir: # si hay donde ir, pues posiciono mi rectangulo objetivo y paso al siguiente estado
            self._humano.rectangulo_objetivo.topleft = (self.seleccion_x * settings.TILE_SIZE, self.seleccion_y * settings.TILE_SIZE)
            
            self._humano.set_estado(Movimiento(self._humano, # si no me transfiero a mi mismo, no podré ver hacer nada, el personaje queda sin cerebro
                                               (self._humano.rectangulo_objetivo.centerx // settings.TILE_SIZE, self._humano.rectangulo_objetivo.centery // settings.TILE_SIZE),
                                               self._donde_ir , self._need))
            
class Movimiento:
    def __init__(self , jugador : Wosim, destino : tuple, cosa_donde_ir : object , necesidad) -> None:
        """
        Esta clase se encarga de apuntar y mover al personaje
        
        crea un grafo apartir de una matriz
        crea nodos
        
        crea un camino, puntos de recta, colisiones para que el personaje siga esos puntos
        
        al final, cometemos la transicion pasando los datos necesarios para el siguiente estado
        """
        self._humano = jugador # por supuesto, mi cerebro me conoce
        self._cosa = cosa_donde_ir # la cosa que voy a usar
        self._need = necesidad # la necesidad que debo satisfacer
        
        self._pantalla = pygame.display.get_surface()
        self._direccion = pygame.math.Vector2(0 , 0)
        self._pos = self._humano.rect.center # obtengo la posicion actual de mi personaje
        
        self._inicio = (self._humano.rect.centerx // settings.TILE_SIZE , self._humano.rect.centery // settings.TILE_SIZE)
        # convierto la posicion actual de mi personaje a tamaño cuadricula para poder crear nodo en el grafo
        
        self._grafo = Grid(matrix= MAPA_MATRIX , inverse= True)
        # inverso ya que la matriz es la capa de muros, -1 es el suelo
        
        self._nodo_inicio = self._grafo.node(*self._inicio)
        self._nodo_final = self._grafo.node(*destino)
        
        self._path =  []
        self._puntos = []
        self._colisiones = []
        
        self._index = 1
        self._sprite = lambda i , image: pygame.image.load(resource_path(image.format(int(i)))).convert_alpha()
        self._humano.image = self._sprite(self._index , "assets\\img\\player\\front_run ({}).png")
        
        self.crear_camino()
    
    def crear_camino(self):
        finder = BiAstar(diagonal_movement= True)
        
        camino , pasos = finder.find_path(self._nodo_inicio , self._nodo_final , self._grafo) # pasos son cuantas cuadriculas tengo que recorrer, no me sirve de nada
        
        self._path = [(obj.x , obj.y) for obj in asarray(camino)] # obtengo las cordenadas del camino
        
        self._puntos = [((x * 32) + 16, (y * 32) + 16) for x,y in asarray(self._path)] # las normalizo y centro
        
        self._colisiones = [pygame.Rect((x -2 , y - 2) , (4 , 4)) for x , y in asarray(self._puntos[1 : -1])] # creo pequeñas colisiones para esos puntos que el jugador seguirá
    
    def ir(self, delta):
        if not self._colisiones:
            return
        
        self._index += 6 * delta
        
        if self._index > 4:
            self._index = 1
            
        inicio = pygame.math.Vector2(self._humano.rect.center)
        
        final = pygame.math.Vector2(self._colisiones[0].center)
        
        self._direccion = (final - inicio).normalize() # crea la direccion en x & y donde se moverá el personaje
        
        self._pos += self._direccion * 100 * delta # velocidad jugador
        self._humano.rect.center = self._pos # asignacion de posicion
        
        
        for rect in self._colisiones:
            if rect.collidepoint(self._pos):
                del self._colisiones[0] # cuando colisiona se elimina provocando que tenga que trackear la siguiente colision
        
        if not self._colisiones:
            return
        
        if self._colisiones[0].centery > self._humano.rect.centery: 
            self._humano.image = self._sprite(self._index, "assets\\img\\player\\front_run ({}).png")
        
        elif  self._colisiones[0].centery < self._humano.rect.centery:
            self._humano.image = self._sprite(self._index, "assets\\img\\player\\back_run ({}).png")
            
        elif  self._colisiones[0].centerx > self._humano.rect.centerx:
            self._humano.image = self._sprite(self._index, "assets\\img\\player\\der_run ({}).png")
            
        elif  self._colisiones[0].centerx < self._humano.rect.centerx:
            self._humano.image = self._sprite(self._index, "assets\\img\\player\\izq_run ({}).png")
        
        
    def main(self, delta = None):
        self.ir(delta)
        
        if not self._puntos: # si aun no he creado puntos, pues no sigo avanzando
            return
        
        if not self._colisiones: # cuando no hay más puntos significa que llegué al final
            self._humano.set_estado(Satisfaciendo(self._humano , self._cosa , self._need))
            
            
class Satisfaciendo:
    def __init__(self , jugador : Wosim, cosa , necesidad) -> None:
        self._humano = jugador
        
        self._cosa = cosa
        
        self._need = necesidad
        
        self._humano.image = pygame.image.load(resource_path("assets\\img\\player\\idle.png")).convert_alpha()
        
    def main(self , delta = None):
        #if not self._need in asarray(self._cosa.yo_relleno()): # si no está la necesidad en el objeto, pues cambio de estado, esto es redundante aunque me ha servido para darme cuenta al crear nuevos sims
            #self._humano.set_estado(Esperando(self._humano))
    
        if self._cosa.usar(self._need): # uso la Cosa y relleno la necesidad que necesito
            self._humano.set_estado(Esperando(self._humano))