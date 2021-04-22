import random
import math

# Calcular pi  en forma probabilística (Montecarlo)

# Se "dibuja" (en forma imaginaria) un cuadrado de 1 x 1 y se tiran puntos (x,y)  en el cuadrado
# es decir 0 <= x, y <= 1. 
# (x,y) pertenece al círculo de radio 1 sii x**2 + y**2 <= 1
# La cantidad de (x,y) pertenecientes al círculo de radio 1 es aproximadamente  PI* 0.5**2 * (cantidad de puntos totales).
# Luego PI  "=" (cantidad de puntos en el círculo) /(0.5**2 * (cantidad de puntos totales))

def calcular_pi_prob(n: int ) -> float:
    # calcula pi con n puntos
    en_circulo = 0
    for _ in range(n):
        x, y = random.uniform(0, 1), random.uniform(0, 1)
        if x**2 + y**2 <= 1:
            en_circulo = en_circulo + 1
    return en_circulo /(0.5**2 * n)

print(calcular_pi_prob(1000000))


def  calcular_pi_poligono_cir(n: int) -> float:
    # pre: n >=3
    # post: calcula pi haciendo el polígono regular de n-lados circunscripto a una circunferencia de radio 1
    angulo = 2 * math.pi / n
    base = 2 * math.sin(angulo / 2)
    perimetro = n * base # parecido  2 * PI * radio = 2 * PI
    return perimetro / 2

print(calcular_pi_poligono_cir(1000))

def  calcular_pi_poligono_ins(n: int) -> float:
    # pre: n >=3
    # post: calcula pi haciendo el polígono regular de n-lados circunscripto a una circunferencia de radio 1
    angulo = 2 * math.pi / n
    altura =  math.cos(angulo / 2)
    base = 2 * (1 - altura**2)**0.5
    perimetro = n * base # parecido  2 * PI * radio = 2 * PI
    return perimetro / 2

print(calcular_pi_poligono_ins(1000))

print(calcular_pi_poligono_cir(1000) - calcular_pi_poligono_ins(1000))




def calcular_pi_Newton(n: int ) -> float:
    # ver: http://www.pi314.net/eng/newton.php
    # calcula  24*(3**0.5 /32 - \sum_{k=0}^n  0.5**(4*k+2) * (2*k)!/ (k!**2 * (2*k - 1)*(2*k + 3)))
    pi24 = 3**0.5 / 32
    for k in range(n+1):
        pi24 = pi24 - 0.5**(4*k+2) * math.factorial(2*k) / (math.factorial(k)**2 * (2*k - 1) * (2*k + 3))
    return 24 * pi24

# print(calcular_pi_Newton(50)) # 30 decimales correctos


def calcular_pi_1997(n: int ) -> float:
    # ver: https://en.wikipedia.org/wiki/Approximations_of_%CF%80#Efficient_methods
    # calcula   \sum_{k=0}^n  0.5**(4*k) * (4/(8*k + 1) - 2/(8*k + 4) - 1/(8*k + 5) - 1/(8*k + 6))
    pi = 0
    for k in range(n+1):
        pi = pi +  0.5**(4*k) * (4/(8*k + 1) - 2/(8*k + 4) - 1/(8*k + 5) - 1/(8*k + 6))
    return pi

print(calcular_pi_1997(20)) # ?? decimales correctos
