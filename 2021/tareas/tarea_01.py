from turtle import *
import math
import time

# 1. Hacer una función `poligono-regular()`que dado un entero positivo `n`, dibuje un polígono regular de `n` lados. 
# 
#**Ejemplo**
#        poligono_regular(3) 



def triangulo_iso(ang: float, largo: float):
    # post: dibuja un triángulo isosceles con un vértice con angulo interior ang  
    #       y los lados iguales de longitud largo
    #       (la orientación depende de hacia donde esté mirando la tortuga)

    ang_inf = (180 - ang) / 2 # los angulos de los otros vertices
    base = 2 * math.sin(math.pi * ang / 360) * largo # el largo del lado distinto (hat que pasar a radianes)
    print ('ang:', ang, 'ang_inf :', ang_inf, largo, base)
    forward(largo)
    right(180 - ang_inf)
    forward(base)
    right(180 - ang_inf)
    forward(largo)
    right(180 - ang) # queda en la misma orientación que partio


def poligono_regular(n: int, radio: float):
    ang_int = 360 / n
    for i in range(n):
        triangulo_iso(ang_int, radio)
        right(ang_int)

colormode(255)
bgcolor('lightgray')
shapesize(1, 1, 2)
pensize(4)
speed(1)

# triangulo_iso(15, 250)
poligono_regular(6,150)


done()