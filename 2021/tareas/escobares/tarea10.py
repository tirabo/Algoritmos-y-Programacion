import requests
from bs4 import BeautifulSoup
import json


DIR = './2021/tareas/escobares/'

CLAVES = ['hora', 'desc', 'temp', 'dir', 'vel', 'hum', 'pres'] 

def registro_fila_tabla(fila_tabla) -> dict: 
    # post: devuelve un diccionario con las mediciones registradas en esa fila
    celdas_fila = fila_tabla.findAll('td')
    registro = {}
    i = 0
    for celda in celdas_fila:                # recorre las celdas de la fila correspondiente a una toma de mediciones
        if celda.img != None:                # si existe el tag 'img'
            input_tag = celda.img['title']   # recupera en el tag 'img' el valor del atributo 'title'
            registro[CLAVES[i]] = input_tag  # dirección del viento
            i = i + 1
        registro[CLAVES[i]] = celda.text
        i = i + 1
    return registro


def registros_tabla(tabla) -> dict:          
    # post: devuelve un diccionario de registros contenidos en esa tabla
    registros = {}
    for fila_tabla in tabla.findAll('tr'):
        registro = registro_fila_tabla(fila_tabla)
        if len(registro) != 0:
            hora = registro.pop('hora')
            hh = int(hora[:2])
            registros[hh] = registro
            eliminar_unidades(registros[hh])   
    return registros


def formatear_fecha(fecha: str) -> str:
    # pre:  fecha es una fecha en el formato 'AAAAMMDD'
    # post: devuelve la fecha  en el foma dia- nombre del mes -año
    assert type(fecha) == str and len(fecha) == 8, 'Debe ingresar un str de la forma AAAAMMDD'
    MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    anho = fecha[:4]          
    mes = int(fecha[4:6])
    mes_ok = MESES[mes - 1]
    dia = fecha [-2:]
    if dia[0] == '0':       #No es una expresión válida 01-junio-2020
        dia = dia[1]
    return dia + '-' + mes_ok + '-' + anho

def eliminar_unidades(registro: dict):
    # pre:  recibe un diccionario tipo  {'desc': 'Despejado', 'temp': '13°', 'dir': 'Noroeste', 'vel': '7 km/h', 'hum': '88%', 'pres': '1015 hPa'}
    # post: modifica el propio diccionario tipo   {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015}
    assert type(registro) == dict, 'Debe ingresar un diccionario'
    unidades = {'temp': '°', 'vel': 'km/h', 'hum': '%', 'pres': 'hPa'}    #Unidades a eliminar en cada diccionario
    for x in unidades.keys():
        valor = registro[x]
        eliminar = unidades[x]
        if eliminar in valor:
            valor = valor.split(eliminar)      #Eliminamos la unidad no deseada
            asignacion = valor[0].split()      #En muchos casos, se genera una lista con dos elementos: el dato deseado y un espacio
            try: 
                registro[x] = int(asignacion[0])
            except:
                registro[x] = asignacion[0]     #Puede contener siglas meteorológicas como BECMG, NOSIG o no hay registro '-'
        else:
            registro[x] = None                #Si está en otra unidad el dato, devuelve None
        
    return registro


def registros_dia(estacion: str, fecha: str) -> dict:
    # pre: estacion y fecha son str
    # post: devuelve un diccionario con los datos metereologicos de ese día y estación
    assert type(estacion) == type(fecha) == str and len(fecha) == 8, 'Debe ingresar los datos en str y la fecha en formato AAAAMMDD'
    nombre_fecha = formatear_fecha(fecha)
    contenido_url = requests.get('https://www.tutiempo.net/registros/' + estacion + '/' + nombre_fecha + '.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")
    return registros_tabla(tabla_dia)

def clima_anho(estacion: str, anho: str, mes_ini: int, mes_fin: int):
    # pre: anho es un str, mes_ini y mes_fin son enteros
    # post: guarda en el archivo 'AAAA.txt', en cada renglón, los datos del clima de cada día estación desde mes_ini hasta el mes_fin
    tipos = (type(anho) == str and type(mes_ini) == type(mes_fin) == int)
    condiciones = 2014 <= int(anho) <= 2021 and 1 <= mes_ini <= 12 and 1 <= mes_fin <= 12    #Los datos del año completo en tu tiempo son a partir del 2014
    assert tipos and condiciones, 'Debe ingresar un str entre 2014 y 2021, y dos números entre 1 y 12'
    
    fechas = fechas_desde(anho, mes_ini, mes_fin)
    nombre = ('{}.txt'.format(anho))
    nombre = DIR + nombre
    archivo = open(nombre,'w')   
    for dia in fechas:
        diccionario = {dia: registros_dia(estacion, dia)}
        dicc_json = json.dumps(diccionario)
        archivo.write(dicc_json + '\n')
    archivo.close()


def fechas_desde(anho: str, mes_ini: int, mes_fin: int) -> list:
    # pre: anho es un str, mes_ini y mes_fin son enteros
    # post: devuelve una lista con todas las fechas con formato AAAAMMDD desde mes_ini hasta mes_fin
    tipos = (type(anho) == str and type(mes_ini) == type(mes_fin) == int)
    condiciones = 1 <= mes_ini <= 12 and 1 <= mes_fin <= 12
    assert tipos and condiciones, 'Debe ingresar un año en str y dos números entre 1 y 12'
    
    DIAS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (int(anho) % 4 == 0 and int(anho) % 100 != 0) or (int(anho) % 100 == 0 and int(anho) % 400 == 0):     #Comprueba que no sea un año bisiesto
        DIAS = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    fechas = []
    meses_entre = 0   
    for dia in DIAS[mes_ini -1 : mes_fin]:
        for numero in range(dia):
            if numero < 9:
                dia = str(0) + str(numero +1)                #El dia debe tener longitud 2 si o si
            else:
                dia = str(numero + 1)
            if (mes_ini + meses_entre) < 10:
                mes = str(0) + str(mes_ini + meses_entre)    #El mes debe tener longitud 2 si o si
            else: 
                mes = str(mes_ini + meses_entre)
            fecha = str(anho) + mes + dia
            fechas.append(fecha)
        meses_entre = meses_entre + 1
    return fechas 


def temp_min_max(estacion, anho):
    # pre: estacion es el codigo iaci de una estación meteorológica y anho en un str
    # post: devuelve un diccionario con las temperaturas máximas y minimas de cada mes
    assert type(estacion) == type(anho) == str, 'Debe ingersar los datos en str'
    MESES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    temperaturas_anuales = {}
    temperaturas_mes = []
    mes = '01'
    # archivo = open('/content/drive/MyDrive/2018.txt', 'r')    #Es el archivo con todos los datos del 2018 en estación
    archivo = open(DIR + '2018.txt', 'r')    #Es que hizo el profe para poder ver que anda
    linea = archivo.readline()
    fechas = fechas_desde(anho, 1, 12)          #Lista con todas las fechas del año ingresado
    while linea != '':
        x = json.loads(linea)
        dia = [y for y in x.keys()][0]          #Devuelve el elemento como str, no como una lista de un único elemento
        if dia [4:6] != mes:
            temperaturas_anuales[MESES[int(mes)-1]] = {'Max': max(temperaturas_mes), 'Min': min(temperaturas_mes)}
            mes = dia[4:6]
            temperaturas_mes = []               #Se inicializa la lista para guardar los datos del nuevo mes
        if dia in fechas:
            claves = [y for y in x[dia].keys()]
            for hora in claves:
                temp = x[dia][hora]['temp']     #Extrae cual fue la temperatura en ese día y hora
                try: 
                    temperaturas_mes.append(int(temp))
                except:
                    None               #Sino se puede convertir a int es porque el dato es N/D, que implica que no existe la medición
        linea = archivo.readline()
    archivo.close()
    temperaturas_anuales[MESES[int(mes)-1]] = {'Max': max(temperaturas_mes), 'Min': min(temperaturas_mes)}   #Agrego el mes de diciembre
    return temperaturas_anuales
    

def temp_max(estacion, mes_ini, mes_fin):
    # pre: estacion es un str, mes_ini y mes_fin son enteros
    # post: devuelve el promedio de las máximas temperaturas de los dias entre mes_ini y mes_fin
    tipos = type(mes_ini) == type(mes_fin) == int
    condicion = 1 <= mes_ini <= 12 and 1 <= mes_fin <= 12
    assert tipos and condicion, 'Debe ingresar un str y dos números entre 1 y 12'

    # archivo = open('/content/drive/MyDrive/2018.txt', 'r')    #Es el archivo con todos los datos del 2018 en estación
    archivo = open(DIR + '2018.txt', 'r')    #Es que hizo el profe para poder ver que anda
    temperaturas_maximas = []
    linea = archivo.readline()
    fechas = fechas_desde('2018', mes_ini, mes_fin)         #Lista con todas las fechas entre mes_ini y mes_fin
    while linea != '':
        x = json.loads(linea)
        dia = [y for y in x.keys()][0]                      #Devuelve el elemento como str, no como una lista de un único elemento
        if dia in fechas:
            claves = [y for y in x[dia].keys()]
            temperaturas = []
            for hora in claves:
                temp = x[dia][hora]['temp']                 #Extrae cual fue la temperatura en ese día y hora
                try: 
                    temperaturas.append(int(temp))
                except:
                    None               #Sino se puede convertir a int es porque el dato es N/D, que implica que no existe la medición
            temperaturas_maximas.append(max(temperaturas))
        linea = archivo.readline()
    archivo.close()
    promedio = sum(temperaturas_maximas) / len(temperaturas_maximas)
    return promedio


def dir_viento(estacion, mes_ini, mes_fin):
    # pre: estacion es un str, mes_ini y mes_fin son enteros
    # post: devuelve la dirección del viento predominante durante la primavera del año 2018 en estacion
    tipos = type(mes_ini) == type(mes_fin) == int
    condiciones = 1 <= mes_ini <= 12 and 1 <= mes_fin <= 12
    assert tipos and condiciones, 'Debe ingresar un str y dos números entre 1 y 12'
    
    # archivo = open('/content/drive/MyDrive/2018.txt', 'r')    #Es el archivo con todos los datos del 2018 en estación
    archivo = open(DIR + '2018.txt', 'r')    #Es que hizo el profe para poder ver que anda
    contenido = []
    linea = archivo.readline()
    fechas = fechas_desde('2018', mes_ini, mes_fin)    #Lista con todas las fechas entre mes_ini y mes_fin
    while linea != '':
        x = json.loads(linea)
        dia = [y for y in x.keys()][0]                 #Devuelve el elemento como str, no como una lista de un único elemento
        if dia in fechas:
            claves = [y for y in x[dia].keys()]
            for hora in claves:
                direccion = x[dia][hora]['dir']        #Extrae cual fue la dirección del viento en ese día y hora
                contenido.append(direccion)
        linea = archivo.readline()
    archivo.close()
    repeticiones = {contenido.count(i): i for i in contenido}   #Clave: cant de repeticiones de la dirección del viento, valor: dirección del viento
    
    return repeticiones[max(repeticiones.keys())]


def main():
    estacion, anho = 'mslp', '2018' # El Salvador
    # clima_anho(estacion, anho, 1, 12)
    max_min_anual = temp_min_max(estacion, anho )
    print(max_min_anual)   

    prom_primavera = temp_max(estacion, 9, 12)
    print(prom_primavera)

    dir_primavera = dir_viento(estacion, 9, 12)
    print(dir_primavera)

# RUN

if __name__ == '__main__':
    main()