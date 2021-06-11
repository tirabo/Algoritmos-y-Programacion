import time

def criba(n):
    # pre: n número natural
    # post: se obtiene ''primos'' la lista de números primos hasta n
    primos = [] # lista vacía
    tachados = [] # lista de números tachados 
    for i in range(2, n + 1):
        if i not in tachados:
            primos.append(i) # agregar i a primos
            k = 2
            while k * i <= n:
                tachados.append(k * i) # agrega k*i a tachados
                k = k + 1
    return primos

def criba_m(n):
    # pre: n número natural
    # post: se obtiene ''primos'' la lista de números primos hasta n
    primos = set(range(2,n+1)) # conjunto de todos los números de 2 a n
    for i in range(2, int(n**0.5) +1):
        if i in primos:
            for j in range(i**2, n+1, i):
                primos.discard(j * i) 
    return primos


def criba_w(n): # de Wikipedia. El mejor. 
    a = [True]*(n+1)
    for i in range(2, int(n**0.5) + 1):
        if a[i] == True:
            for j in range(i**2, n+1, i ):
                a[j] = False
    return [i for i in range(2,n+1) if a[i] == True]


def criba2(n): # esta no es estrictamente la criba: saca todos los k*x para k >=2, sin importar si x es primo o no
    # ce = set(range(2, n + 1)) -  {k * x  for x in range(2, int(n**0.5) + 1) for k in range(2 , n // x  + 1)}
    ce = set(range(2, n + 1)) -  {k for i in range(2, int(n**0.5) + 1) for k in range(i**2, n + 1, i )}
    return  sorted(list(ce))

def criba3(n):
    a = set({})
    for x in range(2, int(n**0.5) + 1):
        if x not in a:
            a = a.union({k*x for k in range(x, n // x  + 1)})
    return set(range(2, n + 1)) - a 

def main():
    n = 10000000
    # n = 100

    t0 = time.time()
    # x = criba(n)
    #print('criba',x)
    t1 = time.time()
    print('criba:',n,'  ',t1-t0)

    t0 = time.time()
    x = criba_m(n)
    #print('criba_m',x)
    t1 = time.time()
    print('criba_m:',n,'  ',t1-t0)

    t0 = time.time()
    x = criba_w(n)
    # print('criba_w', x)
    t1 = time.time()
    print('criba_w:',n,'  ',t1-t0)

    t0 = time.time()
    x = criba2(n)
    # print('criba2', x)
    t1 = time.time()
    print('criba2:',n,'  ',t1-t0)

    t0 = time.time()
    # x = criba3(n)
    #print('criba3', x)
    t1 = time.time()
    print('criba3:',n,'  ',t1-t0)



# RUN

if __name__ == '__main__':
    main()