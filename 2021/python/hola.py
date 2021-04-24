import turtle
import buscando_a_tientas as bat


bat.dibujar_grilla(6, 6)
boton = bat.ubicar_boton()
bat.encontrar_al_azar(boton)
turtle.done()

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