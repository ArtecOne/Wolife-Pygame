import pygame , os , sys , time
import numpy as np
from debug import debug
import settings , data
from new_wosim import Wosim
from new_mapa import Mapa, HIGIENE , DIVERSION , ENERGIA , HAMBRE

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
GRUPO_JUGADOR = pygame.sprite.GroupSingle()

class Wolife:
    def __init__(self) -> None:
        self.amplitud : int = settings.ANCHURA_PANTALLA
        self.altura : int = settings.ALTURA_PANTALLA
        self.pantalla = pygame.display.set_mode((self.amplitud , self.altura) , pygame.SCALED  ,  vsync= 1)
        self.titulo = pygame.display.set_caption("Wolife")
        self.reloj = pygame.time.Clock()
        self.frame_anterior = time.time()
        
        self.mapa = Mapa(data.MAPA , self.pantalla, GRUPO_COSAS , GRUPO_TODOS)
        self.jugador = Wosim([GRUPO_JUGADOR , GRUPO_TODOS])
        
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
                    HIGIENE.puntos += -np.random.random()
                    DIVERSION.puntos += -np.random.random() 
                    ENERGIA.puntos += 1/2 * -np.random.random()
                    HAMBRE.puntos += 2 * -np.random.random()
                    
                    
            self.pantalla.fill("blue")
            self.mapa.mostrar()
            GRUPO_TODOS.draw(self.pantalla)
            GRUPO_TODOS.update(DELTATIME)
            
            debug(int(self.reloj.get_fps()) , 20 , color= "black")
            self.reloj.tick(120)
            pygame.display.update()
            
            
juego = Wolife()
juego.iniciar()