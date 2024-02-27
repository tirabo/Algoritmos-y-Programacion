import pygame
from pygame.locals import *
import time
import random


"""
JUEGO DE LA VIDA TOROIDAL(versión nueva)
El juego se desarrolla en un rectángulo WIDTH x HEIGHT donde lo de arriba se continúa con lo de abajo y lo de la izquierda con lo de la derecha 
(es un toro S^1 x S^1 con diámetros WIDTH y HEIGHT respectivamente).
Las reglas son 
1) Cada pixel de tablero es 1 o 0 (negro o blanco). 
2) Hay una cantidad de pixeles inciales que está en 1 (patrón o semilla). 
3) Cada pixel (x,y) tiene 8 vecinos: (x-1,y+1), (x,y+1), (x+1,y+1), (x-1,y), (x+1,y), (x-1,y-1), (x,y-1), (x+1,y-1).
4) En cada paso se cambian los pixeles de 1 a 0 o de 0 a 1 según las siguientes reglas: para obtener el tablero n se usan los valores del tablero n-1 y
      a) Cualquier pixel 1 con dos o tres vecinos vivos sigue siendo 1.
      b) Cualquier pixel 0 con tres vecinos 1 se convierte a 1.
      c) Todas los otros pixeles pasan a 0.

Tutorial sencillo para dibujar con pygame: https://sites.cs.ucsb.edu/~pconrad//cs5nm/topics/pygame/drawing/index.html
Sitio útil (tutorial, ejemplos, etc) para pygame:  http://programarcadegames.com/

Esta versión se implementa con un conjunto que serán los pares ordenados con  las coordenadas de los píxeles vivos
"""


# FUNCIONES

def vecinos(u):
    """
    pre: u es un par ordenado (m,n) con m,n enteros
    post: devuelve el conjunto de vecinos de u 
    """
    (m, n) = u
    return {(m-1,n+1), (m,n+1), (m+1,n+1), (m-1,n), (m+1,n), (m-1,n-1), (m,n-1), (m+1,n-1)}


def vecinos_vivos(tablero, u):
    """
    pre:tablero es el conjunto de pixeles vivos, u es un par ordenado (m,n) con m,n enteros
    post: devuelve el conjunto de vecinos vivos de (m,n)
    """
    (m,n) = u
    return tablero & {(m-1,n+1), (m,n+1), (m+1,n+1), (m-1,n), (m+1,n), (m-1,n-1), (m,n-1), (m+1,n-1)}


def crear_ventana(titulo: str, width = 120, height = 80, e = 10, colors =  ['gray', 'black']):
    """
    pre: titulo: título de la ventana
         width, height: ancho y alto de la ventana (en pixeles)
         e: tamaño del pixel. Un pixel es  e x e  de pygame
         colors: color de fondo y color de dibujo
    """     
    pygame.init()
    screen = pygame.display.set_mode((e*width, e*height)) # crea ventana
    pygame.display.set_caption(titulo)
    screen.fill(colors[0])
    pygame.display.update()
    return screen


def actualizar_tablero(screen, width, height, e, colors, tablero_original, tablero_nuevo):
    """
    pre: screen es la ventana de dibujo, width, height son enteros, e es entero, colors es una lista de dos colores.
         tablero_original es el conjunto de pixeles vivos original, tablero_nuevo es el conjunto de pixeles vivos nuevos
    post:  dibuja los pixeles vivos en una  grilla de (e * width) x (e * height) con colores[0] como fondo y colores[1] como color de dibujo. 
    El (0,0) se ubica en (e * width//2, e * height//2). 
    El (m,n) se ubica en (e * (m + width//2), e * (n + height//2)) y es de tamaño e x e. 
    En  el caso toroidal (m, n) se identifica con (m, n) = (m % width, n % height) y luego se ubica en (e * (x + width//2), e * (y + height//2)) 
    """
    tablero_v = tablero_nuevo - tablero_original # los que nacieron
    tablero_m = tablero_original - tablero_nuevo # los que murieron
    for u in tablero_v:
        (m,n)  = u
        # pygame.draw.rect(screen, colors[1], (e * (m + width//2), e * (n + height//2),e,e), 0) # plano
        pygame.draw.rect(screen, colors[1], (e * ((m + width//2) % width), e * ((n + height//2) % height),e,e),0) # toroidal 
    for u in tablero_m:
        (m,n)  = u
        # pygame.draw.rect(screen, colors[0], (e * (m + width//2), e * (n + height//2),e,e), 0) # plano
        pygame.draw.rect(screen, colors[0], (e * ((m + width//2) % width), e * ((n + height//2) % height),e,e),0) # toroidal 
    pygame.display.update()




def dibujar_grilla(screen, width, height, e):
    # post:  hace le cuadriculado del tablero
    for y in range(height + 1):
        pygame.draw.line(screen, "black", (0, e * y), (e * width, e * y), 1) # Draw a horizontal line
    for x in range(width + 1):
        pygame.draw.line(screen, "black", (e * x, 0), (e * x, e * height), 1) # Draw a horizontal line
    pygame.display.update()

"""
def put_borde_pixel(screen, x, y, clr = 'black'):
    # post: dibuja un cuadradito de la grilla en la posición (x,y) con los bordes de color clr (coordenadas de la grilla, no de pygame)
    pygame.draw.polygon(screen, clr, [(E*x, E*y),(E*x + E, E*y),(E*x + E, E*y + E),(E*x, E*y + E), (E*x, E*y)], 1)
    pygame.display.update()

def put_pixel(screen, width, height, e, colors, tablero, col, u):
    # pre: col = 0 o 1 
    # post: dibuja el pixel u con  color "col"
    x, y = u[0] % width, u[1] % height
    pygame.draw.rect(screen, colors[col], (e*x,e*y,e,e), 0)
"""

def juego_vida(screen, width, height, e, colors, patron):
    """
    pre:  screen es la ventana de dibujo, patron es la lista de los pixeles iniciales
    post: tablero será el conjunto de pixeles vivos
         1) se agrega (x,y) a tablero para cada (x,y) en patron 
         Cada pixel (x,y) tiene 8 vecinos: (x-1,y+1), (x,y+1), (x+1,y+1), (x-1,y), (x+1,y), (x-1,y-1), (x,y-1), (x+1,y-1).
         2) En cada paso se inspeccionan los píxeles que pueden cambiar que son los que están vivos y  sus vecinos. 
         Los pixeles pasa de muerto a vivo (se agregan a tablero) o de vivo a muerto (se saca de tablero) 
         según las siguientes reglas: para obtener el tablero n se usan los valores del tablero n-1 y
            a) Cualquier pixel vivo con dos o tres vecinos vivos sigue vivo (no cambia nada).
            b) Cualquier pixel muerto con tres vecinos vivos se convierte a vivo.
            c) Todas los otros pixeles vivos  que no cumplen a) mueren.
    """
    tablero = set()
    for u in patron:
        tablero = tablero | {u}
    print('Patron:', len(tablero),'vivos')
    print('Comienza el juego')
    pasos = 0
    print('vecinos vivos de (0,0)', len(vecinos_vivos(tablero, (0,0))))
    while True:
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                exit(0) # apretando "x" arriba derecha cierra la ventana
        print('Vivos:',tablero, pasos)
        tablero_orig = tablero.copy()
        print('Vivos 2:',tablero_orig, pasos)
        for u in tablero_orig:
            entorno = vecinos(u) | {u} # u y todos sus vecinos
            # print('entorno de', u, entorno)
            for v in entorno:
                n_vecinos_vivos = len(vecinos_vivos(tablero_orig, v))
                if  v in tablero_orig and not(2 <= n_vecinos_vivos  <= 3):
                    print('muere', v)
                    tablero = tablero - {v}
                elif v not in tablero_orig and n_vecinos_vivos == 3:
                    print('nace', v)
                    tablero = tablero | {v}
        actualizar_tablero(screen, width, height, e, colors, tablero_orig, tablero)
        pasos += 1
        # time.sleep(0.01)


"""
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
"""
def patron_aleatorio(n: int, ancho = 120, alto = 80):
    # post: devuelve una lista de n tuplas (x,y) con 0 <= x < WIDTH y 0 <= y < HEIGHT
    patron = []
    for i in range(n):
        patron.append((random.randint(0,ancho-1), random.randint(0,alto-1)))
    return patron
    

def main():
    titulo = "Juego de la vida"
    width, height, e = 300, 200, 4
    colors =  ['gray', 'black']
    screen = crear_ventana(titulo, width, height, e, colors)
    # dibujar_grilla(screen, width, height, e)

    patron = [(0,0), (2,0),(2,1), (4,2),(4,3),(4,4), (6,3),(6,4),(6,5),(7,4)]
    # patron = [(0,1), (1,2), (2,0), (2,1),(2,2)]
    # patron = [(1,5),(1,6),(2,5),(2,6),(11,5),(11,6),(11,7),(12,4),(12,8),(13,3),(13,9),(14,3),(14,9),(15,6),(16,4),(16,8), (17,5),(17,6),(17,7),(18,6),(21,3),(21,4),(21,5),(22,3),(22,4),(22,5),(23,2),(23,6),(25,1),(25,2),(25,6),(25,7),(35,3),(35,4),(36,3),(36,4)]
    # patron = patron_aleatorio(50,40,20)
    juego_vida(screen, width, height, e, colors, patron)



    return 0

# RUN

if __name__ == '__main__':
    main()