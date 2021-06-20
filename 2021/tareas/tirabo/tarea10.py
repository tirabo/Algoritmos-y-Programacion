import requests
from bs4 import BeautifulSoup
import json

# Código ordenado con todas las funciones predefinidas hasta ahora 

CLAVES = ['hora', 'desc', 'temp', 'dir', 'vel', 'hum', 'pres'] 
DIR = './2021/tareas/tirabo/'

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
    if len(registro) != 0:
        eliminar_unidades(registro)
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


def formatear_fecha(fecha: str) -> str:
    # pre:  fecha es una fecha en el formato 'AAAAMMDD'
    # post: devuelve la fecha  en el foma dia-nombre del mes-año
    fecha_formateada = ''
    # Insertar código
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    anho, mes, dia = int(fecha[:4]), int(fecha[4:6]), int(fecha[6:])
    mes = meses[mes - 1]
    fecha_formateada = str(dia) + '-' + mes + '-' + str(anho)
    return fecha_formateada

def eliminar_unidades(registro: dict):
    # pre:  recibe un diccionario tipo  {'desc': 'Despejado', 'temp': '13°', 'dir': 'Noroeste', 'vel': '7 km/h', 'hum': '88%', 'pres': '1015 hPa'}
    # post: modifica el propio diccionario tipo   {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015}
    temperatura = registro['temp'].replace('°','').strip()
    try:
        registro['temp'] = int(temperatura)
    except:
        registro['temp'] = None
    velocidad = registro['vel'].replace('km/h','').strip()
    try: 
        registro['vel'] = int(velocidad)
    except:
        registro['vel'] = None
    humedad = registro['hum'].replace('%','').strip()
    try: 
        registro['hum'] = int(humedad)
    except:
        registro['hum'] = None
    presion = registro['pres'].replace('RMK', '').replace('hPa','').strip()
    try: 
        registro['pres'] = int(presion)
    except:
        registro['pres'] = None


def registros_dia(estacion, fecha: str) -> dict:
    nombre_fecha = formatear_fecha(fecha)
    contenido_url = requests.get('https://www.tutiempo.net/registros/'+estacion+'/' + nombre_fecha + '.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")
    return registros_tabla(tabla_dia)

def clima_anho(estacion: str, anho: str, mes_ini: int, mes_fin: int):
    pass # insertar código
    n_anho = str(anho)
    mes_dias = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    datos = open(DIR + n_anho + estacion +'.txt', 'w')
    
    for i in range(mes_ini - 1, mes_fin):
        for j in range(mes_dias[i]):
            fecha = n_anho + '{:02}'.format(i+1) + '{:02}'.format(j+1)
            print(fecha)
            dato = {}
            dato[fecha] = registros_dia(estacion, fecha)   
            datos.write(json.dumps(dato) + '\n')
    datos.close()


# Obtener las temperaturas máximas y mínimas de cada mes del año 2018 de la ciudad elegida.
def leer_medidas(estacion, anho):
    with open(DIR + anho + estacion + '.txt', 'r') as fp:
        anual = fp.readlines()
    datos = {}
    for linea in anual:
        # print(linea)
        dato_dia = json.loads(linea.strip())
        for clave in dato_dia:
            datos[clave] = dato_dia[clave]
    return datos


def temp_min_max(estacion, anho):
    datos = leer_medidas(estacion, anho) # un diccionario con los datos del año
    t_max_list, t_min_list = [-1000]*12 , [1000]*12 # listas temperaturas máximas y mínimas por mes (de 0  a 11)
    for dia in datos:
        t_max_dia, t_min_dia = -1000, 1000
        for hora in datos[dia]:
            if datos[dia][hora]['temp'] != None:
                t_max_dia = max(t_max_dia, datos[dia][hora]['temp'])
                t_min_dia = min(t_min_dia, datos[dia][hora]['temp'])
        # t_max_dia, t_min_dia son máximo y mínimo de dia
        mes = int(dia[4:6]) -1
        t_max_list[mes] = max(t_max_list[mes], t_max_dia)
        t_min_list[mes] = min(t_min_list[mes], t_min_dia)
    print('La temperaturas máximas por mes en '+ estacion + ' en el año ' + anho + ' fueron : ' + str(t_max_list))
    print('La temperaturas mínimas por mes en '+ estacion + ' en el año ' + anho + ' fueron : ' + str(t_min_list))


def primavera(dia):
    # dia en formato 'AAAAMMDD'
    return (dia[4:6] == '03' and int(dia[6:]) >= 21) or dia[4:6] == '04' or dia[4:6] == '05' or (dia[4:6] == '06' and int(dia[6:]) <= 20)

# Calcular el promedio de temperaturas máximas diarias durante la primavera del año 2018 en la ciudad elegida.
def temp_max_prim(estacion, anho):
    datos = leer_medidas(estacion, anho) 
    t_max_list = [] # lista temperaturas máximas por dia
    for dia in datos:
        if primavera(dia):
            t_max_dia = -100
            for hora in datos[dia]:
                if datos[dia][hora]['temp'] != None:
                    t_max_dia = max(t_max_dia, datos[dia][hora]['temp'])
            if t_max_dia != -100:
                t_max_list.append(t_max_dia)
    t_max_prom =  sum(t_max_list) / len(t_max_list)
    print('El promedio de temperaturas máximas en primavera en '+ estacion + ' en el año ' + anho + ' es : ' + str(round(t_max_prom,2)))


# Calcular la dirección del viento predominante durante la primavera del año 2018 en la ciudad elegida.

# Esto es la moda de una lista (de las direcciones del viento). Se puede hace con alguna función de alguna biblioteca.
# pero lo hacemos "a mano"

def moda(lista: list[str]):
    conj_val = set(lista) # conjunto de posibles valores
    moda_lista = ['', -1]
    for valor in conj_val:
        cant = lista.count(valor)
        if cant > moda_lista[1]:
            moda_lista = [valor, cant]
    return moda_lista[0]



def dir_viento_prim(estacion, anho):
    datos = leer_medidas(estacion, anho) 
    t_dir_list = [] # lista direcciones del viento por hora
    for dia in datos:
        if primavera(dia):
            for hora in datos[dia]:
                if datos[dia][hora]['dir'] != None:
                    t_dir_list.append(datos[dia][hora]['dir'])
    print('La dirección del viento predominante durante la primavera del año '+ anho +' en '+ estacion + ' es : ' + moda(t_dir_list))
    


def main():
    # estacion, anho = 'eddl', '2018' # Düsseldorf
    # estacion, anho = 'saco', '2018' # Córdoba
    # estacion, anho = 'eddb', '2018' # Berlín
    # estacion, anho = 'mmun', '2018' # Cancún
    # estacion, anho = 'rjtt', '2018' # Tokio
    # estacion, anho = 'mslp', '2018' # El Salvador
    estacion, anho = 'cwdk', '2018' # Claresholm
    # clima_anho(estacion, anho, 1, 12)
    temp_min_max(estacion, anho)
    temp_max_prim(estacion, anho)
    dir_viento_prim(estacion, anho)

# RUN

if __name__ == '__main__':
    main()

"""
# Cancún: mmun
La temperaturas máximas por mes en mmun en el año 2018 fueron : [28, 30, 30, 31, 31, 31, 33, 33, 32, 31, 30, 30]
La temperaturas mínimas por mes en mmun en el año 2018 fueron : [12, 14, 15, 16, 19, 23, 23, 23, 23, 20, 18, 13]
El promedio de temperaturas máximas en primavera en mmun en el año 2018 es : 29.03
La dirección del viento predominante durante la primavera del año 2018 en mmun es : Sureste

# Düsseldorf: eddl
La temperaturas máximas por mes en eddl en el año 2018 fueron : [14, 8, 16, 29, 30, 29, 36, 36, 31, 27, 19, 14]
La temperaturas mínimas por mes en eddl en el año 2018 fueron : [-1, -9, -8, -1, 5, 9, 11, 8, 2, 2, -2, -3]
El promedio de temperaturas máximas en primavera en eddl en el año 2018 es : 20.26
La dirección del viento predominante durante la primavera del año 2018 en eddl es : Suroeste

# Córdoba: saco
La temperaturas máximas por mes en saco en el año 2018 fueron : [37, 38, 37, 35, 29, 27, 26, 31, 38, 37, 35, 37]
La temperaturas mínimas por mes en saco en el año 2018 fueron : [11, 8, 6, 10, 3, -5, -3, -4, 1, 3, 10, 10]
El promedio de temperaturas máximas en primavera en saco en el año 2018 es : 22.82
La dirección del viento predominante durante la primavera del año 2018 en saco es : Nordeste

# Berlín: eddb
La temperaturas máximas por mes en eddb en el año 2018 fueron : [11, 7, 17, 27, 32, 31, 35, 37, 30, 25, 17, 13]
La temperaturas mínimas por mes en eddb en el año 2018 fueron : [-4, -9, -9, -1, 2, 9, 10, 8, 2, 1, -4, -2]
El promedio de temperaturas máximas en primavera en eddb en el año 2018 es : 20.41
La dirección del viento predominante durante la primavera del año 2018 en eddb es : Nordeste

# Tokio: rjtt (Valentín Díaz Moyano)
La temperaturas máximas por mes en rjtt en el año 2018 fueron : [16, 14, 22, 25, 28, 32, 36, 36, 33, 32, 21, 24]
La temperaturas mínimas por mes en rjtt en el año 2018 fueron : [-2, 0, 3, 8, 11, 15, 20, 21, 16, 13, 8, 2]
El promedio de temperaturas máximas en primavera en rjtt en el año 2018 es : 21.88
La dirección del viento predominante durante la primavera del año 2018 en rjtt es : Sur

# El Salvador: 'mslp' (Yesica Nahir Escobares)
La temperaturas máximas por mes en mslp en el año 2018 fueron : [37, 38, 36, 37, 34, 35, 37, 35, 33, 34, 35, 35]
La temperaturas mínimas por mes en mslp en el año 2018 fueron : [17, 19, 20, 21, 23, 22, 22, 21, 22, 22, 20, 18]
El promedio de temperaturas máximas en primavera en mslp en el año 2018 es : 32.64
La dirección del viento predominante durante la primavera del año 2018 en mslp es : Nordeste

# Claresholm (Alberta, Canada): 'CWDK' (Claire Marie Fahy)
La temperaturas máximas por mes en CWDK en el año 2018 fueron : [11, 5, 8, 28, 30, 28, 33, 39, 30, 24, 14, 12]
La temperaturas mínimas por mes en CWDK en el año 2018 fueron : [-9, -9, -9, -9, -1, 4, 4, 1, -3, -9, -9, -9]
El promedio de temperaturas máximas en primavera en CWDK en el año 2018 es : 14.75
La dirección del viento predominante durante la primavera del año 2018 en CWDK es : Norte
"""