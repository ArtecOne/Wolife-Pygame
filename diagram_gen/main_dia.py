import pygame, os , sys ,  time , csv
from numpy import asarray , arange , random
from csv import reader
from pathfinding.core.grid import Grid
from pathfinding.finder.bi_a_star import BiAStarFinder as BiAstar
from abc import ABC , abstractmethod

pygame.init()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

font = pygame.font.Font(resource_path("assets/fuentes/pixeled_font.ttf") , 15)
def debug(info , x = 10 , y = 10 , color = "black"):
    surf : pygame.Surface = pygame.display.get_surface()
    # crear texto
    # crear rectangulo
    # blit
    
    
    texto : pygame.surface.Surface= font.render(f"{info}" , False , color)
    rect : pygame.Rect = texto.get_rect(center = (x , y))
    
    surf.blit(texto, rect)

VERTICAL_TILE_NUMBER : int = 20
HORIZONTAL_TILE_NUMBER : int = 20
TILE_SIZE : int = 32

ALTURA_PANTALLA : int = VERTICAL_TILE_NUMBER * TILE_SIZE
ANCHURA_PANTALLA : int = HORIZONTAL_TILE_NUMBER * TILE_SIZE

MAPA : dict = {
    "suelo" : resource_path("assets/tmx/casa_vacia_suelo.csv") ,
    "muros" : resource_path("assets/tmx/casa_vacia_muros.csv") ,
    "sprites" : resource_path("assets/img/tiles/Room_Builder_free_32x32.png")
}

MAPA_MATRIX : list[list] = asarray([[50,290,290,290,290,290,290,290,290,15,290,290,290,290,290,290,290,290,290,14],
               [32,307,307,307,307,307,307,307,307,32,307,307,307,307,307,307,307,307,307,32],
               [32,-1,-1,-1,-1,-1,-1,-1,-1,32,-1,-1,-1,-1,-1,-1,-1,-1,-1,                 32],
               [32,-1,-1,-1,-1,-1,-1,-1,-1,32,-1,-1,-1,-1,-1,-1,-1,-1,-1,                 32],
               [32,-1,-1,-1,-1,-1,-1,-1,-1,32,-1,-1,-1,-1,-1,-1,-1,-1,-1,                 32],
               [32,-1,-1,-1,-1,-1,-1,-1,-1,32,-1,-1,-1,-1,-1,-1,-1,-1,-1,                 32],
               [32,-1,-1,-1,16,290,290,290,290,297,290,290,290,290,290,291,-1,-1,-1,      32],
               [32,-1,-1,-1,32,314,314,314,314,314,314,314,314,314,314,315,-1,-1,-1,      32],
               [32,-1,-1,-1,32,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,                 32],
               [32,-1,-1,-1,32,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,                 32],
               [32,-1,-1,-1,32,-1,-1,-1,-1,-1,-1,-1,-1,16,290,290,290,290,290,            32],
               [32,-1,-1,-1,32,-1,-1,-1,-1,-1,-1,-1,-1,32,307,307,307,307,307,            32],
               [32,-1,-1,-1,292,-1,-1,-1,-1,-1,-1,-1,-1,292,-1,-1,-1,-1,-1,               32],
               [32,-1,-1,-1,309,-1,-1,-1,-1,-1,-1,-1,-1,309,-1,-1,-1,-1,-1,               32],
               [32,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,                 32],
               [32,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,                 32],
               [296,290,290,290,290,290,290,30,-1,-1,-1,-1,28,290,290,290,290,290,290,   298],
               [306,307,307,307,307,307,307,47,-1,-1,-1,-1,45,307,307,307,307,307,307,   308],
               [-1,-1,-1,-1,-1,-1,-1,47,-1,-1,-1,-1,45,-1,-1,-1,-1,-1,-1,                 -1],
               [-1,-1,-1,-1,-1,-1,-1,289,291,-1,-1,289,291,-1,-1,-1,-1,-1,-1,             -1]])

def import_csv_layout(path : str):
    
    mapa_suelo : list = []
    
    with open(path) as map:
        mapa = reader(map , delimiter= ",")
        
        for fila in mapa:
            mapa_suelo.append(list(fila))
    
    return mapa_suelo

def import_graficos(path : str):
        surface : pygame.Surface = pygame.image.load(path).convert_alpha()
        
        tile_num_x : int = surface.get_width() // TILE_SIZE
        tile_num_y : int = surface.get_height() // TILE_SIZE
        
        tiles_cortados : list = []
        
        for fila in arange(tile_num_y):
            for columna in arange(tile_num_x):
                x : int = columna * TILE_SIZE
                y : int = fila * TILE_SIZE
                
                nueva_surf : pygame.Surface = pygame.Surface((TILE_SIZE , TILE_SIZE)).convert_alpha()
                nueva_surf.blit(surface , (0 , 0) , pygame.Rect(x , y , TILE_SIZE , TILE_SIZE))
                nueva_surf.set_colorkey((0 , 0 , 0) , pygame.BLEND_RGB_MULT)
                tiles_cortados.append(nueva_surf)
                
        return tiles_cortados

class Cosa(pygame.sprite.Sprite):
    def __init__(self , necesidades : list , puntos : int, imagen : str):
        """
        Clase superior de todas las cosas, metodos generales se encuentran aquí,
        como el usar ; yo_relleno ; crearse
        """
        super().__init__()
        
        for need in asarray(necesidades):
            need.añadir_cosas(self)
        
        self._necesidades : list = necesidades
        
        self._pts : int = puntos
        
        self.image : pygame.Surface = pygame.image.load(resource_path(imagen)).convert_alpha()
        self.rect : pygame.Rect = self.image.get_rect(center = self.crearse())
    
    def crearse(self):
        seleccion_x : int = random.randint(0 , ANCHURA_PANTALLA) // TILE_SIZE 
        seleccion_y : int = random.randint(0 , ALTURA_PANTALLA) // TILE_SIZE
        
        if MAPA_MATRIX[seleccion_y][seleccion_x] != -1:
            return self.crearse()
        
        return (seleccion_x * TILE_SIZE , seleccion_y * TILE_SIZE)
    
    def yo_relleno(self):
        return self._necesidades
    
    def usar(self , necesidad_a_rellenar : "Necesidad"):
        
        return necesidad_a_rellenar.aumentar(self._pts) # debido a que hay varios personajes, debo pasarle a la cosa la necesidad a Aumentar, de igual forma compruebo ante si existe en este objeto
        
class Cama(Cosa):
    def __init__(self , necesidad : list , puntos : int , imagen : str):
        super().__init__([need for need in asarray(necesidad) if need.nombre == "sueño"] , puntos , imagen)
        
    def hacer_noche(self):
        """
        funcion especializada de ejemplo para la cama
        """ 
        pass
    
class Estanteria(Cosa):
    def __init__(self , necesidad : list , puntos : int , imagen : str):
        super().__init__([need for need in asarray(necesidad) if need.nombre == "diversion"] , puntos , imagen)
    
    def aprender(self):
        """
        funcion especializada de ejemplo para la estanteria
        """
        pass

class Habitacion:
    def __init__(self) -> None:
        pass
    
    def crear_cocina(self ,necesidad : list , puntos : int , imagen : str):
        return Cocina(necesidad , puntos , imagen)
    
    def crear_baño(self , necesidad : list , puntos : int , imagen : str):
        return Bano(necesidad , puntos , imagen)

class Cocina:
    def __init__(self , necesidad : list , puntos : int , imagen : str):
        """
        Esta es una clase que devuelve el objeto que quiero de la zona Cocina
        """
        
        self._necesidad : list = [need for need in asarray(necesidad) if need.nombre == "hambre"]
        self._puntos : int = puntos
        self._imagen : int = imagen
    
    def crear_horno(self):
        return Horno(self._necesidad , self._puntos , self._imagen)
        
class Bano:
    def __init__(self , necesidad : list , puntos : int , imagen : str):
        """
        Esta es una clase que devuelve un objeto que quiero de la zona Baño
        """
    
        self._necesidad : int = [need for need in asarray(necesidad) if need.nombre == "higiene"]
        self._puntos : int = puntos
        self._imagen : int = imagen
    
    def crear_bañera(self):
        return Banera(self._necesidad , self._puntos , self._imagen)

class Horno(Cosa):
    def __init__(self ,necesidad : list , puntos : int , imagen : str):
        super().__init__(necesidad , puntos , imagen)
       
class Banera(Cosa):
    def __init__(self , necesidad : list , puntos : int , imagen : str):
        super().__init__(necesidad , puntos , imagen)

class Tile(pygame.sprite.Sprite):
    """
    Un Tile es una cuadrilla del mapa, esta clase sirve para instaciar objetos Cuadrilla
    con esto creo los suelos y los muros por capas
    """
    
    def __init__(self  , x : int, y : int , superficie : pygame.Surface):
        super().__init__()
        
        self.image : pygame.Surface = superficie
        self.rect : pygame.Rect = self.image.get_rect(topleft = (x , y))
    

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
        
        self._pantalla : pygame.Surface = superficie
        self._data : dict = data
        
        self._lista_terrenos : list = import_graficos(self._data["sprites"])
        
        # suelo
        self._suelo : pygame.sprite.Group = self.crear_grupo_tiles(import_csv_layout(self._data["suelo"]))
        
        # paredes
        self._paredes : pygame.sprite.Group = self.crear_grupo_tiles(import_csv_layout(self._data["muros"]))
    
    def crear_cosas(self , grupos_a_pertenecer : list , necesidades : list):
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
        xx = x * TILE_SIZE
        yy = y * TILE_SIZE
        
        
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

class Necesidad:
    def __init__(self , nombre : str , velocidad_degrade : "function" , prioridad : int , pos_ui : tuple):
        """
        Clase necesidad, obtiene:
        
        nombre que es usado para asignar correctamente la necesidad a una cosa
        
        una velocidad de degrade que es una funcion (en mi caso, la hice de valores aleatorios)
        
        obtiene un nivel de prioridad para aumentar la atención del Wosim sobre el nivel de necesidad
        
        Por ultimo la posicion de la UI
        """
        
        self._nombre : str = nombre
        self._puntos : int = 25
        self._tiempo : function = velocidad_degrade
        self._multiplicador_prioridad : int = prioridad
        self._prioridad : int = 0
        
        self._sprite : function = lambda i: pygame.image.load(resource_path(f"assets/img/UI/indicador ({i}).png"))
        self.image : pygame.Surface = self._sprite(25)
        self.rect : pygame.Rect = self.image.get_rect(center = pos_ui)
        
        self._cosas_que_aumentan_esto : list = []
        
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
        
        self._estado = None # cerebro
        
        self.set_estado(Esperando())
        
        self._grupo_todos : pygame.sprite.Group = grupos[1] # GRUPO_TODOS , en i = 0 está GRUPO_JUGADOR
        
        self._inicio_x = self._pantalla.get_width()//2 // 32
        self._inicio_y = self._pantalla.get_height()//2 // 32
        
        self.image = pygame.image.load(resource_path("assets/img/player/idle.png")).convert_alpha()
        self.rect = self.image.get_rect(center = (self._inicio_x * 32 , self._inicio_y * 32)) # RECT es una propiedad de pygame.Sprite al igual que IMAGE
        
        self._objetivo = pygame.image.load(resource_path("assets/img/UI/selection.png")).convert_alpha()
        self._objetivo_rect = pygame.Rect(self.rect.topleft, (TILE_SIZE , TILE_SIZE))

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
        self._estado.humano = self
        self._estado.init()
    
    def decrementar_necesidades(self):
        [need.decrecer() for need in asarray(self._necesidades)] # jugador.decrementar_necesidades()  sujeto y predicado
    
    def update(self , delta): # metodo polimorfico de todos los sprites, el grupo al cual pertenece llama este metodo para todos sus sprites
        self._estado.main(delta)
        
        for need in asarray(self._necesidades):
            self._pantalla.blit(*need.mostrar_UI())
        
        self._pantalla.blit(self._objetivo , self._objetivo_rect)
        
        debug(f"Nombre {self._nombre} , hambre {int(self._necesidades[0].prioridad)} , higiene {int(self._necesidades[1].prioridad)} , energia {int(self._necesidades[2].prioridad)} , diversion {int(self._necesidades[3].prioridad)}" , self._pantalla.get_width()//2 - 80, self.yy + 10)

class Estado(ABC):
    @property
    def humano(self) -> Wosim:
        return self._humano
    
    @humano.setter
    def humano(self , humano : Wosim) -> None:
        self._humano = humano
    
    @property
    def pantalla(self) -> Wosim:
        self._pantalla = pygame.display.get_surface()
        return self._pantalla
    
    def init(self) -> None:
        pass
    
    @abstractmethod
    def set_imagen(self) -> None:
        pass
        
    @abstractmethod
    def main(self , delta) -> None:
        """Metodo unicamente existente para ser sobreescrito.
        Este metodo debe incorporar o agrupar la funcionalidad del Estado
        """
        pass
    
class Esperando(Estado):
    def __init__(self):
        self.imagen_def = pygame.image.load(resource_path("assets/img/player/idle.png")).convert_alpha() # image es una propieda de pygame.Sprite
        
        self._donde_ir = 0 # esto se convierte en una Cosa
        
        self._seleccion_x = 0
        self.seleccion_y = 0
        
        self._need = 0
    
    def set_imagen(self):
        self.humano.image = self.imagen_def # image es una propieda de pygame.Sprite
    
    def priorizar(self):
        necesidades = sorted(self.humano.necesidades , key= lambda nece: nece.prioridad , reverse= True) # ordeno una lista de necesidades en base a su prioridad
        return necesidades[random.randint(2)]
    
    def asignar_need_y_donde_ir(self, necesidad):
        self._need = necesidad
            
        self._donde_ir = self._need.seleccionar_una_cosa() # aquí selecciono random una Cosa que satisfazca la necesidad
                
        self.seleccion_x = self._donde_ir.rect.centerx // TILE_SIZE # Obtengo la posicion de la cosa para posicionar mi rectangulo Objetivo
        self.seleccion_y = self._donde_ir.rect.centery // TILE_SIZE
    
    def buscar(self):
        necesidad = self.priorizar()
        
        if necesidad.cuantos_puntos() < random.randint(10 , 21): # La personaje elige aleatoriamente cuando es necesario ir a satisfacerse
            self.asignar_need_y_donde_ir(necesidad)
        
        
        
    def main(self , delta = None):
        self.set_imagen()
        
        self.buscar()
        
        if self._donde_ir: # si hay donde ir, pues posiciono mi rectangulo objetivo y paso al siguiente estado
            self.humano.rectangulo_objetivo.topleft = (self.seleccion_x * TILE_SIZE, self.seleccion_y * TILE_SIZE)
            
            self.humano.set_estado(Movimiento((self.humano.rectangulo_objetivo.centerx // TILE_SIZE, self.humano.rectangulo_objetivo.centery // TILE_SIZE),
                                               self._donde_ir , self._need))
            
class Movimiento(Estado):
    def __init__(self , destino : tuple, cosa_donde_ir : object , necesidad) -> None:
        """
        Esta clase se encarga de apuntar y mover al personaje
        
        crea un grafo apartir de una matriz
        crea nodos
        
        crea un camino, puntos de recta, colisiones para que el personaje siga esos puntos
        
        al final, cometemos la transicion pasando los datos necesarios para el siguiente estado
        """
        self._cosa = cosa_donde_ir # la cosa que voy a usar
        self._need = necesidad # la necesidad que debo satisfacer
        self._direccion = pygame.math.Vector2(0 , 0)    
        
        self._destino = destino
        
        self._path =  []
        self._puntos = []
        self._colisiones = []
        
        self._index = 1
        self._sprite = lambda i , image: pygame.image.load(resource_path(image.format(int(i)))).convert_alpha()
        
        
    
    def init(self):
        self._pos = self.humano.rect.center # obtengo la posicion actual de mi personaje
        
        self._inicio = (self.humano.rect.centerx // TILE_SIZE , self.humano.rect.centery // TILE_SIZE)
        # convierto la posicion actual de mi personaje a tamaño cuadricula para poder crear nodo en el grafo
        
        self._grafo = Grid(matrix= MAPA_MATRIX , inverse= True)
        # inverso ya que la matriz es la capa de muros, -1 es el suelo
        
        self._nodo_inicio = self._grafo.node(*self._inicio)
        self._nodo_final = self._grafo.node(*self._destino)
        
        self.crear_camino()
        
    def set_imagen(self , photo) -> None:
        self.humano.image = self._sprite(self._index , photo)
    
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
            
        inicio = pygame.math.Vector2(self.humano.rect.center)
        
        final = pygame.math.Vector2(self._colisiones[0].center)
        
        self._direccion = (final - inicio).normalize() # crea la direccion en x & y donde se moverá el personaje
        
        self._pos += self._direccion * 100 * delta # velocidad jugador
        self.humano.rect.center = self._pos # asignacion de posicion
        
        
        for rect in self._colisiones:
            if rect.collidepoint(self._pos):
                del self._colisiones[0] # cuando colisiona se elimina provocando que tenga que trackear la siguiente colision
        
        if not self._colisiones:
            return
        
        if self._colisiones[0].centery > self.humano.rect.centery: 
            self.set_imagen("assets/img/player/front_run ({}).png")
        
        elif  self._colisiones[0].centery < self.humano.rect.centery:
            self.set_imagen("assets/img/player/back_run ({}).png")
            
        elif  self._colisiones[0].centerx > self.humano.rect.centerx:
            self.set_imagen("assets/img/player/der_run ({}).png")
            
        elif  self._colisiones[0].centerx < self.humano.rect.centerx:
            self.set_imagen("assets/img/player/izq_run ({}).png")
        
        
    def main(self, delta = None):
        if self._index == 1:
            self.set_imagen("assets/img/player/front_run ({}).png")
        
        self.ir(delta)
        
        if not self._puntos: # si aun no he creado puntos, pues no sigo avanzando
            return
        
        if not self._colisiones: # cuando no hay más puntos significa que llegué al final
            self.humano.set_estado(Satisfaciendo(self._cosa , self._need))
            
            
class Satisfaciendo(Estado):
    def __init__(self , cosa , necesidad) -> None:
        self._cosa = cosa
        
        self._need = necesidad
        
        self.imagen_def = pygame.image.load(resource_path("assets/img/player/idle.png")).convert_alpha()

    def set_imagen(self) -> None:
        self.humano.image = self.imagen_def
     
    def main(self , delta = None):
        #if not self._need in asarray(self._cosa.yo_relleno()): # si no está la necesidad en el objeto, pues cambio de estado, esto es redundante aunque me ha servido para darme cuenta al crear nuevos sims
            #self._humano.set_estado(Esperando(self._humano))

        self.set_imagen()
        
        if self._cosa.usar(self._need): # uso la Cosa y relleno la necesidad que necesito
            self.humano.set_estado(Esperando())

GRUPO_TODOS = pygame.sprite.Group()
GRUPO_COSAS = pygame.sprite.Group()
GRUPO_JUGADOR = pygame.sprite.Group()

class Wolife:
    def __init__(self) -> None:
        self.amplitud : int = ANCHURA_PANTALLA
        self.altura : int = ALTURA_PANTALLA
        self.pantalla = pygame.display.set_mode((self.amplitud , self.altura) , pygame.SCALED  ,  vsync= 1)
        self.titulo = pygame.display.set_caption("Wolife")
        self.reloj = pygame.time.Clock()
        self.frame_anterior = time.time()
        
        self.mapa = Mapa(MAPA , self.pantalla)
        self.jugador = Wosim("Jose" , [GRUPO_JUGADOR , GRUPO_TODOS] , (130 , 20))
        self.jugador2 = Wosim("Alfa" , [GRUPO_JUGADOR , GRUPO_TODOS] , (130 , 50))
        
        self.mapa.crear_cosas([GRUPO_COSAS , GRUPO_TODOS] , self.jugador.necesidades + self.jugador2.necesidades) # grupos y una lista con la totalidad de necesidades a asignar a cada Cosa
        
        self.timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer , 1000)
        
    def iniciar(self):
        global DELTATIME
        
        while True: 
            DELTATIME = time.time() - self.frame_anterior
            self.frame_anterior = time.time()
            
            teclas = pygame.key.get_pressed()
            
            for evento in asarray(pygame.event.get()):
                if evento.type == pygame.QUIT or teclas[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
                if evento.type == self.timer:
                    self.jugador.decrementar_necesidades()
                    self.jugador2.decrementar_necesidades()
                    
                    
            self.pantalla.fill("blue")
            self.mapa.mostrar()
            GRUPO_TODOS.draw(self.pantalla)
            GRUPO_JUGADOR.update(DELTATIME)
            
            debug(int(self.reloj.get_fps()) , 20 , color= "black")
            self.reloj.tick(120)
            pygame.display.update()
            
            
juego = Wolife()
juego.iniciar()