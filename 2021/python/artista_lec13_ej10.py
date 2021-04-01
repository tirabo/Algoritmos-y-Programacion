from turtle import *

"""
Esta biblioteca está documentada en
https://docs.python.org/3/library/turtle.html
Funciones que podés usar:
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

# https://studio.code.org/s/20-hour/stage/13/puzzle/10

# todas las coordenadas las multiplico por  10, para que haya separación
# Hacemos una grilla de 20 x 20 (lista de listas), y en cada coordenada ponemos 0 si está vacía,  n > 0 si es montículo de de altura n y m < 0 si es pozo de profundidad m. 
# 
terreno = []
for i in range(10):
    terreno.append([])
    for j in range(10):
        terreno[i].append(0)
# terreno es plano
# Ahora ponemos montones y agujeros
terreno[0][0], terreno[1][0], terreno[2][0], terreno[3][0] = 1, 1, 1, 1 # columna 0
terreno[0][1], terreno[1][1] = -1, -1 # columna 1
terreno[0][2], terreno[1][2], terreno[2][2], terreno[3][2] = 1, 1, 1, 1 # columna 2
terreno[0][3], terreno[1][3] = -1, -1 # columna 3
terreno[0][4], terreno[1][4] = -1, -1 # columna 4
terreno[0][5], terreno[1][5], terreno[2][5], terreno[3][5] = 1, 1, 1, 1 # columna 5
terreno[0][6], terreno[1][6] = -1, -1 # columna 6

def dib_monton(i,j: int):
    color('black')
    fillcolor('black')
    penup()
    u, v = 20*i, 20*j
    setpos(u, v)
    pendown()
    begin_fill()
    for i in range(4):
        forward(5)
        right(90)
    end_fill()
    penup()

def dib_pozo(i,j: int):
    color('red')
    fillcolor('red')
    penup()
    u, v = 20*i, 20*j
    setpos(u, v)
    pendown()
    begin_fill()
    for i in range(4):
        forward(5)
        right(90)
    end_fill()
    penup()

# Dibujar terreno
for i in range(10):
    for j in range(10):
        if terreno[j][i] == 1:
            dib_monton(i, j)
        if terreno[j][i] == -1:
            dib_pozo(i, j)
penup()
setpos(0,0)


def quitar_pila_4():
    left(90)
    for _ in range(4):
        pass


done()