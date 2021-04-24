from turtle import *
# import turtle_conf
from random import randint
from random import choice

"""
Esta biblioteca está documentada en
https://docs.python.org/3/library/turtle.html
Funciones que podés usar:
- bgcolor(color)
- color(color)
- forward(units)
- backward(units)
- goto(x, y), move turtle to an absolute position. If the pen is down, draw line. Do not change the turtle’s orientation.
- speed(speed), speed debe ser un número entre 1 y 13
- right(degrees) # sexagesimales
- left(degrees) # sexagesimales
- setheading(degrees), para apuntar en cierta dirección (0 - este, 90 - norte, 180 - oeste, 270 - sur)
- penup(), levanta el lápiz, para poder desplazarse sin dejar huella
- pendown(), apoya el lápiz, para volver a dibujar después de haberlo levantado
- width(width), para cambiar el ancho de la línea
- hideturtle(), para que no se vea al "artista"
- showturtle(), para que se lo vuelva a ver
- pos(), return the turtle’s current location (x,y) (as a Vec2D vector).
"""


def dibujar_grilla(ancho = 16, alto = 16):
    global ANCHO, ALTO
    ANCHO, ALTO = ancho,  alto
    hideturtle()
    bgcolor('green')
    color('black')
    pensize(1)
    speed(15)
    # Draw ANCHO-by-ALTO lattice
    color("black") # Color for lattice
    x = -10 * ANCHO
    for y in range(-10 * ALTO, 10 * ALTO + 1, 20):
        penup()
        goto(x, y) # Draw a horizontal line
        pendown()
        forward(2 * 10 * ANCHO)
    y = 10 * ALTO
    right(90)
    for x in range(-10 * ANCHO, 10 * ANCHO + 1, 20):
        penup()
        goto(x, y) # Draw a vertical line
        pendown()
        forward(2 * 10 * ALTO)
    pensize(10)
    color("red")
    penup()
    cruz("red",(ANCHO // 2, ALTO // 2))
    # Go to the center
    pendown()
    speed(1)

def turtle_2_grilla(coor: tuple[int, int]) -> tuple[int, int]:
    # El cuadrado inferior izquierdo de turtle es -20*ANCHO // 2 + 10, -20*ALTO // 2 + 10 en la grilla es 0 , 0 o
    #      (-10*ANCHO  + 10, -10*ALTO + 10) turtle -> (0 , 0) grilla 
    # El cuadrado superior derecho  de turtle es 20*ANCHO // 2 + 10, 20*ALTO // 2 + 10 en la grilla es ANCHO , ALTO, 0
    #     (10*ANCHO + 10, 10*ALTO + 10 ) turtle -> (ANCHO, ALTO)
    # (x,y) turtle ->  ((x-10) // 20 + ANCHO // 2 , (y-10) // 20 + ALTO // 2 ) grilla 
    x, y = coor[0], coor[1]
    x , y = (x-10) // 20 + ANCHO // 2 , (y-10) // 20 + ALTO // 2 
    return x % ANCHO, y % ALTO 

def grilla_2_turtle(coor: tuple[int, int]) -> tuple[int, int]:
    #      (0 , 0) grilla  -> (-10*ANCHO  + 10, -10*ALTO + 10) turtle 
    #     (ANCHO, ALTO) grilla -> (10*ANCHO + 10, 10*ALTO + 10 ) turtle
    # (x,y) grilla ->  ((x-10) + 10*ANCHO)//2, (y-10) + 10*ALTO)//2)
    x, y = coor[0], coor[1]
    return  (20*x -10*ANCHO + 10, 20*y - 10*ALTO + 10)


def cruz(color_cruz, punto: tuple[int, int]):
    # x, y  coordenada de la grilla
    setheading(90)
    penup()
    xt, yt = grilla_2_turtle(punto)
    goto(xt, yt)
    pendown()
    color(color_cruz)
    goto(xt, yt + 1)
    goto(xt, yt - 1)
    goto(xt + 1, yt)
    goto(xt -1, yt)
    goto(xt,yt)
    penup()



def mover_a(dir: str):
    # pre: dir in {'N', 'S', 'E', 'O'} indica puntos cardinales
    # post: se mueve en la grilla ancho x alto según la dirección del punto cardinal
    assert dir in ['N', 'S', 'E', 'O'], "El  input debe ser 'N', 'S', 'E', 'O'"
    xt, yt = pos()
    xt, yt = int(xt), int(yt)
    x, y = turtle_2_grilla((xt, yt))
    penup()
    # print(x,y)
    cruz("blue",(x, y))
    if dir == 'N':
        x, y = x, y + 1
    elif dir == 'S':
        x, y = x, y - 1
    elif dir == 'E':
        x, y = x + 1 , y
    elif dir == 'O':
        x, y = x - 1, y
    cruz("red",(x % ANCHO, y % ALTO))
    return x % ANCHO, y % ALTO

def ubicar_boton():
    x0, y0 = pos()
    penup()
    color("blue")
    x, y = randint(0,ANCHO-1), randint(0,ALTO-1) 
    pensize(10)
    cruz("white",(x , y))
    goto(x0, y0)
    return x, y

def encontrar_al_azar(boton: tuple[int, int]):
    dir = choice(['N', 'S', 'E', 'O'])
    print(dir)
    (xb, yb) = boton
    (x, y) = mover_a(dir)
    while (x,y) != (xb, yb):
        dir = choice(['N', 'S', 'E', 'O'])
        (x, y) = mover_a(dir)
    cruz("yellow", boton)


    


def main():
    dibujar_grilla(10, 10)
    boton = ubicar_boton()
    encontrar_al_azar(boton)
    done()
    return 0

# RUN
 
if __name__ == '__main__':
    main()