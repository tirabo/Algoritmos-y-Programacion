import pygame
from pygame.locals import *


screen = pygame.display.set_mode((400, 500)) # crea ventana
pygame.display.set_caption("")
pygame.display.update()
while True:
    for eventos in pygame.event.get():
        if eventos.type == QUIT:
            exit(0) # apretando "x" arriba derecha cierra la ventana
    pygame.display.update()

