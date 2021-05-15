from math import log2
from random import randint

def exp_mod_r0(a, d, n):
    if d == 0:
        res = 1
    elif d % 2 == 1:
        res =  (a * exp_mod_r0(a, d - 1, n)) % n
    else:
        res = exp_mod_r0(a, d // 2, n)**2 % n
    return res


def exp_mod_r1(a, d, n):
    if d == 0:
        res = 1
    elif d % 2 == 1:
        res =  (a * exp_mod_r1(a, d - 1, n)) % n
    else:
        res =  exp_mod_r1(a**2 % n, d // 2, n) 
    return res


def exp_mod_i0(a, d, n):
    # pre: a, d >= 0, n > 0
    # post: calcula res = a**d % n utilizando el método binario 
    #       de exponenciacion modular
    res = 1
    base, exponente = a, d
    while exponente > 0:
        # invariante: (a**d) % n = (res * base**exponente) % n
        if exponente % 2 == 1:
            res = (res * base) % n
            exponente = exponente // 2
            base = base**2 % n
        elif exponente % 2 == 0:
            exponente = exponente // 2
            base = base**2 % n
    return res


def exp_mod_i1(a, d, n):
    # pre: a, d >= 0, n > 0
    # post: calcula em = a**d % n utilizando el método binario 
    #       de exponenciacion modular
    res = 1
    base, exponente, paridad = a,d, 0
    while exponente > 0:
        # invariante: (a**d) % n = (res * base**exponente) % n
        paridad = exponente % 2
        exponente = exponente // 2
        res = (res * base**paridad) % n
        base = base**2 % n
    return res

def em(a, d, n):
    return exp_mod_i1(a,d,n)


def fuertemente_pp(n, a: int) -> bool:
    # Devuelve True si  n  es fuertemente probable primo con base a
    d = (n - 1) // 2
    s = 1
    while d % 2 == 0:
        d = d // 2
        s = s + 1
    # n  = 2**s * d + 1 con mcd(2, d) = 1
    fpp = False # suponemos n no es fuertemente primo en base a
    if 1 == em(a, d, n):
        fpp = True
    else:
        r = 0
        while r <= s and fpp == False:
            if n - 1 == em(a, 2**r * d, n): # a**(2**r * d) % n
                fpp = True
            r = r + 1
    return fpp

def test_Miller_Rabin(n: int, k: int) -> bool:
    test = True # paso 0-veces el test
    for _ in range(k):
        a = randint(2, n - 1) # entero al azar entre 2 y n-1
        if not fuertemente_pp(n, a):
            test = False
    return test 


def main():
    tests = [(2,3,23), (5,1125899986842625,100000037)]
    tests = []
    for (a, d, n) in tests:
        print((a, d, n))
        print('em_r0',exp_mod_r0(a, d, n))
        print('em_r1',exp_mod_r1(a, d, n))
        print('em_i0',exp_mod_i0(a, d, n))
        print('em_i1',exp_mod_i1(a, d, n))
    
    print(10000011111111111133343, test_Miller_Rabin(10000011111111111133343, 10))
    print(10000011111111111133349, test_Miller_Rabin(10000011111111111133349, 10))
    print(test_Miller_Rabin(2074722246773485207821695222107608587480996474721117292752992589912196684750549658310084416732550077, 100))


# RUN
 
if __name__ == '__main__':
    main()






















def factorial(n: int) -> int:
    # pre: n >= 0
    # post: devuelve el valor de 1 * 2 * 3 * ... * (n-1) * n
    if n == 0:
        res = 1
    else:
        res = n * factorial(n - 1)
    return res

"""
for n in range(2000):
    print(n)
    factorial(n)
"""

def potencia(a, n: int) -> int:
    # pre: n >= 0
    # post: devuelve el valor de a * a * a * ... * a * a , n veces
    if n == 0:
        res = 1
    else:
        res = a * potencia(a, n - 1)
    return res

"""
for n in range(2000):
    print(n)
    potencia(1, n)
"""

#print(2**1500)