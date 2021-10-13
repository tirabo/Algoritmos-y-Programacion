import random

rep, rango =  10**6, 10**4

frecuencia = [0]*9

for i in range(rep):
    x = random.randint(1, rango)
    xs = str(x)
    split_x = list(xs)
    primer_d = int(split_x[0])
    frecuencia[primer_d - 1] += 1

print(frecuencia)


def siracusa(n: int):
    k = n
    secuencia = []
    while k != 1:
        secuencia.append(k)
        if k % 2 == 0:
            k = k // 2
        else:
            k = 3 * k + 1
    return secuencia
