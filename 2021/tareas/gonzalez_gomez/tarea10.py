import requests
from bs4 import BeautifulSoup
import json

# Basado en: 1) https://stackoverflow.com/questions/17196018/extracting-table-contents-from-html-with-python-and-beautifulsoup
# 2) https://www.kite.com/python/examples/4420/beautifulsoup-parse-an-html-table-and-write-to-a-csv

# La información la extraemos de la estación metereológica SACO, correspondiente al Aeropuerto de Córdoba. 

CLAVES = ['hora', 'desc', 'temp', 'dir', 'vel', 'hum', 'pres']
DIR = './2021/tareas/gonzalez_gomez/'

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


def registros_dia(estacion: str, fecha: str) -> dict:
    # pre: fecha es una fecha en el formato 'AAAAMMDD' y estacion es una string que indica la estacion meteorologica a analizar
    # pos: devuelve un diccionario de diccionarios con las claves correspondientes 
    #a las horas del dia y dentro de esos diccionarios las claves "hora", "desc", "temp", "dir", "vel", "hum", "pres"
    #que representan los datos climáticos de la estacion a analizar
    
    assert((type(fecha) == str) and (len(fecha) == 8) and (fecha.isnumeric()) and (type(estacion) == str))

    CLAVES = ["hora", "desc", "temp", "dir", "vel", "hum", "pres"]
    nombre_fecha = formatear_fecha(fecha)
    contenido_url = requests.get('https://www.tutiempo.net/registros/'+ estacion +'/' + nombre_fecha + '.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') 
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) 
    registros = {}
    for fila_tabla in tabla_dia.findAll('tr'):
        celdas_fila = fila_tabla.findAll('td')
        registro = {}
        i = 0
        for celda in celdas_fila:
            if celda.img != None:
                input_tag = celda.img['title']
                registro[CLAVES[i]] = input_tag
                i = i + 1
            registro[CLAVES[i]] = celda.text
            i = i + 1
        if len(registro) != 0:
                hora = registro.pop('hora')
                hh = int(hora[:2])
                registros[hh] = eliminar_unidades(registro)
    return registros

def formatear_fecha(fecha: str) -> str:
    # pre:    fecha es una fecha en el formato 'AAAAMMDD'
    # post: devuelve la fecha    en el foma dia-nombre del mes-año
    assert((type(fecha) == str) and (len(fecha) == 8) and (fecha.isnumeric()))
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    return str(int(fecha[6:])) + '-' + meses[int(fecha[4:6])- 1] + '-' + fecha[:4]


def eliminar_unidades(registro: dict):
    # pre:    recibe un diccionario tipo    {'desc': 'Despejado', 'temp': '13°', 'dir': 'Noroeste', 'vel': '7 km/h', 'hum': '88%', 'pres': '1015 hPa'}
    # post: modifica el propio diccionario tipo     {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015}
    assert(type(registro) == dict and ('temp' in registro) and ('vel' in registro) and ('hum' in registro) and ('pres' in registro))
    
    CLAVES_U = ['temp', 'vel', 'hum', 'pres']
    for CLAVE in CLAVES_U:
        i = len(registro[CLAVE])
        if (registro[CLAVE][0] != '-'):
            while ((not(registro[CLAVE].isnumeric())) and (len(registro[CLAVE]) != 0)): 
                registro[CLAVE] = registro[CLAVE][0:i]
                i = i-1
            if (len(registro[CLAVE]) == 0):
                registro[CLAVE] = None
        else:
            registro[CLAVE] = registro[CLAVE][1:]
            while ((not(registro[CLAVE].isnumeric())) and (len(registro[CLAVE]) != 0)):
                registro[CLAVE] = registro[CLAVE][0:i]
                i = i-1
            if ((len(registro[CLAVE])) == 0):
                registro[CLAVE] = None
            else:
                registro[CLAVE] = '-' + registro[CLAVE]
    return registro



def clima_anho(estacion: str, anho: str, mes_ini: int, mes_fin: int):
    # pre: Recibe una string con la estacion meteorológica a analizar, un año en forma de string, 
    #el mes donde empieza a analizar la funcion y el mes que finaliza de analizar en forma de int
    # pos: Escribe un archivo del tipo 'anho_estacion.txt' en el que en cada renglon hay un diccionario 
    #con los datos del clima de las 24 horas de cada día entre los meses indicados anteriormente en la ciudad que corresponde a la estacion meteorológica
    
    assert((type(anho) == str) and (len(anho) == 4) and (anho.isnumeric()) and (type(mes_ini) == int) and (type(mes_fin) == int) and (mes_ini <= mes_fin) and (type(estacion) == str))

    meses = [31, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    if (((int(anho)) % 4 == 0 and (not ((int(anho)) % 100 == 0))) or ((int(anho)) % 100 == 0 and (int(anho)) % 400 == 0)):
        meses.insert(1, 29)
    else:
        meses.insert(1, 28)
    
    archivo = anho + '_' + estacion + '.txt'
    res = open(DIR + archivo, 'w')
    dicc = {}
    i = mes_ini - 1

    while (i <= (mes_fin - 1)):
        dia = ''
        mes = ''
        if ((i+1) < 10):
            mes = '0' + str(i+1)
        else:
            mes = str(i+1)
        j = 1
        while (j <= (meses[i])):
            if (j < 10):
                dia = '0' + str(j)
            else:
                dia = str(j)
            fecha = anho + mes + dia
            print(fecha)
            dicc[fecha] = registros_dia(estacion, fecha)
            j = j+1
        i = i+1
    
    
    for claves in dicc:
        mes = ''
        if (mes_fin < 10):
            mes = '0' + str(mes_fin)
        else:
            mes = str(mes_fin)
        if (claves == anho + mes + str(meses[(mes_fin) - 1])):
            res.write('{"' + claves + '": ' + json.dumps(dicc[claves]) + '}')
        else:
            res.write('{"'+ claves + '": ' + json.dumps(dicc[claves]) + '}')
            res.write("\n")
    res.close()

def temp_min_max(estacion, anho):
    # pre: Recibe una estacion meteorológica y un año, ambos en forma de string
    # pos: Devuelve una lista de tuplas con la temperatura maxima y minima de cada mes respectivamente del archivo 'anho_estacion.txt'
    
    assert((type(estacion) == str) and (type(anho) == str) and (len(anho) == 4))

    bis = (((int(anho)) % 4 == 0 and (not ((int(anho)) % 100 == 0))) or ((int(anho)) % 100 == 0 and (int(anho)) % 400 == 0))
    DIAS_MESES_ANTERIORES = [31, 59 + bis, 90 + bis, 120 + bis, 151 + bis, 181 + bis, 212 + bis, 243 + bis, 273 + bis, 304 + bis, 334 + bis, 365 + bis]

    arch = open(DIR + anho + '_' + estacion + ".txt", "r")
    arch_lines = arch.readlines()
    dicts = []
    for lines in arch_lines:
        dicts.append(json.loads(lines))
    arch.close()

    max_y_mins = []
    ind = 0
    for can_dias in DIAS_MESES_ANTERIORES:
        temp_min = float("inf")
        temp_max = -274
        while (ind < can_dias):
            fecha = list(dicts[ind].keys())[0]
            for h in range(24):
                if (((str(h)) in (dicts[ind][fecha])) and (type(dicts[ind][fecha][str(h)]['temp']) == str)):
                    temp = int(dicts[ind][fecha][str(h)]['temp'])
                    if (temp > temp_max):
                        temp_max = temp
                    if (temp < temp_min):
                        temp_min = temp                                            
            ind = ind + 1
        max_y_mins.append((temp_max, temp_min))
    
    return max_y_mins

def temp_max(estacion, anho, mes_ini, mes_fin, dia_mes_ini, dia_mes_fin):
    # pre: Recibe una estacion meteorologica y un año en forma de string, y un mes inicial, 
    # mes final, dia inicial del mes inicial, dia final del mes final en forma de int
    # pos: Devuelve un int que representa el promedio de temperaturas maximas de 
    # cada día entre dia_mes_ini/mes_ini/anho y dia_mes_fin/mes_fin/anho

    assert((type(estacion) == str) and (type(anho) == str) and (type(mes_ini) == int) and (type(mes_fin) == int) and (type(dia_mes_ini) == int) and (type(dia_mes_fin) == int) and (len(anho) == 4) and (mes_ini <= mes_fin))



    DIAS_MESES_ANTERIORES = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

    dias_mes_ini = dia_mes_ini + DIAS_MESES_ANTERIORES[mes_ini-1]
    if (((int(anho)) % 4 == 0 and (not ((int(anho)) % 100 == 0))) or ((int(anho)) % 100 == 0 and (int(anho)) % 400 == 0)) and mes_ini >= 3:
        dias_mes_ini = dias_mes_ini + 1

    dias_mes_fin = dia_mes_fin + DIAS_MESES_ANTERIORES[mes_fin-1]
    if (((int(anho)) % 4 == 0 and (not ((int(anho)) % 100 == 0))) or ((int(anho)) % 100 == 0 and (int(anho)) % 400 == 0)) and mes_ini >= 3:
        dias_mes_fin = dias_mes_fin + 1

    arch = open(DIR + anho + '_' + estacion +".txt", "r")
    arch_lines = arch.readlines()
    dicts = []
    for lines in arch_lines:
        dicts.append(json.loads(lines))
    arch.close()

    maximas = []
    ind = dias_mes_ini -1
    while (ind <= (dias_mes_fin-1)):
        temp_max = -274
        fecha = list(dicts[ind].keys())[0]
        print(fecha)
        for h in range(24):
            if (((str(h)) in (dicts[ind][fecha])) and (type(dicts[ind][fecha][str(h)]['temp']) == str)):
                temp = int(dicts[ind][fecha][str(h)]['temp'])

                if (temp > temp_max):
                    temp_max = temp
        maximas.append(temp_max)
        ind = ind + 1    
    res = 0
    for temp in maximas:
        res = res + temp    
    res = res / (len(maximas))
    
    return res



def dir_viento(estacion, anho, mes_ini, mes_fin, dia_mes_ini, dia_mes_fin):
    # pre: Recibe una estacion meteorologica y un año en forma de string, y un mes inicial, 
    # mes final, dia inicial del mes inicial, dia final del mes final en forma de int
    # pos: Devuelve una lista con la/s direccion/es del viento predominante/s entre dia_mes_ini/mes_ini/anho y dia_mes_fin/mes_fin/anho
    
    assert((type(estacion) == str) and (type(anho) == str) and (type(mes_ini) == int) and (type(mes_fin) == int) and (type(dia_mes_ini) == int) and (type(dia_mes_fin) == int) and (len(anho) == 4) and (mes_ini <= mes_fin))


    DIAS_MESES_ANTERIORES = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

    dias_mes_ini = dia_mes_ini + DIAS_MESES_ANTERIORES[mes_ini-1]
    if (((int(anho)) % 4 == 0 and (not ((int(anho)) % 100 == 0))) or ((int(anho)) % 100 == 0 and (int(anho)) % 400 == 0)) and mes_ini >= 3:
        dias_mes_ini = dias_mes_ini + 1

    dias_mes_fin = dia_mes_fin + DIAS_MESES_ANTERIORES[mes_fin-1]
    if (((int(anho)) % 4 == 0 and (not ((int(anho)) % 100 == 0))) or ((int(anho)) % 100 == 0 and (int(anho)) % 400 == 0)) and mes_ini >= 3:
        dias_mes_fin = dias_mes_fin + 1

    arch = open(DIR + anho + '_' + estacion +".txt", "r")
    arch_lines = arch.readlines()
    dicts = []
    for lines in arch_lines:
        dicts.append(json.loads(lines))
    arch.close()

    dir_vien = []
    ind = dias_mes_ini -1
    while (ind <= (dias_mes_fin-1)):
        temp_max = -274
        fecha = list(dicts[ind].keys())[0]
        for h in range(24):
            if (((str(h)) in (dicts[ind][fecha])) and (type(dicts[ind][fecha][str(h)]['dir']) == str)):
                dir_vien.append(dicts[ind][fecha][str(h)]['dir'])                
        ind = ind + 1    
    
    res = []
    count_dires = 0
    for dires in dir_vien:
        if ((dir_vien.count(dires)) > count_dires):
            count_dires = dir_vien.count(dires)
    for dires in dir_vien:
        if (((dir_vien.count(dires)) == count_dires) and ((res.count(dires)) < 1)):
            res.append(dires)
    
    return res


# Llamo a la funcion clima_anho() para crear el archivo a analizar




# Resultados




def main():
    estacion = "sazs"
    anho = "2018"
    # clima_anho(estacion, anho, 1, 12)

    max_y_min = temp_min_max(estacion, anho)
    prom_temp_max = temp_max(estacion, anho, 9, 12, 21, 21)
    dir_pred = dir_viento(estacion, anho, 9, 12, 21, 21)
    
    print("Las temperaturas máximas y minimas respectivamente para cada mes de 2018 en San Carlos de Bariloche son: " + str(max_y_min))
    print("El promedio de las temperaturas máximas diarias durante la primavera del 2018 en San Carlos de Bariloche es: " + str(prom_temp_max) + '°C' )
    print("La/s dirección/es del viento predominante/s durante la primavera del 2018 en San Carlos de Bariloche es/son: " + str(dir_pred))


# RUN

if __name__ == '__main__':
    main()

