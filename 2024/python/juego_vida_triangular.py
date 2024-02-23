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
    * Arriba: (m-2,n+1), (m-1,n+1), (m,n+1), (m+1,n+1), (m21,n+1)
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

def num_vecinos_vivos_dic(tablero, m:int, n:int):
    """
    - Si (m + n) % 2 == 0 sus vecinos son: 
    (m-1,n+1), (m,n+1), (m+1,n+1), (m-2,n), (m-1,n), (m+1,n), (m+2,n), (m-2,n-1), (m-1,n-1), (m,n-1), (m+1,n-1), (m+2,n-1)  
    - Si (m + n) % 2 == 1 sus vecinos son:
    (m-2,n+1), (m-1,n+1), (m,n+1), (m+1,n+1), (m21,n+1), (m-1,n), (m-2,n), (m+1,n), (m+2,n), (m-1,n-1), (m,n-1), (m+1,n-1)
    post: devuelve la cantidad de vecinos que valen 1.
    """
    if abs(m) > WIDTH // 2 - 1 or abs(n) > HEIGHT // 2 - 1:
        print('Error: m o n fuera de rango', m, n)
        exit(0)  
    num_vecinos_vivos = 0
    vecinos_E = [(m-1,n+1), (m,n+1), (m+1,n+1), (m-2,n), (m-1,n), (m+1,n), (m+2,n), (m-2,n-1), (m-1,n-1), (m,n-1), (m+1,n-1), (m+2,n-1)]
    vecinos_O = [(m-2,n+1), (m-1,n+1), (m,n+1), (m+1,n+1), (m+2,n+1), (m-1,n), (m-2,n), (m+1,n), (m+2,n), (m-1,n-1), (m,n-1), (m+1,n-1)]
    if (m + n) % 2 == 0:
        for vecino in vecinos_E:
            num_vecinos_vivos += tablero[vecino[0]][vecino[1]]
    else:
        for vecino in vecinos_O:
            num_vecinos_vivos += tablero[vecino[0]][vecino[1]]
    return num_vecinos_vivos


def num_vecinos_vivos_dic(tablero, u):
    """
    Sea (m,n) = u
    - Si (m + n) % 2 == 0 sus vecinos son: 
    (m-1,n+1), (m,n+1), (m+1,n+1), (m-2,n), (m-1,n), (m+1,n), (m+2,n), (m-2,n-1), (m-1,n-1), (m,n-1), (m+1,n-1), (m+2,n-1)  
    - Si (m + n) % 2 == 1 sus vecinos son:
    (m-2,n+1), (m-1,n+1), (m,n+1), (m+1,n+1), (m21,n+1), (m-1,n), (m-2,n), (m+1,n), (m+2,n), (m-1,n-1), (m,n-1), (m+1,n-1)
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

def vivos(tablero):
    # post: devuelve la cantidad de pixeles vivos en tablero
    vivos = 0
    for u in tablero:
            if tablero[u] == 1:
                vivos = vivos + 1
    return vivos


def juego_vida_dic(screen, LFR, patron):
    # tablero: es un diccionario con claves (m,n) y valores 0 o 1
    tablero = {}
    for u in patron:
        tablero[u] = 1
    print('Patron:', vivos(tablero),'vivos')
    print('Comienza el juego')
    pasos = 0
    while pasos < 100:
        print('Vivos:', vivos(tablero), pasos)
        tablero_orig = tablero.copy()
        for u in tablero_orig:
            (m,n) = u
            if (m + n) % 2 == 0:
                vecinos = [(m-1,n+1), (m,n+1), (m+1,n+1), (m-2,n), (m-1,n), (m+1,n), (m+2,n), (m-2,n-1), (m-1,n-1), (m,n-1), (m+1,n-1), (m+2,n-1)]
            else:
                vecinos = [(m-2,n+1), (m-1,n+1), (m,n+1), (m+1,n+1), (m+2,n+1), (m-1,n), (m-2,n), (m+1,n), (m+2,n), (m-1,n-1), (m,n-1), (m+1,n-1)]
            for v in vecinos:
                if v not in tablero:
                    tablero[v] = 0
            if tablero_orig[u] == 1 and not(LFR[0] <= num_vecinos_vivos_dic(tablero_orig,u) <= LFR[1]):
                    tablero[u] = 0
            elif tablero_orig[u] == 0 and LFR[2] <= num_vecinos_vivos_dic(tablero_orig,u) <= LFR[3]:
                    tablero[u] = 1
                    print('Vivo:', u)
        pasos += 1
        # print(pasos)
    print(len(tablero))
    tablero_arr = [[0]*(HEIGHT // 2) for _ in range(WIDTH // 2)  ]
    for i in range(WIDTH // 2):
        for j in range(HEIGHT // 2):
            if (i,j) in tablero:
                tablero_arr[i][j] = tablero[(i,j)]
    print('Vivos:', vivos(tablero))
                


def juego_vida(screen, LFR, patron):
    """ 
        pre: tablero es un tablero, LFR es la regla (4-upla) y patron es la lista de los pixeles iniciales en 1
        post: juego de la vida con reglas LFR
    """
    tablero =  [[0]*HEIGHT for _ in range(WIDTH)] # tablero de ceros WIDTH x HEIGHT
    # tablero lo pensaremos como un array que en la primera coordenada es desde -WIDHT//2 hasta WIDTH//2 y en la segunda desde -HEIGHT//2 hasta HEIGHT//2 (Phyton nos permite pensarlo así). 
    for u in patron:
        tablero[u[0]][u[1]] = 1

    tablero_orig =  [[0]*HEIGHT for _ in range(WIDTH)]

    print('Comienza el juego')
    pasos = 0
    cambios = {}
    while True:
        # for eventos in pygame.event.get():
        #     if eventos.type == QUIT:
        #         exit(0) # apretando "x" arriba drecha cierra la ventana
        for i in range(-WIDTH //2, WIDTH // 2):
            for j in range(-HEIGHT // 2, HEIGHT // 2):
                 tablero_orig[i][j] = tablero[i][j]
        for i in range(-WIDTH //2 + 1, WIDTH // 2 - 1):
            for j in range(-HEIGHT // 2 + 1, HEIGHT // 2 - 1):
                if tablero_orig[i][j] == 1 and not(LFR[0] <= num_vecinos_vivos(tablero_orig,i,j) <= LFR[1]):
                    tablero[i][j] = 0
                elif tablero_orig[i][j] == 0 and LFR[2] <= num_vecinos_vivos(tablero_orig,i,j) <= LFR[3]:
                    tablero[i][j] = 1
        pasos += 1
        print('Pasos:', pasos)
        # pygame.display.update()
        #time.sleep(1)

    

def main():
    screen = ''
    # patron = [(0,0), (2,0),(2,1), (4,2),(4,3),(4,4), (6,3),(6,4),(6,5),(7,4)]
    # patron = [(0,1), (1,2), (2,0), (2,1),(2,2)]
    # patron = [(1,5),(1,6),(2,5),(2,6),(11,5),(11,6),(11,7),(12,4),(12,8),(13,3),(13,9),(14,3),(14,9),(15,6),(16,4),(16,8), (17,5),(17,6),(17,7),(18,6),(21,3),(21,4),(21,5),(22,3),(22,4),(22,5),(23,2),(23,6),(25,1),(25,2),(25,6),(25,7),(35,3),(35,4),(36,3),(36,4)]
    patron = [(i,j) for  i in range(10) for j in range(10)]

    # juego_vida_dic(screen, (2,3,3,3), patron)
    juego_vida_dic(screen, (4,6,4,4), patron)
    return 0

# RUN
 
if __name__ == '__main__':
    main()