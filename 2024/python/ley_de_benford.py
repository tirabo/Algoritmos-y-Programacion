import random
import math



rep, rango =  10**6, 10**4

frecuencia = [0]*9

for i in range(rep):
    x = random.randint(1, rango)
    primer_d = int(str(x)[0])
    frecuencia[primer_d - 1] += 1

def porcentaje_digitos(frecuencia):
    lon = len(frecuencia)
    total = 0
    for i in range(lon):
        total += frecuencia[i]
    return [math.floor(frecuencia[i] * 1000 / total) / 10 for i in range(lon)]



def siracusa(n: int, frecuencia: list):
    k = n
    contador = 0
    while k != 1:
        contador += 1
        primer_d = int(str(k)[0])
        frecuencia[primer_d - 1] += 1
        if k  % 2 == 0:
            k = k // 2
        else:
            k = 3 * k + 1
    return contador

frecuencia = [0]*9

print(siracusa(13, frecuencia))
print(siracusa(123, frecuencia))
print(siracusa(1000, frecuencia))
print(siracusa(27, frecuencia))
print(siracusa(121, frecuencia))

exit(0)

frecuencia = [0]*9
for i in range(2, 3000):
    siracusa(i, frecuencia)


print('Siracusa:', porcentaje_digitos(frecuencia))



# frecuencia = [0]*9
# for i in range(2, 10000):
#     siracusa(i, frecuencia)
# print(frecuencia)

# print('Siracusa:', porcentaje_digitos(frecuencia))
# print("Teórico:  [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]")


def tipo_sir1(n: int, iteraciones: int, frecuencia: list):
    k, i = n, 0
    while k != 1 and i <= iteraciones:
        i += 1
        primer_d = int(str(k)[0])
        frecuencia[primer_d - 1] += 1
        if k  % 2 == 0:
            k = k // 2
        else:
            k = 7 * k + 3
        # k = k % 10**6 # el numero se mantiene siempre por abajo de los 6 dígitos

frecuencia = [0]*9
for i in range(2, 1000):
    tipo_sir1(i, 1000, frecuencia)


print('Tipo Siracusa 1:', porcentaje_digitos(frecuencia))

def tipo_sir2(n: int, iteraciones: int, frecuencia: list):
    k, i = n, 0
    while k != 1 and i <= iteraciones:
        i += 1
        primer_d = int(str(k)[0])
        frecuencia[primer_d - 1] += 1
        if k  % 4 == 0:
            k = k // 4
        elif k % 2 == 0:
            k = k + 1
        else:
            k = 9 * k + 1
        # k = k % 10**6 # el numero se mantiene siempre por abajo de los 6 dígitos


frecuencia = [0]*9
for i in range(50000, 51000):
    tipo_sir2(i, 1000, frecuencia)


print('Tipo Siracusa 2:', porcentaje_digitos(frecuencia))
print("Teórico:         [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]")