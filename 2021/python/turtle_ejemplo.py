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


def dibujar_triangulo(lado: int):
    for _ in range(4):
        forward(lado)
        left(120)

def dibujar_cuadrado(lado: int):
    for _ in range(4):
        forward(lado)
        left(90)

cadena_1 = ' Hola! Que tal?   '
cadena_1 = cadena_1.strip() # 'Hola! Que tal?'
cadena_2 = 'ok'
cadena = cadena_1 + cadena_2

def factorial(n:int) -> int:
    fac = 1
    if n == 1:
        fac = 1
    if n > 1:
        fac = factorial(n-1)*n
    return fac

print(factorial(5))


# print(cadena_1[3])
#print(cadena_2)
#print(cadena_1 + cadena_2)
#print(cadena_1,cadena_2)





bgcolor('green')
color('black')
pensize(5)
speed(1)

#dibujar_triangulo(100)

dibujar_cuadrado(100)
penup()
forward(150)
pendown()
dibujar_cuadrado(100)


done()

