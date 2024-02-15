import numpy as np
import random
import matplotlib.pyplot as plt

# Amit Saha - Doing Math with Python_ Use Programming to Explore Algebra, Statistics, Calculus, and More!-No Starch Press (2015)
# pp. 163 - 168
# Helecho de Barnsley 

def transformation_1(p):
    x = p[0]
    y = p[1]
    x1 = 0.85*x + 0.04*y
    y1 = -0.04*x + 0.85*y + 1.6
    return x1, y1

def transformation_2(p):
    x = p[0]
    y = p[1]
    x1 = 0.2*x - 0.26*y
    y1 = 0.23*x + 0.22*y + 1.6
    return x1, y1

def transformation_3(p):
    x = p[0]
    y = p[1]
    x1 = -0.15*x + 0.28*y
    y1 = 0.26*x + 0.24*y + 0.44
    return x1, y1

def transformation_4(p):
    x = p[0]
    y = p[1]
    x1 = 0
    y1 = 0.16*y
    return x1, y1


def transform(p):
    # List of transformation functions
    transformations = [transformation_1, transformation_2, transformation_3, transformation_4]
    # Probabilities of each transformation function
    probability = [0.85, 0.07, 0.07, 0.01]
    # Pick a random transformation function and call it
    rnd = random.random() # Random number between 0 and 1
    if rnd <= probability[0]:
        tindex = 0
    elif rnd <= probability[0] + probability[1]:
        tindex = 1
    elif rnd <= probability[0] + probability[1] + probability[2]:
        tindex = 2
    else:
        tindex = 3
    t = transformations[tindex] # Call the transformation function
    x, y = t(p)
    return x, y

def dibujar_helecho(n):
    # We start with (0, 0)
    x, y = [0], [0]
    for i in range(n):
        x1, y1 = transform((x[i], y[i]))
        x.append(x1)
        y.append(y1)
    return x, y


def main():
    n = 1000000 # número de puntos del helecho
    x, y = dibujar_helecho(n)
    # dibujar los puntos
    plt.plot(x, y, '.', color='b', markersize=1)
    plt.title('Helecho {:.2e} puntos'.format(n)) # la cantidad de puntos en notación exponencial
    plt.show()

if __name__ == '__main__':
    main()