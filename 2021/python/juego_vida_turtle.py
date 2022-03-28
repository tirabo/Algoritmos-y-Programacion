from turtle import *
import random
import time

"""
JUEGO DE LA VIDA TOROIDAL
El juego se desrrolla en un toro S^1 x S^1 con diámetros WIDTH y HEIGHT respectivamente 
(más sencillo: un rectángulo donde lo de arriba se continúa con lo de abajo, lo de la izquierda con lo de la derecha). 
Las reglas son 
1) Cada pixel de tablero es 1 o 0 (negro o blanco). 
2) Hay una cantidad de pixeles inciales que está en 1 (patrón o semilla). 
3) Cada pixel (x,y) tiene 8 vecinos: (x-1,y+1), (x,y+1), (x+1,y+1), (x-1,y), (x+1,y), (x-1,y-1), (x,y-1), (x+1,y-1).
4) En cada paso se cambian los pixeles de 1 a 0 o de 0 a 1 según las siguientes reglas: para obtener la nueva distribución de pixeles en el paso n
     a) En la configuración n-1 cualquier pixel 1 con dos o tres vecinos vivos sigue siendo 1 en la configuración n.
     b) En la configuración n-1 cualquier pixel 0 con tres vecinos 1 pasa a ser 1 en la configuración n.
     c) Todas los otros pixeles de la configuración n-1 pasan a 0 en la configuración n.
"""

# CONSTANTES

WIDTH = 64
HEIGHT = 48
E = 10 # E es la escala, la pantalla se dibuja de WIDTH * E x HEIGHT * E
background = 'gray' # color de fondo
lapiz = 'black' # color dl lápiz
# patron = [(0,0), (2,0),(2,1), (4,2),(4,3),(4,4), (6,3),(6,4),(6,5),(7,4)]
# patron = [(0,1), (1,2), (2,0), (2,1),(2,2)]
patron = [(1,5),(1,6),(2,5),(2,6),(11,5),(11,6),(11,7),(12,4),(12,8),(13,3),(13,9),(14,3),(14,9),(15,6),(16,4),(16,8),
(17,5),(17,6),(17,7),(18,6),(21,3),(21,4),(21,5),(22,3),(22,4),(22,5),(23,2),(23,6),(25,1),(25,2),(25,6),(25,7),(35,3),(35,4),(36,3),(36,4)]

# FUNCIONES

def coord_dib(x:int, y:int):
    # pre: 0 <= x <= W, 0 <= y <= H (si no se arregla con congruencia)
    # post: hace un cambio de coordenadas de (x,y) tal que 
    # (0,0) -> (-E*W/2,E*H/2), 
    # (W,H) -> (E*W/2,-E*H/2)
    u, v = x % WIDTH, y % HEIGHT
    return (E*u - (E*WIDTH)//2, - E*v + (E*HEIGHT)//2)

def make_tablero():
    # post: Dibuja el ractángulo. Construye un array de WIDTH x HEIGHT con 0 en todas partes y lo devuelve
    color(lapiz)
    fillcolor(background)
    penup()
    (u, v) = coord_dib(0,0)
    setpos(u, v)
    pendown()
    begin_fill()
    forward(E*WIDTH)
    right(90)
    forward(E*HEIGHT)
    right(90)
    forward(E*WIDTH)
    right(90)
    forward(E*HEIGHT)
    right(90)
    end_fill()
    penup()
    tblr = []
    for i in range(WIDTH):
        tblr.append([])
        for j in range(HEIGHT):
            tblr[i].append(0)
    return tblr

def put_pixel(tablero, x:int, y:int):
    # pre: tablero es el tablero creado por  make_tablero(), screen es la ventana (0 <= x < WIDTH, 0 <= y < HEGHT)
    # post: dibuja el pixel (x,y), actualiza el array tablero 
    color(lapiz)
    fillcolor(lapiz)
    penup()
    (u, v) = coord_dib(x,y)
    setpos(u, v)
    pendown()
    begin_fill()
    for i in range(4):
        forward(E)
        right(90)
    end_fill()
    penup()
    tablero[x][y] = 1

def del_pixel(tablero, x:int, y:int):
    # pre: tablero es el tablero creado por  make_tablero(), screen es la ventana (0 <= x < WIDTH, 0 <= y < HEGHT)
    # post: borra el pixel (x,y), actualiza el array tablero 
    color(background)
    fillcolor(background)
    penup()
    (u, v) = coord_dib(x,y)
    setpos(u, v)
    pendown()
    begin_fill()
    for i in range(4):
        forward(E)
        right(90)
    end_fill()
    penup()
    tablero[x][y] = 0

def num_vecinos(tablero, x:int, y:int):
    # post: devuelve la cantidad de vecinos de tablero[x][y] que valen 1 (0 <= x < WIDTH, 0 <= y < HEGHT)
    #       Cada pixel (x,y) tiene 8 vecinos: (x-1,y+1), (x,y+1), (x+1,y+1), (x-1,y), (x+1,y), (x-1,y-1), (x,y-1), (x+1,y-1).
    num_1 = 0
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if tablero[(x + i) % WIDTH][ (y + j) % HEIGHT] == 1:
                num_1 = num_1  + 1
    if tablero[x % WIDTH][y % HEIGHT] == 1:
        num_1 = num_1 - 1
    return num_1

def juego_vida(tablero, patron):
    # pre: tablero es un tablero y patron es la lista de los pixeles iniciales
    # post: cada pixel de tablero es 1 o 0 (1 se dibuja color lapiz, 0 se dibuja color background).
    #      1) se pone 1 en los pixeles de patron
    #      Cada pixel (x,y) tiene 8 vecinos: (x-1,y+1), (x,y+1), (x+1,y+1), (x-1,y), (x+1,y), (x-1,y-1), (x,y-1), (x+1,y-1).
    #      2)  Las reglas para didujar (o borrar) pixeles son: se hace un recorrido por todos los pixeles y
    #         a) Cualquier pixel 1 con dos o tres vecinos vivos sigue siendo 1.
    #         b) Cualquier pixel 0 con tres vecinos 1 se convierte a 1.
    #         c) Todas los otros pixeles pasan a 0.
    
    print('Dibujamos patron')
    for u in patron:
        # put_pixel(tablero, u[0] + WIDTH//2,u[1] + HEIGHT//2)
        put_pixel(tablero, u[0],u[1])
    
    tablero_orig = []
    for i in range(WIDTH):
        tablero_orig.append([])
        for j in range(HEIGHT):
            tablero_orig[i].append(0)
    # time.sleep(5)

    print('Comienza el juego')
    k = 0
    while True:
        k = k + 1
        print('Paso ',k)
        for i in range(WIDTH):
            for j in range(HEIGHT):
                 tablero_orig[i][j] = tablero[i][j]
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if tablero_orig[i][j] == 1 and (num_vecinos(tablero_orig,i,j) == 2 or num_vecinos(tablero_orig,i,j) == 3):
                    tablero[i][j] = 1
                    # put_pixel(tablero, i, j)
                elif tablero_orig[i][j] == 0 and num_vecinos(tablero_orig,i,j) == 3:
                    tablero[i][j] = 1
                    put_pixel(tablero, i, j)
                else:
                    if tablero_orig[i][j] == 1:
                        tablero[i][j] = 0
                        del_pixel(tablero, i, j)
                    else:
                        tablero[i][j] = 0
        # time.sleep(0.03)

"""
def tablero():
    # post: 1) dibuja un tablero con esquinas (-max_x, -max_y), (-max_x, max_y), (max_x, max_y), (max_x, -max_y)
    #       2) construye un array de 2x x 2y con 0 en todas partes
    #       3) devuelve el array
    color('black')
    penup()
    setpos(max_x+1, max_y+1)
    pendown()
    setpos(-max_x-1, max_y+1)
    setpos(-max_x-1,-max_y-1)
    setpos(max_x+1,-max_y-1)
    setpos(max_x+1,max_y+1)
    penup()
    tblr = []
    for i in range(2*max_x):
        tblr.append([])
        for j in range(2*max_y):
            tblr[i].append(0)
    return tblr


def del_pixel(tablero, x:int, y:int):
    # pre: 
    # post: borra el pixel (x,y), actualiza el array tablero 
    x = (x + max_x) % (2*max_x) - max_x 
    y = (y + max_y) % (2*max_y) - max_y
    color(background)
    penup()
    setpos(x, y)
    pendown()
    setpos(x +1 , y)
    setpos(x +1 , y+1)
    setpos(x , y+1)
    setpos(x , y)
    penup()
    tablero[x + max_x][y + max_y] = 0
"""
"""
tblr = tablero(max_x,max_y)
print(len(tblr), len(tblr[0]))

for i in range(10):
    put_pixel(tblr, 10+i, 10+i)
 
for i in range(15):
    del_pixel(tblr,10 + 2*i, 10 + 2*i)
"""
"""
def num_vecinos(tablero, x:int, y:int):
    # post: devuelve la cantidad de vecinos de tablero[x + max_x][y + max_y] que valen 1
    #       Cada pixel (x,y) tiene 8 vecinos: (x-1,y+1), (x,y+1), (x+1,y+1), (x-1,y), (x+1,y), (x-1,y-1), (x,y-1), (x+1,y-1).
    num_1 = 0
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if tablero[(x + i + max_x) % (2*max_x)][ (y + j + max_y) % (2*max_y)] == 1:
                num_1 = num_1  + 1
    if tablero[(x + max_x) % (2*max_x)][ (y + max_y) % (2*max_y)] == 1:
        num_1 = num_1  - 1
    return num_1

def juego(tablero, patron):
    # pre: tablero es un tablero y patron es la lista de los pixeles iniciales
    # post: cada pixel de tablero es 1 o 0 (1 se dibuja color lapiz, 0 se dibuja color background).
    #      1) se pone 1 en los pixeles de patron
    #      Cada pixel (x,y) tiene 8 vecinos: (x-1,y+1), (x,y+1), (x+1,y+1), (x-1,y), (x+1,y), (x-1,y-1), (x,y-1), (x+1,y-1).
    #      2)  Las reglas para didujar (o borrar) pixeles son: se hace un recorrido por todos los pixeles y
    #         a) Cualquier pixel 1 con dos o tres vecinos vivos sigue siendo 1.
    #         b) Cualquier pixel 0 con tres vecinos 1 se convierte a 1.
    #         c) Todas los otros pixeles pasan a 0.
    
    # Dibujamos patron
    for u in patron:
        put_pixel(tablero,u[0],u[1])

    tablero_orig = []
    for i in range(2*max_x):
        tablero_orig.append([])
        for j in range(2*max_y):
            tablero_orig[i].append(0)

    while True:
        for i in range(2*max_x):
            for j in range(2*max_y):
                 tablero_orig[i][j] = tablero[i][j]
        for i in range(2*max_x):
            for j in range(2*max_y):
                if tablero_orig[i][j] == 1 and (num_vecinos(tablero_orig,i,j) == 2 or num_vecinos(tablero_orig,i,j) == 3):
                    tablero[i][j] = 1
                elif tablero_orig[i][j] == 0 and num_vecinos(tablero_orig,i,j) == 3:
                    tablero[i][j] = 1
                    put_pixel(tablero, i -max_x, j - max_y)
                else:
                    if tablero_orig[i][j] == 1:
                        tablero[i][j] = 0
                        del_pixel(tablero, i -max_x, j - max_y)
                    else:
                        tablero[i][j] = 0
    done()
        

tabl = tablero()
juego(tabl, patron)
"""


def main():
    hideturtle()
    tablero = make_tablero()
    juego_vida(tablero, patron)
    return 0

# RUN
 
if __name__ == '__main__':
    main()
    done()
