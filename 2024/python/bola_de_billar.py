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
- setposition(x, y), para mover la tortuga a la posición (x, y)
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

Observación:  el sistema de coordenadas está centrado en la esquina inferior derecha de la ventana 

"""




def dibujar_rectangulo(ancho, alto, col = 'black', grosor_lapiz = 2):
    # pre: ancho y alto son números enteros positivos, col es un color, grosor_lapiz de 1 a 20
    # post: dibuja una rectángulo ancho x alto en el centro de la ventana
    penup()
    pensize(grosor_lapiz)
    setposition(-ancho//2, alto//2) # (-ancho//2, alto//2) es el centro.  
    setheading(0)
    color(col)
    pendown()
    for _ in range(2):
        forward(ancho)
        right(90)
        forward(alto)
        right(90)
    penup()
    color('black') 



def pizarra_vacia(velocidad = 5, grosor_lapiz = 5):
    # inicializa la pizarra con velocidad 5 y ancho del lápiz igual 5
    # Dibuja un marco de 10 px de grosor
    screensize(800, 500)
    dibujar_rectangulo(800, 500, 'black', 10) # dibuja el marco
    hideturtle()
    bgcolor('white')
    color('black')
    speed(velocidad)
    pensize(5)


def bola_de_billar(n: int, repet: int):
    # pre: n de 1 a 12
    # post: dibuja la trayectoria de una bola de billar con velocidad n que parte de (pos_x, pos_y)
    #       con direccion direc. Los tres números pos_x, pos_y, direc son elegidos al azar.
    #       devuelve  pos_x, pos_y, direc
    #       La bola de billar se detiene si 
    #           1) "cae" en una caja roja de 50 x 50  centrada, o bien,
    #           2) el número de movimientos es > repet
    dibujar_rectangulo(50, 50, 'red')
    speed(n)
    pos_x0, pos_y0 = randint(-400, 400), randint(-250,250)
    penup()
    setposition(pos_x0, pos_y0) # ubica la tortuga en (pos_x0, pos_y0)
    direc0 = randint(1, 360)
    setheading(direc0) # la tortuga apunta a direc
    pendown()
    pos_x, pos_y, direc = pos_x0, pos_y0, direc0

    limite = 0
    while not (-25 <= pos_x <= 25 and -25 <= pos_y <= 25) and limite < repet:
        pos_x, pos_y = position()
        if pos_x >= 400:
            direc = 180 - direc
            setheading(direc)
            setposition(400, pos_y) 
        elif pos_x <= -400:
            direc = 180 - direc
            setposition(-400, pos_y)
            setheading(direc) 
        elif pos_y >= 250:
            direc = 360 - direc
            setposition(pos_x, 250)
            setheading(direc)
        elif pos_y <= -250:
            direc = 360 - direc
            setposition(pos_x, -250)
            setheading(direc)
        forward(5)
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