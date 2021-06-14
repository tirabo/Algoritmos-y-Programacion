import random
import math

def pot_mod(a: int, d: int, n: int) -> int:
    # pre: a, d, n enteros positivos
    # post: devuelve a**d % n calculado por el método binario de exponenciacion modular
    c = 1
    d1, r1 = (d // 2), d % 2 # d = d1 * 2 + r1 => a**d = (a**2)**d1 * a**r1
    a1 = a
    while d1 > 0:
        a1, c  = a1**2 % n, c * a1**r1 % n
        r1 =  d1 % 2
        d1 = d1 // 2
    c = c * a1**r1 % n
    return c


# INICIO: generación de primos

def pot2(n: int):
    # pre: n > 0, n impar
    # post: devuelve s, d tal n = 2**s * d + 1,  con d impar.
    u, m = (n -1) % 2, (n - 1) // 2
    s = 0
    while u == 0:
        s = s + 1
        u, m = m % 2, m // 2
    d = (n -1) // 2**s
    return (s, d)


def fpp(n, a: int) -> bool:
    # pre:  n impar, 0 < a < n
    # post: devuelve True si n = es FPP respecto a a. False en caso contrario
    ret = False
    (s, d) = pot2(n)
    if 1 == pot_mod(a, d, n):
        ret = True
    else:
        r, b = 0, d
        while r  <= s and ret == False:
            # print(r)
            if n - 1 == pot_mod(a, b, n):
                ret = True
            r, b = r + 1, 2 * b
    return ret


def test_Miller_Rabin(n: int, k: int) -> bool:
    # pre: n > 2, n impar, k > 0
    # post: si n es FPP k-veces (con base al azar) devuelve True. En  caso  contrario  devuelve False. 
    ret = False
    (s, d) = pot2(n)
    # print('Verificando si  2**%d * %d + 1 = %d  es primo' % (s, d, n))
    for i in range(k):
        a = random.randrange(2, n) # entero al azar entre 2 y n-1
        # print(i, a, d,n)
        if 1 == pot_mod(a, d, n):
            ret = True
        else:
            r, b = 0, d
            while r  <= s and ret == False:
                # print(r)
                if n - 1 == pot_mod(a, b, n):
                    ret = True
                r, b = r + 1, 2 * b
    return ret


def criba_w(n): # de Wikipedia en inglés.
    # Devuelve la lista de primos  <= n
    a = [True]*(n+1) # Hace un  lista de n+1 elementos cada uno True [True, True, ..., True]
    """
    a = []
    for _ in range(n+1):
        a.append(True)
    """
    for i in range(2, int(n**0.5) + 1): # por observación 1
        if a[i] == True:
            for j in range(i**2, n+1, i ): # por observación 2
                a[j] = False
    # Si a[i] == True,  entonces i es primo (i >= 2)
    return [i for i in range(2,n+1) if a[i] == True]

def coprimo_primos(n, primos):
    # devuelve True si n no es divisible  por los números de la lista primos
    assert n > primos[-1], 'El número debe ser mayor que el último número de la lista'
    res = True
    i, k = 0, len(primos)
    while i < k and n % primos[i] != 0:
        i = i + 1
    if i < k:
        res = False
    return res 


def generador_candidato(long, primos):
    # post: genera al azar un número de longitud long no divisible por los u in primos
    candidato = random.randint(10**long + 1, 10**(long+1)-1)
    while not coprimo_primos(candidato, primos):
        candidato = random.randint(10**long + 1, 10**(long+1)-1)
    return candidato


def numero_primo(long, primos, k):
    # Devuelve un número  de longitud long que supera M-R k veces (un primo)
    candidato = generador_candidato(long, primos)
    print('Intento: ', end = '')
    i = 0
    while not test_Miller_Rabin(candidato, k):
        candidato = generador_candidato(long, primos)
        i = i + 1
        print(str(i)+', ',end='')
    print('')
    return candidato

# FIN: generación de primos


# INICIO: RSA obtención de claves

def clave_pub(p,q: int) -> tuple[int, int]:
    # pre: p, q números primos
    # post: devuelve (n, e) tal que n == p*q y mcd(e, (p-1)*(q-1)) == 1 
    pass
    n = p * q
    e, m = 3, (p-1) * (q-1)
    while math.gcd(e, m) != 1:
        e = e + 1
    return n, e

# Se debe usar la siguiente función (o similar) para resolver ed = 1 (mod (p-1)(q-1))

def mcd_extendido(a, b: int) -> tuple[int, int, int]:
    # pre: a y b son números positivos
    # post: devuelve d, s, t tal que d = mcd(a,b) = a*s + b*t
    d, s, t = 0, 0, 0
    r0, r1 = a, b
    s0, t0, s1, t1 = 1, 0, 0, 1
    while r1 != 0:
        # invariante: r0 = a * s0 + b * t0  y
        #             mcd(a, b) = mcd(r0, r1)
        resto = r0 % r1
        q, r0, r1 = r0 // r1, r1, resto
        s1p, t1p = s1, t1
        s0, t0, s1, t1 =  s1p, t1p, s0 - s1 * q, t0 - t1 * q
        d, s, t = r0, s0, t0 # linea para notación
    return (d, s, t)

# Ver https://cp-algorithms.com/algebra/extended-euclid-algorithm.html por el recursivo
def mcd_extendido_rec(a, b: int ) -> tuple[int, int, int]:
    d, s, y = 0, 0, 0  
    # Caso base  
    if a == 0 :   
        d, s, t = b, 0, 1 
    else:         
        d, s1, t1 = mcd_extendido(b % a, a)  
        # Update x and y using results of recursive  
        # call  
        s = t1 - (b//a) * s1  
        t = s1  
    return (d, s, t) 


def clave_priv(p, q, e: int) -> int:
    # pre: p, q números primos, mcd(e, (p-1)*(q-1)) == 1
    # post: devuelve d tal que e * d % (p-1)*(q-1) == 1
    pass
    m = (p-1) * (q-1)
    return mcd_extendido(e, m)[1] % m

# FIN: RSA obtención de claves


# INICIO: RSA 

def encriptar(m, n, e: int) -> int:
    # pre: n y e deben ser una clave pública RSA
    # post: devuelve m**e % n 
    return m**e % n

def desencriptar(n, c, d: int)  -> int:
    # pre: n es la primera clave pública, d es la clave privada, c es un mensaje encriptado. 
    # post: devuelve c**d % n
    return pot_mod(c, d, n)

# FIN: RSA 

def main():
    # Descomentar lo siguiente si se quieren nuevos primos
    """
    primos = primos = criba_w(5000) # todos los primos <= 5000
    p, q = numero_primo(100, primos, 50), numero_primo(100, primos, 50) # obtención de primos
    print(p)
    print(q)
    """
    p = 12195878778068251673224510841090361216371724659218143091701098943552708400169879538990823136619718141
    q = 32443522233551044158197351393974000677841230224084672992641137108209159232691644730637877353177980877
    (n, e) = clave_pub(p, q) # Obtención de clave pública
    print('Clave pública:', n, e)
    d = clave_priv(p, q, e) # Obtención de clave privada
    print('Clave privada:',d)
    m = random.randint(10**198, 10**199) # Mensaje al azar
    print('mensaje O:', m) # Mensaje original
    m_e = encriptar(m, n, e) # Encriptar
    print('encriptado:', m_e) # Mensaje encriptado
    # El último paso no se puede hacer sin una mejor implementación de c**d % n
    m_d = desencriptar(n, m_e, d)  # Desencriptar
    print('mensaje D:', m_d) # Mensaje desencriptado
    
    return None


# RUN
if __name__ == '__main__':
    main()
