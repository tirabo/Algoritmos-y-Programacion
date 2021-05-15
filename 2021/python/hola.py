import turtle
import buscando_a_tientas as bat

def raiz_bab(x: float, error: float) -> float:
    # pre: x >= 0
    assert x >= 0, 'El número debe ser >= 0'
    # post: devuelve b tal |x - b**2| < error
    b, h = x, 1 
    while abs(x - b**2) >= error:
            # inv: b * h == x and ¿h**2 + b**2 <= 2*x? 
            b, h = (h + b) /2,  2 * x / ( h + b)
            # print(h, b, x - b**2)
    return b 

def raiz_bab_int(x: float, error: float) -> float:
    # pre: x >= 0
    assert x >= 0, 'El número debe ser >= 0'
    # post: devuelve b tal |x - b**2| < error
    b, h = x, 1 
    while abs(x - b**2) >= error:
            # inv: b * h == x and ¿h**2 + b**2 <= 2*x? 
            if b - h > 1000:
                b, h, y = int(b), int(h), int(x)
                b, h = (h + b) // 2,  2 * x // ( h + b)
            else:
                b, h = (h + b) /2,  2 * x / ( h + b)
            # print(h, b, x - b**2)
    return b 
x = 10**55+23344
print(raiz_bab_int(x, 0.1), x**0.5)

#for i in range(26):
#  print(raiz_bab(i**2, 1))

def raiz_bab2(x: float, n: int) -> float:
    b, h = x, 1
    for i in range(n):
        b, h = (h + b) /2,  2 * x / ( h + b)
    return b 

# for i in range(26):
#    print(raiz_bab2(i, 100))

# print(raiz_bab(120888888888888888888887, 0.001))
"""
for i  in range(1000):
    print(raiz_bab(10**14 + i, 0.1))
"""

"""
bat.dibujar_grilla(6, 6)
boton = bat.ubicar_boton()
bat.encontrar_al_azar(boton)
turtle.done()
"""
"""
def es_bisiesto(anho: int) -> bool:
  if anho > 0 and anho % 4 == 0:
    result = True
    if anho % 100 == 0:
      result = False
      if anho % 400 == 0:
        result = True
  else: 
    result = False

  return result
  
def bisiestos_desde_1970(anno) -> int:
    bisiestos_anteriores = (anno // 4 - anno // 100 + anno // 400) - (1970 // 4 - 1970 // 100 + 1970 // 400)
    return bisiestos_anteriores


def dias_del_anho_actual(fec: tuple) -> int:
    DIAS_MESES_ANTERIORES = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    d, m, a = fec

    ddd = d + DIAS_MESES_ANTERIORES[m-1]
    if es_bisiesto(a) and m >= 3:
        ddd = ddd + 1
    return ddd


def dias_desde_epoch(fecha: tuple) -> int:
  dia, mes, anho = fecha
  total_dias = 0
  if anho >= 1970:
      dias_anho = (anho - 1970) * 365
      print(dias_anho)
      print(bisiestos_desde_1970(anho))
      print(dias_del_anho_actual(fecha))
      dias_hasta_anho = bisiestos_desde_1970(anho - 1 ) + dias_anho
      print(dias_hasta_anho)
      total_dias = dias_del_anho_actual(fecha) + dias_hasta_anho
  return total_dias

#print(dias_desde_epoch((1,1,1970))) # 1 (el primer día)
#print(dias_desde_epoch((31,12,1970))) # 365 (todo un año)
#print(dias_desde_epoch((31,12,1971))) # 730 (dos años: 365 * 2)
print(dias_desde_epoch((1,1,1972))) # 1096 (dos años + un año bisiesto: 365 * 2 + 366)
#print(dias_desde_epoch((31,12,1973))) # 1461 (tres años + un año bisiesto: 365 * 3 + 366) 
#print(dias_desde_epoch((12,4,2021))) # 18730 (el lunes pasado)
"""