import requests
from bs4 import BeautifulSoup
import json

CLAVES = ['hora', 'desc', 'temp', 'dir', 'vel', 'hum', 'pres'] 
DIR = './2021/tareas/lopez/'

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
    if tabla == None:
        registros = {'None' : 'none'}
    else    :
        for fila_tabla in tabla.findAll('tr'):
            registro = registro_fila_tabla(fila_tabla)    
            if len(registro) != 0:
                hora = registro.pop('hora')
                hh = int(hora[:2])
                registro = eliminar_unidades(registro)
                registros[hh] = registro                
    return registros


def registros_dia(estacion: str, fecha: str) -> dict:
    nombre_fecha = formatear_fecha(fecha)
    contenido_url = requests.get('https://www.tutiempo.net/registros/' + estacion + '/' + nombre_fecha + '.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")
    return registros_tabla(tabla_dia)


def formatear_fecha(fecha: str) -> str:
    # pre:  fecha es una fecha en el formato 'AAAAMMDD'
    # post: devuelve la fecha  en el foma dia-nombre del mes-año
    mes=['','enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    # resultado = fecha[6:8] + '-' + mes[int(fecha[4:6])] + '-' + fecha[0:4] # Corrección: los días de un dígito deben permanecer de un dígito
    resultado = str(int(fecha[6:8])) + '-' + mes[int(fecha[4:6])] + '-' + fecha[0:4] # agregado por mi
    return resultado


def eliminar_unidades(registro: dict):
    # pre:  recibe un diccionario tipo  {'desc': 'Despejado', 'temp': '13°', 'dir': 'Noroeste', 'vel': '7 km/h', 'hum': '88%', 'pres': '1015 hPa'}
    # post: modifica el propio diccionario tipo   {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015}
    if registro['temp'][0:len(registro['temp'])-1] != 'N/D':
        registro['temp'] = int(registro['temp'][0:len(registro['temp'])-1])
    if registro['hum'][0:len(registro['hum'])-1] != 'N/D':
        registro['hum'] = int(registro['hum'][0:len(registro['hum'])-1])
    if registro['pres'][0:len(registro['pres'])-4] != '-':
        registro['pres'] = int(registro['pres'][0:len(registro['pres'])-4])
    return registro


def clima_anho(estacion, anho: str, mes_ini: int, mes_fin: int):
    archivo = open(DIR + anho + '.txt', 'w')
    registros = {}
    for i in range(mes_ini,mes_fin+1):
        print('mes:', i)
        if i == 1 or i == 3 or i == 5 or i == 7 or i == 8 :
            for j in range(1,32):
                if j<10:
                    registros[anho + '0' + str(i) + '0' + str(j)] = registros_dia(estacion, anho + '0' + str(i) + '0' + str(j))
                    # archivo.write(str(registros[anho + '0' + str(i) + '0' + str(j)]) + '\n') # Corrección: no guardar así
                    archivo.write(json.dumps({anho + '0' + str(i) + '0' + str(j): registros[anho + '0' + str(i) + '0' + str(j)]}) + '\n') # Agregado mio
                else:
                    registros[anho + '0' + str(i) + str(j)] = registros_dia(estacion, anho + '0' + str(i) + str(j))
                    # archivo.write(str(registros[anho + '0' + str(i) + str(j)]) + '\n')   Corrección: no guardar así 
                    archivo.write(json.dumps({anho + '0' + str(i) + str(j) : registros[anho + '0' + str(i) + str(j)]}) + '\n')
        elif i == 10 or i == 12:        
            for j in range(1,32):
                if j<10:
                    registros[anho + str(i) + '0' + str(j)] = registros_dia(estacion, anho + str(i) + '0' + str(j))
                    archivo.write(json.dumps({anho + str(i) + '0' + str(j) : registros[anho + str(i) + '0' + str(j)]}) + '\n')
                else:
                    # registros[anho + str(i) + str(j)] = registros_dia(anho + str(i) + str(j)) # Corrección: falta la estación
                    registros[anho + str(i) + str(j)] = registros_dia(estacion, anho + str(i) + str(j)) # Agregado mio
                    archivo.write(json.dumps({anho + str(i) + str(j) : registros[anho + str(i) + str(j)]}) + '\n')
        elif i == 2:
            for j in range(1,28):
                if j<10:
                    registros[anho + '0' + str(i) + '0' + str(j)] = registros_dia(estacion, anho + '0' + str(i) + '0' + str(j))
                    archivo.write(json.dumps({anho + '0' + str(i) + '0' + str(j) : registros[anho + '0' + str(i) + '0' + str(j)]}) + '\n')
                else:
                    registros[anho + '0' + str(i) + str(j)] = registros_dia(estacion, anho + '0' + str(i) + str(j))
                    archivo.write(json.dumps({anho + '0' + str(i) + str(j) : registros[anho + '0' + str(i) + str(j)]}) + '\n') 
        elif i == 11:
            for j in range(1,31):
                if j<10:
                    registros[anho + str(i) + '0' + str(j)] = registros_dia(estacion, anho + str(i) + '0' + str(j))
                    archivo.write(json.dumps({anho + str(i) + '0' + str(j) : registros[anho + str(i) + '0' + str(j)]}) + '\n')
                else:
                    registros[anho + str(i) + str(j)] = registros_dia(estacion, anho + str(i) + str(j))
                    archivo.write(json.dumps({anho + str(i) + str(j) : registros[anho + str(i) + str(j)]}) + '\n')                 
        else:
            for j in range(1,31):
                if j<10:
                    registros[anho + '0' + str(i) + '0' + str(j)] = registros_dia(estacion, anho + '0' + str(i) + '0' + str(j))
                    archivo.write(json.dumps({anho + '0' + str(i) + '0' + str(j) : registros[anho + '0' + str(i) + '0' + str(j)]}) + '\n')
                else:
                    registros[anho + '0' + str(i) + str(j)] = registros_dia(estacion, anho + '0' + str(i) + str(j))
                    archivo.write(json.dumps({anho + '0' + str(i) + str(j) : registros[anho + '0' + str(i) + str(j)]}) + '\n')                            
    archivo.close()


def temp_min_max(estacion, anho):
    for i in range(1,13):
        # txt=clima_anho(estacion, anho, i, i)  # Corrección: 1 ) clima_anho()  no devuelve nada. 2) # Corrección: clima_anho() se debe correr una sola vez con todos los meses. 
        texto=open(DIR + anho + '.txt', 'r')
        dias = []
        max = 0
        min = 1000
        for linea in texto:
            # dias = dias.append(json.loads(linea)) # Corregir: dias.append() devuelve None,  hay que poner directamente dias.append()
            dia_act = json.loads(linea)
            for u in dia_act:
                dias.append(dia_act[u]) # Agregadas por mi
        print('aaa',dias[0])
        for j in range(len(dias)):
            print(j)    
            for hora in range(24):
                if dias[j][str(hora)]['temp'] > max:
                    max = dias[j][str(hora)]['temp']
                if dias[j][str(hora)]['temp'] < min:
                    min = dias[j][str(hora)]['temp']
        print('Temperatura maxima mes ',i , ':', max)
        print('Temperatura minima mes ',i , ':', min)
        texto.close() # Corrección: siempre se debe cerrar (línea agregada por mi).


def temp_max(estacion, mes_ini, mes_fin):
    suma =    0
    dias = 0 
    for i in range(mes_ini,mes_fin+1):
        # txt=clima_anho(estacion, '2018', i, i)  # Corrección: 1 ) clima_anho()  no devuelve nada. 2) # Corrección: clima_anho() se debe correr una sola vez con todos los meses. 
        texto=open(DIR + '2018.txt', 'r')

        # dias = [] # Corrección: la variable dias a veces es entera y a veces es lista. Está mal.
        dias_lst = [] # Agregado por mi 
        for linea in texto:
            # dias = dias.append(json.loads(linea)) # Corregir: dias.append() devuelve None,  hay que poner directamente dias.append()
            dias_lst.append(json.loads(linea)) # Agregada por mi
        for j in range(len(dias_lst)):  # modificado por mi
            max = 0
            for hora in range(24):
                if dias_lst[j][str(hora)]['temp'] > max:  # modificado por mi
                    max = dias_lst[j][str(hora)]['temp']  # modificado por mi
            dias = dias + 1            
            suma = suma + max     
        # promedio = suma / max  # Corrección: se debe dividir por la cantidad de mediciones
        promedio = suma / dias # Agregada por mi
        texto.close() # Corrección: siempre se debe cerrar (línea agregada por mi).
        return promedio 



def dir_viento(estacion, mes_ini, mes_fin):
    dias = []
    for i in range(mes_ini,mes_fin+1):
        txt=clima_anho(estacion, '2018', i, i)
        texto=open(DIR + '2018.txt', 'r')
        viento = []
        dias = []
        for linea in texto:
            # dias = dias.append(json.loads(linea)) # Corregir: dias.append() devuelve None,  hay que poner directamente dias.append()
            dias.append(json.loads(linea)) # agregado por mi
        for j in range(len(dias)):
            for hora in range(24): 
                dias.append(dias[j][str(hora)]['dir'])
    direcciones = ['Norte', 'Noroeste', 'Oeste', 'Suroeste', 'Sur', 'Sureste', 'Este', 'Noreste']
    max = 0
    # for z in len(direcciones): # Corregir: esto está mal
    for z in range(len(direcciones)): # Agregado por mi
        if dias.count(direcciones[z]) > max :
            max = dias.count(direcciones[z])            
    return max


def main():
    estacion, anho = 'legr', '2018' # Granada 
    # print(registros_dia(estacion, '20180103'))
    # clima_anho(estacion, anho, 1, 12)
    temp_min_max(estacion, anho)
    temp_max(estacion, 1, 12)
    dir_viento(estacion, 1, 12)

# RUN

if __name__ == '__main__':
    main()