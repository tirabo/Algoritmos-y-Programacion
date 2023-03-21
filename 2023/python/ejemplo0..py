import random 

def ejemplo_mientras_r(m: int):
    # pre: m entero, m >= 0
    # post: devuelve n tal 2**(n -1) < m y 2**n >= m
    n = 0
    k = 1
    while k < m:
        n = n + 1
        k = k * 2 
    return n

def main():
    x = random.random() * 10**9 # número decimal de 0 a 1000 millones
    y = ejemplo_mientras_r(x)
    print('Ellogaritmo entero en base 2 de',x,'es',y)
    return 0

# RUN

if __name__ == '__main__':
    main()

