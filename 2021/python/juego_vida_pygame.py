import pygame
from pygame.locals import *
import time
import random


# JUEGO DE LA VIDA TOROIDAL
# El juego se desrrolla en un rectángulo WIDTH x HEIGHT donde lo de arriba se continúa con lo de abajo y lo de la izquierda con lo de la derecha 
# (es un toro S^1 x S^1 con diámetros WIDTH y HEIGHT respectivamente).
# Las reglas son 
# 1) Cada pixel de tablero es 1 o 0 (negro o blanco). 
# 2) Hay una cantidad de pixeles inciales que está en 1 (patrón o semilla). 
# 3) Cada pixel (x,y) tiene 8 vecinos: (x-1,y+1), (x,y+1), (x+1,y+1), (x-1,y), (x+1,y), (x-1,y-1), (x,y-1), (x+1,y-1).
# 4) En cada paso se cambian los pixeles de 1 a 0 o de 0 a 1 según las siguientes reglas: para obtener el tablero n se usan los valores del tablero n-1 y
#       a) Cualquier pixel 1 con dos o tres vecinos vivos sigue siendo 1.
#       b) Cualquier pixel 0 con tres vecinos 1 se convierte a 1.
#       c) Todas los otros pixeles pasan a 0.

    

# Tutorial sencillo para dibujar con pygame: https://sites.cs.ucsb.edu/~pconrad//cs5nm/topics/pygame/drawing/index.html
# Sitio útil (tutorial, ejemplos, etc) para pygame:  http://programarcadegames.com/

# FUNCIONES

def crear_ventana(titulo: str, width = 120, height = 80, e = 10, colors =  ['gray', 'black']):
    # pre: titulo: título de la ventana
    #      width, height: ancho y alto de la ventana (en pixeles)
    #      e: tamaño del pixel. Un pixel es  e x e  de pygame
    #      colors: color de fondo y color de dibujo
    #      

    global WIDTH, HEIGHT, E, COLORES
    WIDTH, HEIGHT, E, COLORES = width, height, e, colors
    pygame.init()
    screen = pygame.display.set_mode((E*WIDTH, E*HEIGHT)) # crea ventana
    pygame.display.set_caption("Juego de la vida")
    screen.fill(COLORES[0])
    pygame.display.update()
    return screen

def make_tablero():
    # post: Construye un array de WIDTH x HEIGHT con 0 en todas partes y lo devuelve
    tblr = []
    for i in range(WIDTH):
        tblr.append([])
        for j in range(HEIGHT):
            tblr[i].append(0)
    return tblr

def dibujar_grilla(screen):
    # post:  hace le cuadriculado del tablero
    for y in range(HEIGHT + 1):
        pygame.draw.line(screen, "black", (0, E * y), (E * WIDTH, E * y), 1) # Draw a horizontal line
    for x in range(WIDTH + 1):
        pygame.draw.line(screen, "black", (E * x, 0), (E * x, E * HEIGHT), 1) # Draw a horizontal line
    pygame.display.update()

def put_borde_pixel(screen, x, y, clr = 'black'):
    # post: dibuja un cuadradito de la grilla en la posición (x,y) con los bordes de color clr (coordenadas de la grilla, no de pygame)
    pygame.draw.polygon(screen, clr, [(E*x, E*y),(E*x + E, E*y),(E*x + E, E*y + E),(E*x, E*y + E), (E*x, E*y)], 1)
    pygame.display.update()

def put_pixel(tablero, screen, x:int, y:int, col:int):
    # pre: col = 0 o 1 
    # post: dibuja el pixel (x,y) con  color "col", actualiza el array tablero 
    x, y = x % WIDTH, y % HEIGHT
    pygame.draw.rect(screen, COLORES[col], (E*x,E*y,E,E), 0)
    tablero[x][y] = col


def num_vecinos(tablero, x:int, y:int):
    # post: devuelve la cantidad de vecinos de tablero[x][y] que valen 1 (0 <= x < WIDTH, 0 <= y < HEIGHT)
    #       Cada pixel (x,y) tiene 8 vecinos: (x-1,y+1), (x,y+1), (x+1,y+1), (x-1,y), (x+1,y), (x-1,y-1), (x,y-1), (x+1,y-1).
    num_1 = 0
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if tablero[(x + i) % WIDTH][ (y + j) % HEIGHT] == 1:
                num_1 = num_1  + 1
    if tablero[x % WIDTH][y % HEIGHT] == 1:
        num_1 = num_1 - 1
    return num_1

def juego_vida(tablero, screen, patron, grilla = False):
    # pre: tablero es un tablero y patron es la lista de los pixeles iniciales
    # post: cada pixel de tablero es 1 o 0 (1 se dibuja color lapiz, 0 se dibuja color background).
    #      1) se pone 1 en los pixeles de patron
    #      Cada pixel (x,y) tiene 8 vecinos: (x-1,y+1), (x,y+1), (x+1,y+1), (x-1,y), (x+1,y), (x-1,y-1), (x,y-1), (x+1,y-1).
    #      2) En cada paso se cambian los pixeles de 1 a 0 o de 0 a 1 según las siguientes reglas: para obtener el tablero n se usan los valores del tablero n-1 y
    #         a) Cualquier pixel 1 con dos o tres vecinos vivos sigue siendo 1.
    #         b) Cualquier pixel 0 con tres vecinos 1 se convierte a 1.
    #         c) Todas los otros pixeles pasan a 0.
    if grilla:
        print("Dibujamos la grilla")
        dibujar_grilla(screen)
    print('Dibujamos patron')
    for u in patron:
        put_pixel(tablero, screen, u[0] + WIDTH//2,u[1] + HEIGHT//2, 1)
        # put_pixel(tablero, screen, u[0],u[1])
    pygame.display.update()
    
    tablero_orig = []
    for i in range(WIDTH):
        tablero_orig.append([])
        for j in range(HEIGHT):
            tablero_orig[i].append(0)
    time.sleep(2)

    print('Comienza el juego')
    while True:
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                exit(0) # apretando "x" arriba derecha cierra la ventana
        for i in range(WIDTH):
            for j in range(HEIGHT):
                tablero_orig[i][j] = tablero[i][j]
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if tablero_orig[i][j] == 1 and (num_vecinos(tablero_orig,i,j) == 2 or num_vecinos(tablero_orig,i,j) == 3):
                    pass
                elif tablero_orig[i][j] == 0 and num_vecinos(tablero_orig,i,j) == 3:
                    put_pixel(tablero, screen, i, j, 1)
                else:
                    if tablero_orig[i][j] == 1:
                        put_pixel(tablero,screen, i, j, 0)
                        if grilla:
                            put_borde_pixel(screen,i, j)
        pygame.display.update()
        # time.sleep(0.1)
    

def main():
    screen = crear_ventana("Juego de la vida")
    tablero = make_tablero()
    patron = [(0,0), (2,0),(2,1), (4,2),(4,3),(4,4), (6,3),(6,4),(6,5),(7,4)]
    # patron = [(0,1), (1,2), (2,0), (2,1),(2,2)]
    # patron = [(1,5),(1,6),(2,5),(2,6),(11,5),(11,6),(11,7),(12,4),(12,8),(13,3),(13,9),(14,3),(14,9),(15,6),(16,4),(16,8), (17,5),(17,6),(17,7),(18,6),(21,3),(21,4),(21,5),(22,3),(22,4),(22,5),(23,2),(23,6),(25,1),(25,2),(25,6),(25,7),(35,3),(35,4),(36,3),(36,4)]
    juego_vida(tablero, screen, patron)
    return 0

# RUN

if __name__ == '__main__':
    main()