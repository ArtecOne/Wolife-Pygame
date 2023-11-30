import pygame , os , sys , time
import numpy as np
from debug import debug
import settings , data
from new_wosim import Wosim
from new_mapa import Mapa

pygame.init()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

GRUPO_TODOS = pygame.sprite.Group()
GRUPO_COSAS = pygame.sprite.Group()
GRUPO_JUGADOR = pygame.sprite.Group()

class Wolife:
    def __init__(self) -> None:
        self.amplitud : int = settings.ANCHURA_PANTALLA
        self.altura : int = settings.ALTURA_PANTALLA
        self.pantalla = pygame.display.set_mode((self.amplitud , self.altura) , pygame.SCALED  ,  vsync= 1)
        self.titulo = pygame.display.set_caption("Wolife")
        self.reloj = pygame.time.Clock()
        self.frame_anterior = time.time()
        
        self.mapa = Mapa(data.MAPA , self.pantalla)
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
            
            for evento in np.asarray(pygame.event.get()):
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