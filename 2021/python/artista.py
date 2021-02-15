from turtle import *

"""
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
bgcolor('white')
color('black')
speed(1)
forward(100)
left(120)
forward(100)
left(120)
forward(100)
penup()
forward(100)
pendown()
forward(100)
left(120)
forward(100)
left(120)
forward(100)
done()