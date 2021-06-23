import requests
from bs4 import BeautifulSoup
import json

# Código ordenado con todas las funciones predefinidas hasta ahora 

CLAVES = ['hora', 'desc', 'temp', 'dir', 'vel', 'hum', 'pres'] 
DIR = './2021/tareas/tirabo/'

def registro_fila_tabla(fila_tabla) -> dict: # procesa una fila de la tabla, devuelve un diccionario con las mediciones registradas en esa fila
    try:
        registro = {}
        celdas_fila = fila_tabla.findAll('td')
        i = 0
        for celda in celdas_fila: # recorre las celdas de la fila correspondiente a una toma de mediciones
            if celda.img != None: # si existe el tag 'img'
                input_tag = celda.img['title'] # recupera en el tag 'img' el valor del atributo 'title'
                registro[CLAVES[i]] = input_tag # dirección del viento
                i = i + 1
            registro[CLAVES[i]] = celda.text
            i = i + 1
        if len(registro) != 0:
            eliminar_unidades(registro)
    except:
        registro = {}
    return registro

def registros_tabla(tabla) -> dict:          # procesa una tabla, devuelve un diccionario de registros contenidos en esa tabla
    try:
        registros = {}
        for fila_tabla in tabla.findAll('tr'):
            registro = registro_fila_tabla(fila_tabla)
            if len(registro) != 0:
                hora = registro.pop('hora')
                hh = int(hora[:2])
                registros[hh] = registro
    except:
        registros = {}
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
    if tabla_dia == None:
        print('La tabla de ',estacion, ' del día ', fecha,' es None')
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


# Calcular el promedio de temperaturas máximas diarias durante la primavera del año 2018 en la ciudad elegida.
def temp_max(estacion, fecha_ini, fecha_fin):
    # post: calcula el promedio de temperaturas máximas diarias entre fecha_ini y fecha_fin
    assert fecha_ini[:4] == fecha_fin[:4], 'Las fechas deben ser del mismo año'
    anho = fecha_ini[:4]
    datos = leer_medidas(estacion, anho) 
    # print('len(datos)',len(datos))
    t_max_list = [] # lista temperaturas máximas por dia
    for dia in datos:
        #print(dia, primavera(dia))
        if fecha_ini <= dia <= fecha_fin:
            #print(dia,' ',end='')
            t_max_dia = -100
            for hora in datos[dia]:
                if datos[dia][hora]['temp'] != None:
                    t_max_dia = max(t_max_dia, datos[dia][hora]['temp'])
            if t_max_dia != None:
                t_max_list.append(t_max_dia)
                # print(t_max_dia)
    t_max_prom =  sum(t_max_list) / len(t_max_list)
    print('El promedio de temperaturas máximas entre '+ fecha_ini + ' y ' + fecha_fin + ' en '+ estacion + ' fue : '  + str(round(t_max_prom,1)))
    return t_max_prom


# Esto es la moda de una lista (de las direcciones del viento). Se puede hacer con alguna función de alguna biblioteca.
# pero lo hacemos "a mano"
def moda(lista: list[str]):
    # Post: calcula la moda de una lista
    conj_val = set(lista) # conjunto de posibles valores
    moda_lista = ['', 0]
    for valor in conj_val:
        cant = lista.count(valor)
        if cant > moda_lista[1]:
            moda_lista = [valor, cant]
    return moda_lista[0]


def dir_viento(estacion, fecha_ini, fecha_fin):
    # post: calcula la dirección del viento predominante entre fecha_ini y fecha_fin
    assert fecha_ini[:4] == fecha_fin[:4], 'Las fechas deben ser del mismo  año'
    anho = fecha_ini[:4]
    datos = leer_medidas(estacion, anho) 
    t_dir_list = [] # lista direcciones del viento por hora
    for dia in datos:
        if fecha_ini <= dia <= fecha_fin:
            for hora in datos[dia]:
                if datos[dia][hora]['dir'] != None:
                    t_dir_list.append(datos[dia][hora]['dir'])
    print('La dirección del viento predominantes entre '+ fecha_ini + ' y ' + fecha_fin + ' en '+ estacion + ' fue : ' + moda(t_dir_list))
    return moda(t_dir_list)


def main():
    primavera_sur = ('20180921', '20181220')
    primavera_nor = ('20180321', '20180620')
    # estacion, anho = 'eddl', '2018' # Düsseldorf
    # estacion, anho = 'saco', '2018' # Córdoba
    # estacion, anho = 'eddb', '2018' # Berlín
    # estacion, anho = 'mmun', '2018' # Cancún
    estacion, anho = 'rjtt', '2018' # Tokio
    # estacion, anho = 'mslp', '2018' # El Salvador
    #estacion, anho = 'cwdk', '2018' # Claresholm
    # estacion, anho = 'sazs', '2018' # San Carlos de Bariloche
    # estacion, anho = 'fmmi', '2018' # Antananarivo / Ivato (Madagascar)
    # estacion, anho = 'legr', '2018' # Granada 
    # estacion, anho = 'sbrj', '2018' # Rio de Janeiro
    # estacion, anho = 'sllp', '2018' # La Paz 
    # estacion, anho = 'mtpp', '2018' # Puerto Príncipe
    # estacion, anho = 'ulli', '2018' # San Petesburgo
    # estacion, anho = 'umkk', '2018' # Kaliningrado
    #clima_anho(estacion, anho, 1, 12)
    temp_min_max(estacion, anho)
    temp_max(estacion, primavera_nor[0], primavera_nor[1])
    dir_viento(estacion, primavera_nor[0], primavera_nor[1])


# RUN

if __name__ == '__main__':
    main()

"""
# Cancún: mmun (Jazmín Caruso Rojo)
La temperaturas máximas por mes en mmun en el año 2018 fueron : [28, 30, 30, 31, 31, 31, 33, 33, 32, 31, 30, 30]
La temperaturas mínimas por mes en mmun en el año 2018 fueron : [12, 14, 15, 16, 19, 23, 23, 23, 23, 20, 18, 13]
El promedio de temperaturas máximas en primavera en mmun en el año 2018 es : 29.03
La dirección del viento predominante durante la primavera del año 2018 en mmun es : Sureste

# Düsseldorf: eddl (Julieta Berenice Cerdá Molina)
La temperaturas máximas por mes en eddl en el año 2018 fueron : [14, 8, 16, 29, 30, 29, 36, 36, 31, 27, 19, 14]
La temperaturas mínimas por mes en eddl en el año 2018 fueron : [-1, -9, -8, -1, 5, 9, 11, 8, 2, 2, -2, -3]
El promedio de temperaturas máximas en primavera en eddl en el año 2018 es : 20.26
La dirección del viento predominante durante la primavera del año 2018 en eddl es : Suroeste

# Córdoba: saco (ejemplo)
La temperaturas máximas por mes en saco en el año 2018 fueron : [37, 38, 37, 35, 29, 27, 26, 31, 38, 37, 35, 37]
La temperaturas mínimas por mes en saco en el año 2018 fueron : [11, 8, 6, 10, 3, -5, -3, -4, 1, 3, 10, 10]
El promedio de temperaturas máximas en primavera en saco en el año 2018 es : 22.82
La dirección del viento predominante durante la primavera del año 2018 en saco es : Nordeste

# Berlín: eddb (ejemplo)
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

# Claresholm (Alberta, Canada): 'cwdk' (Claire Marie Fahy)
La temperaturas máximas por mes en cwdk en el año 2018 fueron : [11, 5, 8, 28, 30, 28, 33, 39, 30, 24, 14, 12]
La temperaturas mínimas por mes en cwdk en el año 2018 fueron : [-37, -34, -26, -23, -1, 4, 4, 1, -3, -9, -19, -22]
El promedio de temperaturas máximas en primavera en cwdk en el año 2018 es : 14.48
La dirección del viento predominante durante la primavera del año 2018 en cwdk es : Norte

# San Carlos de Bariloche: 'sazs' (Emmanuel Darío Gonzalez Gomez)
La temperaturas máximas por mes en sazs en el año 2018 fueron : [32, 33, 28, 24, 17, 14, 9, 14, 18, 20, 25, 29]
La temperaturas mínimas por mes en sazs en el año 2018 fueron : [0, 0, -2, -4, -6, -11, -9, -7, -6, -5, -3, -1]
El promedio de temperaturas máximas en primavera en sazs en el año 2018 es : 15.18
La dirección del viento predominante durante la primavera del año 2018 en sazs es : Noroeste

# Antananarivo / Ivato (Madagascar): 'fmmi' (Carlos Alberto Gómez Prado)
La temperaturas máximas por mes en fmmi en el año 2018 fueron : [30, 30, 29, 29, 30, 26, 26, 28, 28, 31, 32, 31]
La temperaturas mínimas por mes en fmmi en el año 2018 fueron : [14, 16, 15, 11, 9, 5, 6, 6, 8, 10, 15, 14]
El promedio de temperaturas máximas en primavera en fmmi en el año 2018 es : 27.56
La dirección del viento predominante durante la primavera del año 2018 en fmmi es : Sureste

# Granada: 'legr' (Simon Noe Lopez)
La temperaturas máximas por mes en legr en el año 2018 fueron : [21, 20, 23, 29, 28, 40, 38, 41, 38, 31, 20, 24]
La temperaturas mínimas por mes en legr en el año 2018 fueron : [-3, -5, 0, 2, 1, 10, 13, 14, 13, 0, -1, -2]
El promedio de temperaturas máximas en primavera en legr en el año 2018 es : 22.36
La dirección del viento predominante durante la primavera del año 2018 en legr es : Variable

# Rio de Janeiro: 'sbrj' (Luciana Gimena Ruiz)
La temperaturas máximas por mes en sbrj en el año 2018 fueron : [37, 38, 35, 33, 33, 31, 33, 33, 32, 33, 34, 35]
La temperaturas mínimas por mes en sbrj en el año 2018 fueron : [20, 21, 24, 20, 17, 19, 17, 17, 18, 19, 18, 18]
El promedio de temperaturas máximas en primavera en sbrj en el año 2018 es : 28.7
La dirección del viento predominante durante la primavera del año 2018 en sbrj es : Sureste

# La Paz: 'sllp' (Javier Mercado Alcoba)
La temperaturas máximas por mes en sllp en el año 2018 fueron : [19, 17, 18, 19, 18, 16, 17, 17, 18, 19, 20, 21]
La temperaturas mínimas por mes en sllp en el año 2018 fueron : [2, 1, 1, -2, -6, -5, -7, -6, -6, 0, 2, -2]
El promedio de temperaturas máximas en primavera en sllp en el año 2018 es : 15.97
La dirección del viento predominante durante la primavera del año 2018 en sllp es : Nordeste

# Tokio: 'rjtt' (Ignacio Mercado Blanco)
La temperaturas máximas por mes en rjtt en el año 2018 fueron : [16, 14, 22, 25, 28, 32, 36, 36, 33, 32, 21, 24]
La temperaturas mínimas por mes en rjtt en el año 2018 fueron : [-2, 0, 3, 8, 11, 15, 20, 21, 16, 13, 8, 2]
El promedio de temperaturas máximas en primavera en rjtt en el año 2018 es : 21.88
La dirección del viento predominante durante la primavera del año 2018 en rjtt es : Sur

# Puerto Príncipe: 'mtpp' (María De Los Ángeles Rossi)
La temperaturas máximas por mes en mtpp en el año 2018 fueron : [33, 34, 35, 37, 36, 37, 38, 37, 37, 35, 34, 34]
La temperaturas mínimas por mes en mtpp en el año 2018 fueron : [22, 20, 18, 22, 23, 24, 25, 23, 23, 22, 21, 22]
El promedio de temperaturas máximas en primavera en mtpp en el año 2018 es : 25.59
La dirección del viento predominante durante la primavera del año 2018 en mtpp es : Este

# San Petesburgo : 'ulli' (Pedro Salomone)
La temperaturas máximas por mes en ulli en el año 2018 fueron : [4, 0, 4, 19, 28, 27, 30, 32, 27, 19, 10, 3]
La temperaturas mínimas por mes en ulli en el año 2018 fueron : [-15, -21, -24, -8, 2, 5, 9, 10, 1, -4, -9, -13]
El promedio de temperaturas máximas en primavera en ulli en el año 2018 es : 14.28
La dirección del viento predominante durante la primavera del año 2018 en ulli es : Noroeste

# Kaliningrado: 'umkk' (Axel Ricardo Schliamser)
La temperaturas máximas por mes en umkk en el año 2018 fueron : [9, 5, 9, 26, 29, 29, 31, 31, 29, 22, 16, 9]
La temperaturas mínimas por mes en umkk en el año 2018 fueron : [-13, -21, -18, -3, 2, 8, 12, 10, 4, 1, -9, -10]
El promedio de temperaturas máximas en primavera en umkk en el año 2018 es : 17.29
La dirección del viento predominante durante la primavera del año 2018 en umkk es : Noroeste
"""