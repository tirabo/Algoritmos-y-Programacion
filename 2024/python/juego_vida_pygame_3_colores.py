import pygame
from pygame.locals import *
import time
import random

# JUEGO DE LA VIDA TOROIDAL
# El juego se desarrolla en un rectángulo WIDTH x HEIGHT donde lo de arriba se continúa con lo de abajo y lo de la izquierda con lo de la derecha 
# (es un toro S^1 x S^1 con diámetros WIDTH y HEIGHT respectivamente).
# Las reglas son 
# 1) Cada pixel de tablero es 1 o 0 (negro o blanco). 
# 2) Hay una cantidad de pixeles inciales que está en 1 (patrón o semilla). 
# 3) Cada pixel (x,y) tiene 8 vecinos: (x-1,y+1), (x,y+1), (x+1,y+1), (x-1,y), (x+1,y), (x-1,y-1), (x,y-1), (x+1,y-1).
# 4) En cada paso se cambian los pixeles de 1 a 0 o de 0 a 1 según las siguientes reglas: para obtener el tablero n se usan los valores del tablero n-1 y
#      a) Cualquier pixel 1 con menos de dos vecinos 1 pasa a 0.
#      b) Cualquier pixel 1 con dos o tres vecinos 1 queda igual.
#      c) Cualquier pixel 1 con más de tres vecinos 1 muere.
#      d) Cualquier pixel 0 con exactamente tres vecinos 1 se convierte en una pixel 1.
#
# En  este archoivo se modifican algunas reglas agregando probabilidad. 

# Tutorial sencillo para dibujar: https://sites.cs.ucsb.edu/~pconrad//cs5nm/topics/pygame/drawing/index.html
# Sitio útil (tutorial, ejemplos, etc) para pygame:  http://programarcadegames.com/


# CONSTANTES

WIDTH = 120
HEIGHT = 80
E = 10 # E es la escala, la pantalla se dibuja de WIDTH * E x HEIGHT * E
colores = {0:'white',1:'black',2:'red'}

# FUNCIONES

def make_tablero():
    # post: Construye un array de WIDTH x HEIGHT con 0 en todas partes y lo devuelve
    tblr = []
    for i in range(WIDTH):
        tblr.append([])
        for j in range(HEIGHT):
            tblr[i].append(0)
    return tblr

def put_pixel(tablero, screen, x:int, y:int, color:int):
    # pre: tablero es el tablero creado por  make_tablero(), screen es la ventana (0 <= x < WIDTH, 0 <= y < HEGHT)
    # post: dibuja el pixel (x,y), actualiza el array tablero 
    x, y = x % WIDTH, y % HEIGHT
    pygame.draw.rect(screen, colores[color], (E*x,E*y,E,E), 0)
    tablero[x][y] = color

def num_vecinos(tablero, x:int, y:int):
    # post: devuelve la cantidad de vecinos de tablero[x][y] que valen 1 (0 <= x < WIDTH, 0 <= y < HEGHT)
    #       Cada pixel (x,y) tiene 8 vecinos: (x-1,y+1), (x,y+1), (x+1,y+1), (x-1,y), (x+1,y), (x-1,y-1), (x,y-1), (x+1,y-1).
    num_1 = 0
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if tablero[(x + i) % WIDTH][ (y + j) % HEIGHT] > 0:
                num_1 = num_1  + 1
    if tablero[x % WIDTH][y % HEIGHT] > 0:
        num_1 = num_1 - 1
    return num_1

def juego_vida(tablero, screen, patron):
    # pre: tablero es un tablero y patron es la lista de los pixeles iniciales en 1
    # post: cada pixel de tablero es 2, 1 o 0 (2 rojo, 1 negro, 0 blanco). 2 y 1 son vivos, 0 es no vida
    #      1) se pone 1 y 2 en los pixeles de patron. 
    #      Cada pixel (x,y) tiene 8 vecinos: (x-1,y+1), (x,y+1), (x+1,y+1), (x-1,y), (x+1,y), (x-1,y-1), (x,y-1), (x+1,y-1).
    #      2)  Las reglas para didujar (o borrar) pixeles son: se hace un recorrido por todos los pixeles y
    #           - Cualquier pixel vivo con 0 vecinos vivos pasa a 0.
    #           - Cualquier pixel 1 con 1 vecino vivo pasa a 0.
    #           - Cualquier pixel 2 con 1 vecino vivo queda igual.
    #           - Cualquier pixel vivo con dos vecinos vivos queda igual.
    #           - Cualquier pixel vivo con tres vecinos vivos pasa a pixel 2
    #           - Cualquier pixel vivo con más de tres vecinos vivos muere.
    #           - Cualquier pixel 0 con exactamente tres vecinos vivos se convierte en una pixel 1.
    #
    #         e) Cualquier  
    
    print('Dibujamos patron')
    for u in patron:
        put_pixel(tablero, screen, u[0] + WIDTH//2,u[1] + HEIGHT//2,1)
    
    t_ini = time.time()
    while time.time() - t_ini < 3: # 3 segundos muestra el patron
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                exit(0) # apretando "x" arriba drecha cierra la ventana
        pygame.display.update()
    
    tablero_orig = []
    for i in range(WIDTH):
        tablero_orig.append([])
        for j in range(HEIGHT):
            tablero_orig[i].append(0)
    

    print('Comienza el juego')
    while True:
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                exit(0) # apretando "x" arriba drecha cierra la ventana
        for i in range(WIDTH):
            for j in range(HEIGHT):
                 tablero_orig[i][j] = tablero[i][j]
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if (tablero_orig[i][j] == 1 or tablero_orig[i][j] == 2) and num_vecinos(tablero_orig,i,j) == 0:
                    if random.randrange(100) > -1: # -1 - Cualquier pixel vivo con 0 vecinos vivos pasa a 0.
                        put_pixel(tablero, screen, i, j, 0)
                elif tablero_orig[i][j] == 1 and num_vecinos(tablero_orig,i,j) == 1:
                    if random.randrange(100) > -1: # -1 - Cualquier pixel 1 con 1 vecino vivo pasa a 0.
                        put_pixel(tablero, screen, i, j, 0)
                elif tablero_orig[i][j] == 2 and num_vecinos(tablero_orig,i,j) == 1:
                    if random.randrange(100) > 1: # -1  - Cualquier pixel 2 con 1 vecino vivo queda igual.
                        put_pixel(tablero, screen, i, j, 0)
                elif  (tablero_orig[i][j] == 1 or tablero_orig[i][j] == 2) and num_vecinos(tablero_orig,i,j) == 2:
                    if random.randrange(100) > 100: # 100 - Cualquier pixel vivo con dos vecinos vivos queda igual.
                        put_pixel(tablero, screen, i, j, 0)
                elif  (tablero_orig[i][j] == 1 or tablero_orig[i][j] == 2) and num_vecinos(tablero_orig,i,j) == 3:
                    if random.randrange(100) > -1: # -1  - Cualquier pixel vivo con tres vecinos vivos pasa a pixel 2
                        put_pixel(tablero, screen, i, j, 2)
                elif (tablero_orig[i][j] == 1 or tablero_orig[i][j] == 2) and num_vecinos(tablero_orig,i,j) > 3:
                    if random.randrange(100) > -1: # -1 - Cualquier pixel vivo con más de tres vecinos vivos muere.
                        put_pixel(tablero, screen, i, j, 0)
                elif tablero_orig[i][j] == 0 and num_vecinos(tablero_orig,i,j) == 3:
                    if random.randrange(100) > -1: # -1 - Cualquier pixel 0 con exactamente tres vecinos vivos se convierte en una pixel 1.
                        put_pixel(tablero, screen, i, j, 1)
        pygame.display.update()
        #time.sleep(1)
    

def main():
    pygame.init()
    screen = pygame.display.set_mode((E*WIDTH, E*HEIGHT)) # crea ventana
    pygame.display.set_caption("Juego de la vida")
    screen.fill(colores[0])
    pygame.display.update()
    tablero = make_tablero()
    # pygame.draw.rect(screen, color, (x,y,width,height), thickness)
    patron = [(0,0), (2,0),(2,1), (4,2),(4,3),(4,4), (6,3),(6,4),(6,5),(7,4)]
    # patron = [(0,1), (1,2), (2,0), (2,1),(2,2)]
    # patron = [(1,5),(1,6),(2,5),(2,6),(11,5),(11,6),(11,7),(12,4),(12,8),(13,3),(13,9),(14,3),(14,9),(15,6),(16,4),(16,8), (17,5),(17,6),(17,7),(18,6),(21,3),(21,4),(21,5),(22,3),(22,4),(22,5),(23,2),(23,6),(25,1),(25,2),(25,6),(25,7),(35,3),(35,4),(36,3),(36,4)]

    juego_vida(tablero, screen, patron)
    """
    while True:
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                exit(0) # apretando "x" arriba drecha cierra la ventana
    """
    return 0

# RUN
 
if __name__ == '__main__':
    main()