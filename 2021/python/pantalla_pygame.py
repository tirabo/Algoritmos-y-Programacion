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

# CLASES

class Ventana:
    def __init__(self, titulo = '', width = 120, height = 80, e = 10, colors =  ['gray', 'black']):
        self.__titulo = titulo
        self.__width = width
        self.__height = height
        self.__e = e 
        self.__colors = colors
        self.__tblr = []
        for i in range(width):
            self.__tblr.append([])
            for j in range(height):
                self.__tblr[i].append(colors[0])
        # Construye un array que describe el estado de la ventana. El array es de width x height con colors[0] en el inicio en todas partes

        #  Crea una ventana     
        #      titulo: título de la ventana
        #      width, height: ancho y alto de la ventana (en pixeles escalados)
        #      e: tamaño del pixel. Un pixel es  e x e  de pygame
        #      colors: color de fondo y color de dibujo
        pygame.init()
        self.__screen = pygame.display.set_mode((self.__e*self.__width, self.__e*self.__height)) # crea ventana
        pygame.display.set_caption(self.__titulo)
        self.__screen.fill(self.__colors[0])
        pygame.display.update()


    def put_pixel(self, x: int, y: int, col: str):
        # pre: col = un color
        # post: dibuja el pixel (x,y) con  color "col", actualiza el array tablero 
        x, y = x % self.__width, y % self.__height
        pygame.draw.rect(self.__screen, col, (self.__e*x,self.__e*y,self.__e,self.__e), 0)
        self.__tblr[x][y] = col


    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getE(self):
        return self.__e

    def getColores(self):
        return self.__colors
    
    def getTblr(self):
        return self.__tblr

    def setTblr(self, x: int, y: int, color: str):
        print(self.__tblr[2])
        self.__tblr[x][y] = color
        print(x,y)
        print(self.__tblr[2])

        
# FUNCIONES 

def num_vecinos(ventana: Ventana, x: int, y: int):
    # post: devuelve la cantidad de vecinos de ventana.tblr[x][y] que valen ventana.colors[1] (0 <= x < ventana.width, 0 <= y < ventana.height)
    #       Cada pixel (x,y) tiene 8 vecinos: (x-1,y+1), (x,y+1), (x+1,y+1), (x-1,y), (x+1,y), (x-1,y-1), (x,y-1), (x+1,y-1).
    num_1 = 0
    tablero, WIDTH, HEIGHT, COLORES = ventana.getTblr(), ventana.getWidth(), ventana.getHeight(), ventana.getColores()
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if  tablero[(x + i) % WIDTH][ (y + j) % HEIGHT] ==  COLORES[1]:
                num_1 = num_1  + 1
    if tablero[x % WIDTH][y % HEIGHT] == COLORES[1]:
        num_1 = num_1 - 1
    return num_1

def juego_vida(ventana: Ventana,  patron: list):
    # pre: patron es la lista de los pixeles iniciales
    # post: cada entrada de tablero es COLORES[1] o COLORES[0] (color del lapiz es COLORES[1], COLORES[0] color de  background).
    #      1) se pone COLORES[1] en los pixeles de patron
    #      Cada pixel (x,y) tiene 8 vecinos: (x-1,y+1), (x,y+1), (x+1,y+1), (x-1,y), (x+1,y), (x-1,y-1), (x,y-1), (x+1,y-1).
    #      2) En cada paso se cambian los pixeles de COLORES[1] a COLORES[0] o viceversa según las siguientes reglas: 
    #         para obtener el tablero n se usan los valores del tablero n-1 y
    #         a) Cualquier pixel COLORES[1] con dos o tres vecinos vivos sigue siendo COLORES[1].
    #         b) Cualquier pixel COLORES[0] con tres vecinos COLORES[1] se convierte a COLORES[1].
    #         c) Todas los otros pixeles pasan a COLORES[0].
    WIDTH, HEIGHT, COLORES = ventana.getWidth(), ventana.getHeight(), ventana.getColores()

    print('Dibujamos patron')
    for u in patron:
        ventana.put_pixel(u[0] + WIDTH // 2, u[1] + HEIGHT // 2, COLORES[1])
    pygame.display.update()

    vecinos = []
    for i in range(WIDTH):
        vecinos.append([])
        for j in range(HEIGHT):
            vecinos[i].append(0)    

    tablero_orig = [] # [['white'] * HEIGHT] * WIDTH
    for i in range(WIDTH):
        tablero_orig.append([])
        for j in range(HEIGHT):
            tablero_orig[i].append('white')

    print('Comienza el juego', COLORES)
    while True:
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                exit(0) # apretando "x" arriba derecha cierra la ventana
        for i in range(WIDTH):
            for j in range(HEIGHT):
                tablero_orig[i][j] = ventana.getTblr()[i][j]
                vecinos[i][j] = num_vecinos(ventana,i,j)
        
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if tablero_orig[i][j] ==  COLORES[1] and (vecinos[i][j] == 2 or vecinos[i][j] == 3):
                    pass
                elif tablero_orig[i][j] ==  COLORES[0] and vecinos[i][j] == 3:
                    ventana.put_pixel(i, j,  COLORES[1])
                else:
                    if tablero_orig[i][j] ==  COLORES[1]:
                        ventana.put_pixel(i, j,  COLORES[0])
        pygame.display.update()
        # time.sleep(0.1)



def main():

    patron = [(0,0), (2,0),(2,1), (4,2),(4,3),(4,4), (6,3),(6,4),(6,5),(7,4)] 
    # patron = [(0,1), (1,2), (2,0), (2,1),(2,2)]
    # patron = [(1,5),(1,6),(2,5),(2,6),(11,5),(11,6),(11,7),(12,4),(12,8),(13,3),(13,9),(14,3),(14,9),(15,6),(16,4),(16,8), (17,5),(17,6),(17,7),(18,6),(21,3),(21,4),(21,5),(22,3),(22,4),(22,5),(23,2),(23,6),(25,1),(25,2),(25,6),(25,7),(35,3),(35,4),(36,3),(36,4)]
    vtn = Ventana(titulo = '')
    #for u in patron:
    #    vtn.put_pixel(u[0], u[1], 'black')

    juego_vida(vtn, patron)

    return 0

# RUN
 
if __name__ == '__main__':
    main()