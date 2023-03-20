from turtle import *
from random import randint

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
- setheading(degrees), para apuntar en cierta dirección
- setx(x), para cambiar la coordenada x
- sety(y), para cambiar la coordenada y
- penup(), levanta el lápiz, para poder desplazarse sin dejar huella
- pendown(), apoya el lápiz, para volver a dibujar después de haberlo levantado
- width(width), para cambiar el ancho de la línea
- hideturtle(), para que no se vea al "artista"
- showturtle(), para que se lo vuelva a ver
Estado de la tortuga
- position(), 2-upla con las coordenadas
- xcor(), devuelve la coordenada x
- ycor(), devuelve la coordenada y
- heading(), devuelve la dirección en grados

"""



def pizarra_vacia(velocidad = 5, grosor_lapiz = 5):
    # inicializa la pizarra con velocidad 5 y ancho del lápiz igual 5
    screensize(800, 500)
    hideturtle()
    penup()
    setposition(-400, -250)
    setheading(0)
    pendown()
    setheading(0)
    pendown()
    hideturtle()
    bgcolor('white')
    color('black')
    speed(velocidad)
    pensize(grosor_lapiz)
    setposition(0, 0)
    color('red')
    setheading(90)
    forward(380)


def bola_de_billar(n: int, repet: int):
    # pre: n de 1 a 12
    # post: dibuja la trayectoria de una bola de billar con velocidad n que parte de (pos_x, pos_y)
    #       con direccion direc. Los trs números pos_x, pos_y, direc son elegidos al azar.
    #       devuelve  pos_x, pos_y, direc
    speed(n)
    pos_x0, pos_y0 = randint(-400, 400), randint(-250,250)
    penup()
    setposition(pos_x0, pos_y0) # ubica la tortuga en (pos_x0, pos_y0)
    direc0 = randint(1, 360)
    setheading(direc0) # la tortuga apunta a direc
    pendown()
    pos_x, pos_y, direc = pos_x0, pos_y0, direc0
    limite = 0
    while not(pos_x == 400 and pos_y == 250) and limite < repet:
        # print(pos_x, pos_y, direc)
        forward(1)
        pos_x, pos_y = position()
        if pos_x >= 800 or pos_x <= 0:
            direc = 180 - direc
            print('pos_x == 800 or pos_x == 0:', pos_x, pos_y, direc)
            setheading(direc) 
            forward(2) # sale de la encerrona
        elif pos_y >= 500 or pos_y <= 0:
            direc = 360 - direc
            print('pos_y == 500 or pos_y == 0:', pos_x, pos_y, direc)
            setheading(direc)
            forward(2) # sale de la encerrona
        limite += 1
    print('limite:', limite)
    return pos_x0, pos_y0, direc0


def bola_de_billar_2(n: int, repet: int):
    # pre: n de 1 a 12
    # post: dibuja la trayectoria de una bola de billar con velocidad n que parte de (pos_x, pos_y)
    #       con direccion direc. Los trs números pos_x, pos_y, direc son elegidos al azar.
    #       devuelve  pos_x, pos_y, direc
    dibujar_caja(50, 50, 'red')
    speed(n)
    pos_x0, pos_y0 = randint(-400, 400), randint(-250,250)
    penup()
    setposition(pos_x0, pos_y0) # ubica la tortuga en (pos_x0, pos_y0)
    direc0 = randint(1, 360)
    setheading(direc0) # la tortuga apunta a direc
    pendown()
    pos_x, pos_y, direc = pos_x0, pos_y0, direc0
    print(pos_x, pos_y, direc)
    limite = 0
    
    while not (-25 <= pos_x <= 25 and -25 <= pos_y <= 25) and limite < repet:
        pos_x, pos_y = position()
        forward(1)
        if pos_x >= 400 or pos_x <= -400:
            # setposition(400, pos_y)
            direc = 180 - direc
            print('pos_x >= 400:', pos_x, pos_y, direc)
            setheading(direc) 
            forward(2) # para salir de la encerrona
        elif pos_y >= 250 or  pos_y <= -250:
            direc = 360 - direc
            print('pos_y >= 250:', pos_x, pos_y, direc)
            setheading(direc)
            forward(2)
        limite += 1
    print('limite:', limite)
    return pos_x0, pos_y0, direc0


def main():
    pizarra_vacia()
    bola_de_billar(12, 10000)
    done()
    return 0

# RUN

if __name__ == '__main__':
    main()