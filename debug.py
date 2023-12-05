import pygame
import os
import sys

#debug
pygame.init()

# lo encontré por ahí
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
    surf = pygame.display.get_surface()
    # crear texto
    # crear rectangulo
    # blit
    
    
    texto = font.render(f"{info}" , False , color)
    rect = texto.get_rect(center = (x , y))
    
    surf.blit(texto, rect)