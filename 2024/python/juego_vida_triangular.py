import pygame
from pygame.locals import *
import time
import random

"""
JUEGO DE LA VIDA TRIANGULAR PLANO
- Ver https://wpmedia.wolfram.com/sites/13/2018/02/08-2-4.pdf
- Ver https://es.wikipedia.org/wiki/Juego_de_la_vida
En  este caso el espacio está dividido en triángulos equiláteros y cada triángulo tiene 12 vecinos, 3 por los lados 
y 9 por los vértices.
- Reglas.Una regla LFR se escribe ElEhFlFh, donde ElEh (la regla del "entorno") da los límites inferior y superior para el recuento de vecinos vivos de una célula C actualmente viva para que C permanezca viva, y FlFh (la regla de la "fertilidad") da los límites inferior y superior para el recuento de vecinos vivos necesarios para que una célula actualmente muerta vuelva a la vida.
Es decir, 
    - si C == 1, es una célula viva y vecinos es la cantidad de vecinos vivos, entonces C permanece viva si El <= vecinos <= Eh. En  caso contrario C = 0 (pasa a estar muerta)
    - Si C == 0 es una célula muerta y vecinos es la cantidad de vecinos vivos, entonces C = 1 (pasa a ser viva) si  Fl <= vecinos <= Fh.
    Por ejemplo, si El = 2, Eh = 3, Fl = 3, Fh = 3, entonces la regla Se denota "Life 2333" y es la regla del juego de la vida de Conway (en una grilla cuadrada).
    Cada regla LFR se implementará con una 4-tupla de números enteros: LFR = (El, Eh, Fl, Fh)
- Grilla: las grilla en principio es infinita y la pensamos como Z x Z (reticulado de enteros). Cada par (m,n) de la grilla será considerado  como el triángulo equilátero con centro en (m,n). Hoy  dos tipos de triángulos los tipo "E" y los tipo "O". Los tipo "E" son los que apuntan hacia arriba y los tipo "O" son los que apuntan hacia abajo. En (0,0) ponemos un triángulo tipo "E" y  completamos. 
Los triángulos de tipo "E" son los que tienen centro en (m,n) con m + n par y los de tipo "O" son los que tienen centro en (m,n) con m + n impar.
Si un triangulo es de tipo "E" y tiene centro en (m,n) entonces sus vecinos son
    * Arriba: (m-1,n+1), (m,n+1), (m+1,n+1)
    * Izquierda: (m-2,n), (m-1,n)
    * Derecha: (m+1,n), (m+2,n)
    * Abajo: (m-2,n-1), (m-1,n-1), (m,n-1), (m+1,n-1), (m+2,n-1)  
Si un triangulo es de tipo "O" y tiene centro en (m,n) entonces sus vecinos son
    * Arriba: (m-2,n+1), (m-1,n+1), (m,n+1), (m+1,n+1), (m+2,n+1)
    * Izquierda: (m-1,n), (m-2,n)
    * Derecha: (m+1,n), (m+2,n)
    * Abajo: (m-1,n-1), (m,n-1), (m+1,n-1)
    
"""


# CONSTANTES

WIDTH = 100
HEIGHT = 100
E = 10 # E es la escala, la pantalla se dibuja de WIDTH * E x HEIGHT * E
colores = {0:'white',1:'black'}

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



def vecinos_vivos(tablero, m:int, n:int):
    """
    tablero es un conjunto de pares (m,n) con m,n enteros. Son los pixeles vivos.
    """
    """
    - Si (m + n) % 2 == 0 sus vecinos son: 
    (m-1,n+1), (m,n+1), (m+1,n+1), (m-2,n), (m-1,n), (m+1,n), (m+2,n), (m-2,n-1), (m-1,n-1), (m,n-1), (m+1,n-1), (m+2,n-1)  
    - Si (m + n) % 2 == 1 sus vecinos son:
    (m-2,n+1), (m-1,n+1), (m,n+1), (m+1,n+1), (m+2,n+1), (m-1,n), (m-2,n), (m+1,n), (m+2,n), (m-1,n-1), (m,n-1), (m+1,n-1)
    post: devuelve el conjunto de vecinos vivos.
    """
    if (m + n) % 2 == 0:
        vecinos = {(m-1,n+1), (m,n+1), (m+1,n+1), (m-2,n), (m-1,n), (m+1,n), (m+2,n), (m-2,n-1), (m-1,n-1), (m,n-1), (m+1,n-1), (m+2,n-1)}
    else:
        vecinos = {(m-2,n+1), (m-1,n+1), (m,n+1), (m+1,n+1), (m+2,n+1), (m-1,n), (m-2,n), (m+1,n), (m+2,n), (m-1,n-1), (m,n-1), (m+1,n-1)}
    
    return tablero & vecinos


def num_vecinos_vivos_dic(tablero, u):
    """
    Sea (m,n) = u
    - Si (m + n) % 2 == 0 sus vecinos son: 
    (m-1,n+1), (m,n+1), (m+1,n+1), (m-2,n), (m-1,n), (m+1,n), (m+2,n), (m-2,n-1), (m-1,n-1), (m,n-1), (m+1,n-1), (m+2,n-1)  
    - Si (m + n) % 2 == 1 sus vecinos son:
    (m-2,n+1), (m-1,n+1), (m,n+1), (m+1,n+1), (m+2,n+1), (m-1,n), (m-2,n), (m+1,n), (m+2,n), (m-1,n-1), (m,n-1), (m+1,n-1)
    post: devuelve la cantidad de vecinos que valen 1.
    """
    (m,n) = u
    num_vecinos_vivos = 0
    vecinos_E = [(m-1,n+1), (m,n+1), (m+1,n+1), (m-2,n), (m-1,n), (m+1,n), (m+2,n), (m-2,n-1), (m-1,n-1), (m,n-1), (m+1,n-1), (m+2,n-1)]
    vecinos_O = [(m-2,n+1), (m-1,n+1), (m,n+1), (m+1,n+1), (m+2,n+1), (m-1,n), (m-2,n), (m+1,n), (m+2,n), (m-1,n-1), (m,n-1), (m+1,n-1)]
    if (m + n) % 2 == 0:
        for vecino in vecinos_E:
            if (vecino[0],vecino[1]) in tablero:
                num_vecinos_vivos += tablero[(vecino[0],vecino[1])]
    else:
        for vecino in vecinos_O:
            if (vecino[0],vecino[1]) in tablero:
                num_vecinos_vivos += tablero[(vecino[0],vecino[1])]
    return num_vecinos_vivos


def vecinos(tablero, u):
    (m,n) = u
    if (m + n) % 2 == 0:
        vecinos = {(m-1,n+1), (m,n+1), (m+1,n+1), (m-2,n), (m-1,n), (m+1,n), (m+2,n), (m-2,n-1), (m-1,n-1), (m,n-1), (m+1,n-1), (m+2,n-1)}
    else:
        vecinos = {(m-2,n+1), (m-1,n+1), (m,n+1), (m+1,n+1), (m+2,n+1), (m-1,n), (m-2,n), (m+1,n), (m+2,n), (m-1,n-1), (m,n-1), (m+1,n-1)}
    return vecinos

def num_vecinos_vivos(tablero, u):
    return len(vecinos(tablero, u) & tablero)


def juego_vida(screen, LFR, patron):
    # LFR = (El, Eh, Fl, Fh) # regla del juego de la vida
    # patron: es un conjunto de pixeles vivos
    tablero = set()
    for u in patron:
        tablero = tablero | {u}
    print('Patron:', len(tablero),'vivos')
    print('Comienza el juego')
    pasos = 0
    print('vecinos vivos de (0,0)', len(vecinos(tablero, (0,0)) & tablero))
    while pasos < 10:
        print('Vivos:',tablero, pasos)
        tablero_orig = tablero.copy()
        print('Vivos 2:',tablero_orig, pasos)
        for u in tablero_orig:
            entorno = vecinos(tablero_orig,u) | {u} # u y todos sus vecinos
            # print('entorno de', u, entorno)
            for v in entorno:
                n_vivos = num_vecinos_vivos(tablero_orig, v)
                if  v in tablero_orig and not(LFR[0] <= n_vivos <= LFR[1]):
                    print('muere', v)
                    tablero = tablero - {v}
                elif v not in tablero_orig and LFR[2] <= n_vivos <= LFR[3]:
                    print('nace', v)
                    tablero = tablero | {v}
        pasos += 1

                

    

def main():
    screen = ''
    # patron = [(0,0), (2,0),(2,1), (4,2),(4,3),(4,4), (6,3),(6,4),(6,5),(7,4)]
    # patron = [(0,1), (1,2), (2,0), (2,1),(2,2)]
    # patron = [(1,5),(1,6),(2,5),(2,6),(11,5),(11,6),(11,7),(12,4),(12,8),(13,3),(13,9),(14,3),(14,9),(15,6),(16,4),(16,8), (17,5),(17,6),(17,7),(18,6),(21,3),(21,4),(21,5),(22,3),(22,4),(22,5),(23,2),(23,6),(25,1),(25,2),(25,6),(25,7),(35,3),(35,4),(36,3),(36,4)]
    
    patron = {(-1,1), (0,1), (1,1), (-2,0), (-1,0)} # (0,0) tiene 5 vecinos

    # juego_vida_dic(screen, (2,3,3,3), patron)
    juego_vida(screen, (3,4,4,6), patron)
    return 0

# RUN
 
if __name__ == '__main__':
    main()