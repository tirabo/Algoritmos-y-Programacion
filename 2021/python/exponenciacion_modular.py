
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
        #print('x', res, base, exponente)
        if exponente % 2 == 1:
            res = (res * base) % n
            exponente = exponente // 2
            base = base**2 % n
            #print('a', res, base, exponente)
        elif exponente % 2 == 0:
            exponente = exponente // 2
            base = base**2 % n
            #print('b', res, base, exponente)
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



def main():
    tests = [(2,3,23), (5,1125899986842625,100000037)]
    for (a, d, n) in tests:
        print((a, d, n))
        print('em_r0',exp_mod_r0(a, d, n))
        print('em_r1',exp_mod_r1(a, d, n))
        print('em_i0',exp_mod_i0(a, d, n))
        print('em_i1',exp_mod_i1(a, d, n))
    
    return 0

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