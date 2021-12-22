# Escribir el código más abajo
def es_bisiesto(anho: int) -> bool:
    bisiesto = False
    if anho % 100 == 0:
        bisiesto = anho % 400 == 0 
    if anho % 100 != 0:
        bisiesto = anho % 4 == 0
    return bisiesto



def bisiestos_hasta(anho: int) -> int:
    # pre: anho es un año válido
    # post: devuelve el número de años bisiestos pasados incluyendo anho, si es bisiesto
    bisiestos_anteriores = anho // 4 - anho // 100 + anho // 400
    return bisiestos_anteriores


def dias_del_anho_actual(fecha: tuple) -> int:
    # pre: fecha es una fecha válida
    # post: devuelve el número de días transcurridos en el corriente año, contando el actual
    DIAS_MESES_ANTERIORES = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    dia, mes, anho = fecha

    dias = dia + DIAS_MESES_ANTERIORES[mes-1]
    if es_bisiesto(anho) and mes >= 3:
        dias = dias + 1
    return dias


def dias_desde_epoch(fecha: tuple) -> int:
    # pre: fecha tiene el formato (DD, MM, AAAA)
    # post: dias desde 1-1-1970 a DD-MM-AAAA
    dia, mes, anho = fecha
    
    nro_de_dias = (anho - 1970) * 365 + bisiestos_hasta(anho - 1969) + dias_del_anho_actual(fecha)
    return nro_de_dias

def add_n(n):
    def pp(v):
        return [u + n for u in v]
    return pp

M1 = [[1, 2, 3], [-2, 3, 7]]
M2 = [[1,0,0],[0,1,0],[0,0,1]]
def array_mult(M, N):
    return [[sum(a*b for a, b in zip(row, col)) for col in zip(*N)] for row in M]

print(array_mult(M1, M2))