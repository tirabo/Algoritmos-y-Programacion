import pygame
from pygame.locals import *
import time
from random import randint
from random import random
from math import sin, cos, pi

# BOLA DE BILLAR umplementación con pygame


def bola_de_billar(screen, ancho: int, alto:int, repeticiones: int):
    # pre: screen es la ventana de pygame, ancho y alto son las dimensiones de la ventana
    #      repeticiones es el número de movimientos máximos
    # post: dibuja la trayectoria de una bola de billar con velocidad n que parte de (pos_x, pos_y)
    #       con direccion direc. Los tres números pos_x, pos_y, direc son elegidos al azar.
    #       devuelve  pos_x, pos_y, direc
    #       La bola de billar se detiene si 
    #           1) "cae" en una caja roja de 50 x 50  centrada, o bien,
    #           2) el número de movimientos es > repet
    
    pos_x, pos_y = randint(0, ancho), randint(0,alto) # posición inicial
    direc = random() * 2 * pi # angulo de la dirección inicial entre 0 y 2*pi
    dir_x, dir_y = cos(direc), sin(direc) # dirección inicial

    limite = 0
    while not (ancho/2-25 <= pos_x <= ancho/2 + 25 and alto/2-25 <= pos_y <= alto/2+25) and limite < repeticiones:
        if pos_x <= 0:
            # pi/2 < direc < 3pi/2
            direc = pi - direc
            # - pi/2 < direc < pi/2
            dir_x, dir_y = cos(direc), sin(direc)
            pos_x, pos_y = dir_x, pos_y - dir_y 
        elif pos_x >= ancho:
            # -pi/2 < direc < pi/2
            direc = pi - direc
            # pi/2 < direc < 3pi/2
            dir_x, dir_y = cos(direc), sin(direc)
            pos_x, pos_y = ancho + dir_x, pos_y - dir_y  
        elif pos_y >= alto:
            # pi < direc < 2pi
            direc = 2*pi - direc
            # 0 < direc < pi
            dir_x, dir_y = cos(direc), sin(direc)
            pos_x, pos_y = pos_x + dir_x, alto - dir_y  
        elif pos_y <= 0:
            # 0 < direc < pi
            direc = 2*pi - direc
            # pi < direc < 2pi
            dir_x, dir_y = cos(direc), sin(direc)
            pos_x, pos_y = pos_x + dir_x, - dir_y  
        else:
            pos_x, pos_y = pos_x + dir_x, pos_y - dir_y
        pygame.draw.circle(screen, 'white', (pos_x,pos_y), 2)
        pygame.display.update()
        limite += 1
    return pos_x, pos_y, direc


def main():
    pygame.init()
    ancho, alto = 800, 500
    screen = pygame.display.set_mode((ancho, alto)) # crea ventana
    pygame.display.set_caption('Bola de billar')
    color = Color(50,100,50,255) # RGB
    screen.fill(color)
    color_int = (150,50,50,255)
    pygame.draw.rect(screen, color_int, (ancho/2-25,alto/2-25,50,50), 0)

    # pygame.draw.rect(screen, 'black', (100,100,10,10), 0)
    pygame.display.update()
    bola_de_billar(screen, ancho, alto, 100000)
    pygame.display.update()
    time.sleep(30)
    pygame.quit()

# RUN

if __name__ == '__main__':
    main()