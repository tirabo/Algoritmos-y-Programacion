# Prueba de GitHub copilot

def calcular_dias_entre_fechas(fecha_inicial, fecha_final):
    año_inicial, mes_inicial, dia_inicial = fecha_inicial
    año_final, mes_final, dia_final = fecha_final
    dias_entre_fecha_inicial_y_final = 0
    if año_inicial == año_final:
        if mes_inicial == mes_final:
            dias_entre_fecha_inicial_y_final = dia_final - dia_inicial
        else:
            dias_entre_fecha_inicial_y_final = (dia_final - dia_inicial) + (mes_final - mes_inicial) * 30
    else:
        dias_entre_fecha_inicial_y_final = (dia_final - dia_inicial) + (mes_final - mes_inicial) * 30 + ((año_final - año_inicial) - 1) * 360
    return dias_entre_fecha_inicial_y_finalc

def exponenciacion_modular_rapida(base, exponente, modulo):
    resultado = 1
    while exponente > 0:
        if exponente % 2 == 1:
            resultado = (resultado * base) % modulo
        exponente = exponente // 2
        base = (base * base) % modulo
    return resultado

def quick_sort(lista):
    if len(lista) < 2:
        return lista
    pivote = lista[0]
    menores = [x for x in lista[1:] if x <= pivote]
    mayores = [x for x in lista[1:] if x > pivote]
    return quick_sort(menores) + [pivote] + quick_sort(mayores)

def raiz_cuadrada_entera(n:int) -> int:
    """
    Calcula la raiz cuadrada entera de un numero entero
    """
    if n < 0:
        raise ValueError('El numero no puede ser negativo')
    if n == 0:
        return 0
    if n > 0:
        return int(n ** (1/2))

def prime_list(n):
    # Given a natural number n >= 2 returns the list of all prime numbers between 2 and n-1.
    # The function should return an empty list if n < 2.
    if n < 2:
        return []
    else:
        primes = [2]
        for i in range(3, n):
            for j in range(2, i):
                if i % j == 0:
                    break
            else:
                primes.append(i)
        return primes
