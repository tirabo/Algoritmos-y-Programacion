import pygame
from pygame.locals import *
import math
import time

"""
IMPLEMENTACION DE turtle CON pygame
La biblioteca turtle está documentada en
https://docs.python.org/3/library/turtle.html
Funciones a implementar:
- bgcolor(color)
- color(color)
- forward(units)
- backward(units)
- speed(speed), speed debe ser un número entre 1 y 14
- right(degrees)
- left(degrees)
- face(degrees), para apuntar en cierta dirección
- penup(), levanta el lápiz, para poder desplazarse sin dejar huella
- pendown(), apoya el lápiz, para volver a dibujar después de haberlo levantado
- width(width), para cambiar el ancho de la línea
- hideturtle(), para que no se vea al "artista"
- showturtle(), para que se lo vuelva a ver
"""

# Tutorial sencillo para dibujar con pygame: https://sites.cs.ucsb.edu/~pconrad//cs5nm/topics/pygame/drawing/index.html
# Sitio útil (tutorial, ejemplos, etc) para pygame:  http://programarcadegames.com/


# CONSTANTES
WIDTH = 240
HEIGHT = 160
E = 5 # E es la escala, la pantalla se dibuja de WIDTH*E x HEIGHT*E pixeles reales
CAPTION = 'El artista'


# VARIABLES GLOBALES
background = 'gray' # color de fondo
pencil_down = 'black' # color del lapiz
pencil = pencil_down
tort_x, tort_y = (E*WIDTH)//2, (E*HEIGHT)//2, #posición de la tortuga en coordenadas E*WIDTH, E*HEIGHT (en pixeles)
tort_dir = 0 # dirección en grados
tort_vel = 5 # número de  1 a 14
tort_down = 'red'
tort_col = tort_down
tort = (E + 1) // 2 # tamaño de la tortuga
pen = tort # tamaño del lápiz #por ahora debe ser igual a tort

# INIT
pygame.init()
screen = pygame.display.set_mode((E*WIDTH, E*HEIGHT)) # crea ventana


# FUNCIONES

def bgcolor(cl):
    global background
    background = cl
    screen.fill(background)
    pygame.display.update()

def color(cl):
    global pencil_down, pencil
    pencil_down = cl
    pencil = pencil_down

def forward(units):
    # pre: units  está en el rango WIDTH x HEIGHT
    # post: avanza E*units pixeles. Si se va de la pantalla queda en el borde. 
    global tort_x, tort_y # para que no se piense que las variables son de la función
    tort_xp, tort_yp = tort_x + E * units * math.cos(tort_dir * math.pi /180), tort_y + E * units * math.sin(tort_dir * math.pi /180)
    tort_xp, tort_yp = max(0, round(tort_xp)), max(0, round(tort_yp))
    print('(',tort_x,tort_y,') --> (',tort_xp,tort_yp,')')
    r0 = ((tort_xp - tort_x)**2 + (tort_yp - tort_y)**2)**0.5
    r0 = round(r0)
    tort_xp, tort_yp = min(E*WIDTH, tort_xp), min(E*HEIGHT, tort_yp)
    pygame.draw.circle(screen, background, (tort_x,tort_y), tort, 0) # borra la tortuga
    pygame.draw.circle(screen, pencil, (tort_x,tort_y), pen, 0) # dibuja el lapiz en lugar de la tortuga
    if units > 0:
        rango = [ x for x in range(r0)]
    elif units < 0:
        rango = [ -x for x in range(r0)]
    else:
        rango = [0]
    for r in rango:
        x, y = tort_x + r*math.cos(tort_dir * math.pi /180), tort_y + r*math.sin(tort_dir * math.pi /180)
        pygame.draw.circle(screen, tort_col, (x,y), tort, 0)
        pygame.display.update()
        pygame.draw.circle(screen, tort_col, (x,y), tort, 0) #dibujo la tortuga 2 veces para que se vea el desplazamiento
        pygame.display.update()
        time.sleep(0.1/tort_vel)
        pygame.draw.circle(screen, pencil, (x,y), pen, 0)
        pygame.display.update()
    tort_x, tort_y = tort_x + rango[r0-1]*math.cos(tort_dir * math.pi /180), tort_y + rango[r0-1]*math.sin(tort_dir * math.pi /180)
    pygame.draw.circle(screen, tort_col, (tort_x,tort_y), tort, 0)
    pygame.display.update()

def backward(units):
    forward(-units)

def speed(vel):
    # post: setear velocidad. de 1 a 14. 5 es lo estandar.
    global tort_vel
    tort_vel = vel

def right(degrees):
    global tort_dir
    tort_dir = tort_dir + degrees 

def left(degrees):
    right(-degrees)

def face(degrees):
    # post: para apuntar en cierta dirección
    global tort_dir
    tort_dir = degrees

def penup():
    # post:levanta el lápiz, para poder desplazarse sin dejar huella
    global pencil, tort_col
    if tort_col == pencil:
        tort_col = background
    pencil = background
    
def pendown():
    # post: apoya el lápiz, para volver a dibujar después de haberlo levantado
    global pencil
    pencil = pencil_down

def width(width):
    # post: para cambiar el ancho de la línea (y la tortuga). 2 es lo estandar. 
    global pen, tort
    pen, tort  = (2 * width + 1) // 2, (2 * width + 1) // 2

def hideturtle():
    # post:  para que no se vea al "artista" (la tortuga)
    global tort_col
    tort_col = pencil

def showturtle():
    # post: para que se lo vuelva a ver
    global tort_col
    tort_col = tort_down


def main():
    global tort_dir, tort_col, tort_vel, pencil, pen, tort
    pygame.display.set_caption(CAPTION)
    screen.fill(background)
    pygame.draw.circle(screen, tort_col, (tort_x,tort_y), tort, 0)
    pygame.display.update()
    ## EJEMPLOS
    tort_dir = 30
    forward(10)
    color("green")
    tort_dir = 60
    forward(10)
    tort_dir = 90
    forward(20)
    color("black")
    tort_dir = 120
    backward(20)
    speed(10)
    forward(10)
    right(90)
    hideturtle()
    forward(10)
    left(90)
    forward(10)
    face(180)
    forward(10)
    penup()
    forward(20)
    pendown()
    showturtle()
    face(45)
    forward(10)
    ##
    while True:
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                exit(0) # apretando "x" arriba derecha cierra la ventana
            pygame.display.update()

    return 0

# RUN
 
if __name__ == '__main__':
    main()



