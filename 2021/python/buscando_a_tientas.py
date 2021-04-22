from turtle import *
# import turtle_conf
from random import randint

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



def dibujar_grilla(ancho, alto):
    hideturtle()
    bgcolor('green')
    color('black')
    pensize(1)
    speed(15)
    # Draw ancho-by-alto lattice
    color("black") # Color for lattice
    x = -10 * ancho
    for y in range(-10 * alto, 10 * alto + 1, 20):
        penup()
        goto(x, y) # Draw a horizontal line
        pendown()
        forward(2 * 10 * ancho)
    y = 10 * alto
    right(90)
    for x in range(-10 * ancho, 10 * ancho + 1, 20):
        penup()
        goto(x, y) # Draw a vertical line
        pendown()
        forward(2 * 10 * alto)
    pensize(10)
    color("red")
    penup()
    cruz("red",0 - 10, 0 - 10)
    # Go to the center
    pendown()
    speed(1)

def cruz(color_cruz, x, y):
    setheading(90)
    penup()
    goto(x, y)
    pendown()
    color(color_cruz)
    goto(x, y + 1)
    goto(x, y - 1)
    goto(x + 1, y)
    goto(x -1, y)
    goto(x,y)
    penup()



def mover_a(dir: str, ancho,  alto: int):
    # pre: dir in {'N', 'S', 'E', 'O'} indica puntos cardinales
    # post: se mueve en la grilla ancho x alto según la dirección del punto cardinal
    assert dir in ['N', 'S', 'E', 'O'], "El  input debe ser 'N', 'S', 'E', 'O'"
    x, y = pos()
    penup()
    cruz("blue",x, y)
    if dir == 'N':
        x, y = x, (y + 10 * alto + 20) % (2 * 10 * alto) - 10 * alto
        cruz("red",x, y)
    elif dir == 'S':
        x, y = x, (y + 10 * alto - 20) % (2 * 10 * alto) - 10 * alto
        cruz("red",x, y)
    elif dir == 'E':
        x, y = (x + 10 * ancho + 20 ) % (2 * 10 * ancho) - 10 * ancho, y
        cruz("red",x , y)
    elif dir == 'O':
        x, y = (x + 10 * ancho - 20 ) % (2 * 10 * ancho) - 10 * ancho, y
        cruz("red",x , y)




def ubicar_boton():
    penup()
    color("blue")
    x, y = randint(1,16), randint(1,16) 



# 
ANCHO, ALTO = 16, 16
dibujar_grilla(ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
"""
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('E', ANCHO, ALTO)
mover_a('E', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('S', ANCHO, ALTO)
mover_a('O', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('E', ANCHO, ALTO)
mover_a('E', ANCHO, ALTO)
mover_a('N', ANCHO, ALTO)
mover_a('S', ANCHO, ALTO)
mover_a('O', ANCHO, ALTO)
"""

done()