import requests
from bs4 import BeautifulSoup
import json

CLAVES = ['hora', 'desc', 'temp', 'dir', 'vel', 'hum', 'pres'] 


def registro_fila_tabla(fila_tabla) -> dict: # procesa una fila de la tabla, devuelve un diccionario con las mediciones registradas en esa fila
    celdas_fila = fila_tabla.findAll('td')
    registro = {}
    i = 0
    for celda in celdas_fila:                # recorre las celdas de la fila correspondiente a una toma de mediciones
        if celda.img != None: # si existe el tag 'img'
            input_tag = celda.img['title'] # recupera en el tag 'img' el valor del atributo 'title'
            registro[CLAVES[i]] = input_tag # dirección del viento
            i = i + 1
        registro[CLAVES[i]] = celda.text
        i = i + 1
    return registro

def registros_tabla(tabla) -> dict:          # procesa una tabla, devuelve un diccionario de registros contenidos en esa tabla
    registros = {}
    for fila_tabla in tabla.findAll('tr'):
        registro = registro_fila_tabla(fila_tabla)
        if len(registro) != 0:
            hora = registro.pop('hora')
            hh = int(hora[:2])
            registros[hh] = registro
    return registros



MESES = {'01': 'enero', '02': 'febrero', '03': 'marzo', '04': 'abril', '05': 'mayo', '06': 'junio', '07': 'julio', '08': 'agosto', '09': 'septiembre', '10': 'octubre', '11': 'noviembre', '12': 'diciembre'}


def formatear_fecha(fecha: str) -> str:
    # pre:  fecha es una fecha en el formato 'AAAAMMDD'
    # post: devuelve la fecha  en el formato dia-nombre del mes-año
    año = fecha[0:4]
    m = fecha[4:6]
    dia = fecha[6:8]

    mes = MESES[m]
    if dia[0] == '0':
        dia = dia[1]
    return dia + '-' + mes + '-' + año

def eliminar_unidades(registro: dict):
    # pre:  recibe un diccionario tipo  {'desc': 'Despejado', 'temp': '13°', 'dir': 'Noroeste', 'vel': '7 km/h', 'hum': '88%', 'pres': '1015 hPa'}
    # post: modifica el propio diccionario tipo   {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015}
    try:
        registro['temp'] = int(registro['temp'][:-1])
    except:
        registro['temp'] = None
    try:
        registro['vel'] = int(registro['vel'][:-5])
    except:
        registro['vel'] = None
    try:
        registro['hum'] = int(registro['hum'][:-1])
    except:
        registro['hum'] = None
    try:
        registro['pres'] = int(registro['pres'][:-4])
    except:
        registro['pres'] = None
    return registro

def año_bisiesto(n:int):
    if n % 4 != 0:
        return False
    # if multiplo_de_100(n) and multiplo_de_400(n): # Corrección: multiplo_de_100(n) and multiplo_de_400(n) no está definidos
    if n % 100 == 0 and n % 400 == 0:
        return True
    # if not multiplo_de_100(n): # Corrección: multiplo_de_100(n)
    if n % 100 == 0:
        return True
    return False

def int_a_str_largo_dos(n:int):
    # n = str(n) # Corrección: no hay que cambiar el valor del parámetro de entrada
    # if len(n) < 2:
    #    n = '0' + n
    # return n
    return "{:02d}".format(n)



def registros_dia(estacion: str, fecha: str) -> dict:
    contenido_url = requests.get('https://www.tutiempo.net/registros/' + estacion + '/' + formatear_fecha(fecha) + '.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")
    diccionario_de_diccionarios = registros_tabla(tabla_dia)
    for key in diccionario_de_diccionarios:
        diccionario_de_diccionarios[key] = eliminar_unidades(diccionario_de_diccionarios[key])
    return diccionario_de_diccionarios

def clima_anho(estacion: str, anho: str, mes_ini: int, mes_fin: int):
    if año_bisiesto(int(anho)):
        dias_en_febrero = 29
    else:
        dias_en_febrero = 28
    dias_del_mes = {1: 31, 2: dias_en_febrero, 3: 31, 4: 30, 5: 31, 6: 30, 7:31, 8:31, 9: 30, 10: 31, 11: 30, 12: 31}

    fechas = []

    for mes in range(mes_ini, mes_fin + 1):
        for dia in range(1, dias_del_mes[mes] + 1):
            dia = int_a_str_largo_dos(dia)
            # mes = int_a_str_largo_dos(mes) # Corrección: NUNCA modificar la variable del for
            # fechas.append(anho + mes + dia) 
            mes_n = int_a_str_largo_dos(mes)
            fechas.append(anho + mes_n + dia) 
    
    archivo = open('./2021/tareas/cerda_molina/'+str(anho) + '.txt','w')
    for fecha in fechas:
        renglon = registros_dia(estacion, fecha)
        renglon = {fecha : renglon}
        renglon = str(renglon)
        archivo.write(renglon + '\n')
    archivo.close()

def lista_de_diccionarios_desde_archivo(anho) -> list:
    archivo = open('./2021/tareas/cerda_molina/'+str(anho) + '.txt', 'r')
    lista_de_lineas = archivo.readlines()
    archivo.close()
    lista_de_diccionarios = []
    for linea in lista_de_lineas:
        lista_de_diccionarios.append(eval(linea))
    return lista_de_diccionarios

# Retorna el minimo y maximo de un año y un mes dado.
# mes debe ser un string por ejemplo '05'.
def temp_min_max_mes(anho, mes):
    lista_de_diccionarios = lista_de_diccionarios_desde_archivo(anho)
    temps = []
    for diccionario in lista_de_diccionarios:
        # Ahora, diccionario es un diccionario que tiene solo una llave y un valor.
        for key in diccionario: # Este se va a ejecutar una vez
            if key[4:6] == mes:
                diccionario_de_horas = diccionario[key]
                for hora in diccionario_de_horas:
                    diccionario_de_datos = diccionario_de_horas[hora] # Datos del clima
                    temperatura = diccionario_de_datos['temp']
                    if temperatura != None:
                        temps.append(temperatura)
    return min(temps), max(temps)

def temp_min_max(anho): # Corrección: temp_min_max no imprime el promedio de temperaturas máximas del año sino la temperatura máxima de cada
    for mes in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
        min, max = temp_min_max_mes(anho, mes)
        print(mes + ' -> min: ' + str(min) + ', max: ' + str(max))

# fecha es un str del tipo "20180505"
# Devuelve true si se corresponde con una fecha de primavera.
# Considerando que escogimos una estación de un país del hemisferio norte
def es_primavera(fecha) -> bool:
    mes = int(fecha[4:6])
    dia = int(fecha[6:8])
    # return 3 <= mes <= 6 or (mes == 3 and dia >= 21) or (mes == 6 and dia <= 21) 
    # Corrección: como son todos 'or' con el primero alcanza (los otros están incluidos). Luego toma 4 meses, más que la primavera.  
    return (mes == 3 and dia >= 21) or mes == 4 or mes == 5 or (mes == 6 and dia <= 20) # reemplazo mio


def temp_max(anho):
    lista_de_diccionarios = lista_de_diccionarios_desde_archivo(anho)
    temps = [] # Por cada día vamos a tener una temperatura máxima
    for diccionario in lista_de_diccionarios:
        # Ahora, diccionario es un diccionario que tiene solo una llave y un valor.
        for key in diccionario: # Este se va a ejecutar una vez
            if es_primavera(key):
                diccionario_de_horas = diccionario[key]
                temps_del_dia = []
                for hora in diccionario_de_horas:
                    diccionario_de_datos = diccionario_de_horas[hora] # Datos del clima
                    temperatura = diccionario_de_datos['temp']
                    if temperatura != None:
                        temps_del_dia.append(temperatura)
                maximo_del_dia = max(temps_del_dia)
                temps.append(maximo_del_dia)
    # Calculamos el promedio de todas las temperaturas máximas de temps
    print(len(temps))
    return sum(temps) / len(temps)

def dir_viento(anho):
    lista_de_diccionarios = lista_de_diccionarios_desde_archivo(anho)
    dirs = {'En calma': 0, 'Variable': 0, 'Norte': 0, 'Sur': 0, 'Este': 0, 'Oeste': 0, 'Nordeste': 0, 'Noroeste': 0, 'Sureste': 0, 'Suroeste': 0}
    el_mejor = 'En calma'
    cantidad_que_aparecer_el_mejor = 0

    for diccionario in lista_de_diccionarios:
        # Ahora, diccionario es un diccionario que tiene solo una llave y un valor.
        for key in diccionario: # Este se va a ejecutar una vez
            if es_primavera(key):
                diccionario_de_horas = diccionario[key]
                for hora in diccionario_de_horas:
                    diccionario_de_datos = diccionario_de_horas[hora] # Datos del clima
                    direccion = diccionario_de_datos['dir']
                    dirs[direccion] += 1
                    if dirs[direccion] > cantidad_que_aparecer_el_mejor:
                        el_mejor = direccion
                        cantidad_que_aparecer_el_mejor = dirs[direccion]
                    
    return el_mejor


def main():
    # clima_anho('eddl', '2018',1,12)
    print('Temperaturas mínimas y máximas durante cada mes del año en Düsseldorf:')
    temp_min_max('2018')
    print()
    print('Promedio de las temperaturas máximas de primavera de 2018 de Düsseldorf:')
    print(temp_max('2018'))
    print()
    print('Dirección del viento predominante durante la primavera del año 2018 de Düsseldorf:')
    print(dir_viento('2018'))

# RUN

if __name__ == '__main__':
    main()




