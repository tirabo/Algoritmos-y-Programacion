from turtle import *
import random

colormode(255)
bgcolor('white')
shapesize(1, 1, 2)
pensize(3)
speed(8)


for i in range(4):
    for i in range(10):
        clr = (random.randrange(200),random.randrange(200),random.randrange(200))
        pencolor(clr)
        begin_fill()
        for i in range(4):
            forward(10)
            right(90)
        end_fill()
        forward(10)
    right(90)


done()