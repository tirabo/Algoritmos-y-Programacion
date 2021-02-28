import pygame
from pygame.locals import *
import time
import random
import math
import cmath # numeros complejos


"""
https://scipython.com/book2/chapter-7-matplotlib/problems/p72/the-julia-set/
El conjunto Julia asociado a la función compleja f(z)=z**2 + c puede ser representado usando el siguiente algoritmo.
Para cada punto, z_0, en el plano complejo de tal manera que -1.5 <= Re[z_0] <= 1.5 y -1.5 <= Im[z_0] <= 1.5, iterar según 
   z = z**2 + c,  
dónde c es una constante (compleja). 
Coloree el píxel en una imagen correspondiente a esta región del plano complejo de acuerdo con el número de iteraciones 
necesarias para que |z| supere algún valor crítico, r_max > 0 (o negro si esto no sucede antes de un cierto número máximo de iteraciones n_max).

Escriba un programa para trazar el conjunto de Julia para c = -0.1 + 0.65*j Usando r_max= 10 y n_max=500 (en Python el imaginario puro es "j").
"""

# Tutorial sencillo para dibujar: https://sites.cs.ucsb.edu/~pconrad//cs5nm/topics/pygame/drawing/index.html
# Sitio útil (tutorial, ejemplos, etc) para pygame:  http://programarcadegames.com/

# CONSTANTES
W = 360 # ancho y alto de la pantalla
C = complex(-0.1,0.65)
R_max = 10
N_max = 500
background = 'white'

# z = complex(2,1.3)
# print((z**2).real, z.imag,abs(z), z.conjugate())

# FUNCIONES

def complex_2_coord(z:complex):
    # pre: -1.5 <= Re[z] <= 1.5 y -1.5 <= Im[z] <= 1.5
    # post: cambio de coordenadas tal que 
    #       -1.5 + 1.5*j -> (0,0)
    #        1.5 - 1.5*j -> (W,W)
    #      Nos devuelve las coordenadas para dibujar en pygame
    x, y = z.real, z.imag
    xn, yn = (W/3)*x + (W/2), -(W/3)*y + (W/2) 
    return (round(xn), round(yn)) # para dibujar en pygame deben ser enteros

def coord_2_complex(x:int,y:int):
    # pre: 0 <= x, y <= W (coordenadas del plano pygame)
    # post: cambio de coordenadas tal que 
    #       (0,0) -> -1.5 + 1.5*j 
    #       (W,W) -> 1.5 - 1.5*j
    #      Nos devuelve el complejo para calcular Julia
    return complex((3/W)*x -1.5, -(3/W)*y + 1.5)

def julia():
    for i in range(W):
        for j in range(W):
            k = 0 # cantidad de iteraciones
            z = coord_2_complex(i,j)
            while k <= N_max and abs(z) <= R_max:
                k = k + 1
                z = z**2 + C
            # A esta altura abs(z) <= R_max y  se colorea z según lo grande que es  o abs(Zz > R_max y se colorea negro
            if abs(z) <= R_max:
                color0 = round(max (50, 255 - 255 * 10 * abs(z) / R_max))
                #color0 = round(255*math.log10(max (50, 255 - 255 * 10 * abs(z) / R_max))/math.log10(255))
                color1 = color0 #random.randrange(255)
                color2 = color0
                # print(color0)
            else:
                color0 = 0
                color1 = 0
                color2 = 0
            w = pygame.Color(color0,color1,color2)
            pygame.draw.rect(screen, w, (i,j,1,1), 0)
            pygame.display.update()


# RUN

pygame.init()
screen = pygame.display.set_mode((W, W)) # crea ventana
pygame.display.set_caption("Conjunto de Julia")
screen.fill(background)
pygame.display.update()
julia()
while True:
    for eventos in pygame.event.get():
        if eventos.type == QUIT:
            exit(0) # apretando "x" arriba drecha cierra la ventana