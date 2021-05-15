
def exp_mod_r0(a, d, n):
    if d == 0:
        res = 1
    elif d % 2 == 1:
        res =  (a * exp_mod_r0(a, d - 1, n)) % n
    else:
        res =  a**2 * exp_mod_r0(a, d // 2, n) 
    return res

print('em_r0',exp_mod_r0(5,1125899986842625,100000037))


def exp_mod(a, d, n):
    if d == 0:
        res = 1
    elif d % 2 == 1:
        res =  (a * exp_mod(a, d - 1, n)) % n
    else:
        res =  exp_mod(a**2 % n, d // 2, n) 
    return res

#print(exp_mod(2,5,15))


def exp_modular(a, d, n):
    # pre: a, d >= 0, n > 0
    # post: calcula res = a**d % n utilizando el método binario 
    #       de exponenciacion modular
    res = 1
    base, exponente = a, d
    while exponente > 0:
        # invariante: (a**d) % n = (res * base**exponente) % n
        print('x', res, base, exponente)
        if exponente % 2 == 1 and exponente > 1:
            res = a * res
            exponente = exponente - 1
            print('a', res, base, exponente)
        elif exponente % 2 == 0:
            res = (res * base**2) 
            exponente = exponente // 2
            base = base**2 
            print('b', res, base, exponente)
        else:
            exponente = 0
    return res

print(exp_modular(2,7,15), 2**7)
#print(exp_modular(5,1125899986842625,100000037))

def exp_modular2(a, d, n):
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
print('em1',exp_mod(5,1125899986842625,100000037))
print('em2',exp_modular2(5,1125899986842625,100000037))
























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