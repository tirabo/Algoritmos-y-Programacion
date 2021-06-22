import requests
from bs4 import BeautifulSoup
import json # Importado para usar en los ejercicios 2 y 3


CLAVES = ['hora', 'desc', 'temp', 'dir', 'vel', 'hum', 'pres'] 
DIR = './2021/tareas/mercado_alcoba/'

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


def formatear_fecha(fecha: str) -> str:
    # pre:  fecha es una fecha en el formato 'AAAAMMDD'
    # post: devuelve la fecha  en el foma dia-nombre del mes-año
    lista_fecha = fecha
    anho = lista_fecha[:4]
    mes = int(lista_fecha[4:6])
    dia = lista_fecha[6:8]
    MESES = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
    return dia + '-' + MESES[mes - 1] + '-' + anho


def eliminar_unidades(registro: dict):
    # pre:  recibe un diccionario tipo  {'desc': 'Despejado', 'temp': '13°', 'dir': 'Noroeste', 'vel': '7 km/h', 'hum': '88%', 'pres': '1015 hPa'}
    # post: modifica el propio diccionario tipo   {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015}
    new_registro = {}
    lista_claves = registro.keys()
    claves_con_units = ['temp','vel','hum','pres']
    unidades_a_quitar = ['°','km/h','%','hPa']
    i = 0
    for clave in lista_claves:
        if clave in claves_con_units:   
            lista_split = registro[clave].split(unidades_a_quitar[i])
            new_registro[clave] = lista_split[0]
            i = i + 1
        else:
            new_registro[clave] = registro[clave]
    return new_registro


def es_bisiesto(anho: int) -> bool:
    #pre: anho es entero positivo
    #post: devuelve True si annio es bisiesto segun el calendario gregoriano
    return anho % 400 == 0 or (anho % 4 == 0 and not(anho % 100 == 0))


# Funciones Redefinidas:
def registros_dia(estacion: str, fecha: str) -> dict:
    nombre_fecha = formatear_fecha(fecha)
    contenido_url = requests.get('https://www.tutiempo.net/registros/'+ estacion + '/' + nombre_fecha + '.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")
    clave_numerica = registros_tabla(tabla_dia).keys()
    registros_sin_units = {}
    for clave in clave_numerica:
        registros_sin_units[clave] = eliminar_unidades(registros_tabla(tabla_dia)[clave])
    
    return registros_sin_units


def clima_anho(estacion: str, anho: str, mes_ini: int, mes_fin: int):
    archivo_registro = open(DIR + estacion + anho +'.txt','w') #creo un archivo con un nombre nuevo acorde a los registros obtenidos
    #Lista de meses que necesito para buscar los datos del clima 
    MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre',
            'octubre', 'noviembre', 'diciembre']
    MESES_NRO = ['01','02','03','04','05','06','07','08','09','10','11','12']
    DIA_ANHO = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    DIA_ANHO_BIS = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    meses_entre = MESES[mes_ini-1:mes_fin]
    if es_bisiesto(int(anho)):
        dias_entre = DIA_ANHO_BIS[mes_ini-1:mes_fin]
    else: 
        dias_entre = DIA_ANHO[mes_ini-1:mes_fin]
    
    #Procesamiento para escribir en el archivo_registro creado anteriormente
    registro_clima_anho = {}
    for mes in meses_entre:
        idmes = meses_entre.index(mes)
        nro_dias = dias_entre[idmes]
        for dia in range(1, nro_dias + 1):
            registro_clima_anho = {}
            registro_clima_anho[anho + MESES_NRO[MESES.index(mes)]  + str(dia).zfill(2)] = registros_dia(estacion ,anho + MESES_NRO[MESES.index(mes)] + str(dia))
            archivo_registro.write(json.dumps(registro_clima_anho)+'\n')
    archivo_registro.close()

    return archivo_registro


def temp_min_max(estacion, anho):
    #Creacion del archivo registros por un año
    # clima_anho(estacion,anho,1,12) # NOTA: un vez creado el archivo se puede comentar esta linea de codigo para evitar crearlo de nuevo y hacer pruebas # Corrección:  en realida debe correrse clima_anho() independientemente
    dias_del_anho = []
    
    #apertura del archivo
    datos_clima = open(DIR + estacion + anho + '.txt','r')
    
    #Procesamiento para obtener una lista con todas las temperaturas de un año completo y despues buscar la maxima y la minima
    temp_max_min = []
    for linea_i in datos_clima:  #recorre todas las lineas del archivo del registro anual (aprox 365 lineas)
        dias_del_anho.append(json.loads(linea_i)) #convierte un string de diccionario a diccionario python
    for i in range(len(dias_del_anho)):
        fecha_i = dias_del_anho[i]
        clave_fecha = fecha_i.keys()
        for key_fecha in clave_fecha:
            dic_hora = fecha_i[key_fecha]
            clave_hora = dic_hora.keys()
            for key_hora in clave_hora:
                temp_str = dic_hora[key_hora]['temp']
                if temp_str != 'N/D':
                    temp_parcial = int(dic_hora[key_hora]['temp'])
                    temp_max_min.append(temp_parcial) # Corrección: con esto hacés una lista hora por hora de las temperaturas del año. Eso es muy difícil de manejar.  
                    # print(i, key_fecha, key_hora, temp_parcial)
                else:
                    temp_max_min.append(0)
    print(len(temp_max_min))
    #POST- PROCESO PARA BUSCAR LO QUE SE PIDE:
    dias_acu2018 = [31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365] #dias del año acumulados por mes
    mediciones_acu_mes = [744, 1416, 2160, 2880, 3624, 4344, 5088, 5832, 6552, 7296, 8016, len(temp_max_min)] # mediciones acumuladas por mes, cada dia realizan 24 mediciones
    #Procesamiento para calcular la temperatura maxima de cada mes almacenados en la lista maxi_temp
    temp_mes = [] #lista para almacenar todas las temperaturas de un mes
    maxi_temp= [] #lista para almacenar las temperaturas maximas de cada mes del año
    dia_ini = 0
    for dias_ac in mediciones_acu_mes:
        for i in range(dia_ini, dias_ac):
            temp_mes.append(temp_max_min[i])
        maxi_temp.append(max(temp_mes))
        dia_ini = dias_ac
    #Procesamiento para calcular la temperatura minima de cada mes almacenados en la lista min_temp
    temp_mes = [] #lista para almacenar todas las temperaturas de un mes
    min_temp= [] #lista para almacenar las temperaturas minimas de cada mes del año
    dia_ini = 0
    for dias_ac in mediciones_acu_mes:
        for i in range(dia_ini, dias_ac):
            temp_mes.append(temp_max_min[i])
        min_temp.append(min(temp_mes))
        dia_ini = dias_ac
    datos_clima.close()   
    #retorna una tupla con listas donde cada elemento de la lista representa la temperatura maxi o min de cada mes de enero a dicimembre
    return maxi_temp, min_temp


def temp_max(estacion, mes_ini, mes_fin):
    #Creacion del archivo registros por una temporada 
    # clima_anho(estacion,'2018',mes_ini,mes_fin) #NOTA: un vez creado el archivo se puede comentar esta linea de codigo para evitar crearlo de nuevo
    #apertura del archivo # Corrección:  
    datos_clima = open(DIR + estacion + '2018' + '.txt','r')
    
    #Procesamiento para obtener una lista con todas las temperaturas de la primavera y despues calcular el promedio
    dias_primavera = []
    temp_max = []
    temps_diaria = []
    for linea_i in datos_clima:  #recorre todas las lineas del archivo del registro anual (aprox 365 lineas)
        dias_primavera.append(json.loads(linea_i)) #convierte un string de diccionario a diccionario python
    for i in range(365-len(dias_primavera), 366 - 10): #dias del 21 de septiembre al 21 de diciembre
        fecha_i = dias_primavera[i-(365-len(dias_primavera))]
        clave_fecha = fecha_i.keys()
        for key_fecha in clave_fecha:
            dic_hora = fecha_i[key_fecha]
            clave_hora = dic_hora.keys()
            for key_hora in clave_hora:
                temp_str = dic_hora[key_hora]['temp']
                if  temp_str != '-' and temp_str != 'N/D':
                    temp_parcial = int(dic_hora[key_hora]['temp'])
                    temps_diaria.append(temp_parcial) 
            temp_max.append(max(temps_diaria)) #rescato el valor maximo de las lista temps_diarias antes de pasar a la siguiente fecha       
    datos_clima.close()   
    #retorna el promedio de las temperaturas maximas de primavera usando las funciones sum() y len() para listas  
    return sum(temp_max)/len(temp_max)


def dir_viento(estacion, mes_ini, mes_fin):
    #post : retorna la direccion del viento que predomina en primavera como un string
    #Utiliza el mismo archivo creado para temp_max
    # clima_anho(estacion,'2018',mes_ini,mes_fin)  # Corrección:  en realida debe correrse clima_anho() independientemente

    #apertura del archivo
    datos_clima = open(DIR + estacion + '2018' + '.txt','r')
    
    #Procesamiento para obtener una lista con todas las direcciones del viento de la primavera y despues calcular el viento predominante 
    dias_primavera = []
    dir_viento = []
    for linea_i in datos_clima:  #recorre todas las lineas del archivo datos_clima correspondiente a la primavera
        dias_primavera.append(json.loads(linea_i)) #convierte un string de diccionario a diccionario python
    for i in range(365-len(dias_primavera), 366 - 10): #dias del 21 de septiembre al 21 de diciembre
        fecha_i = dias_primavera[i-(365-len(dias_primavera))]
        clave_fecha = fecha_i.keys()
        for key_fecha in clave_fecha:
            dic_hora = fecha_i[key_fecha]
            clave_hora = dic_hora.keys()
            for key_hora in clave_hora:
                viento_parcial = dic_hora[key_hora]['dir']
                dir_viento.append(viento_parcial)
    
    #Procesamiento para encontrar el viento predominante de la lista dir_viento usando la funcion count() para listas
    viento_predominante = None
    cuanto_viento = 0
    for viento in dir_viento:
        if dir_viento.count(viento) > cuanto_viento:
            cuanto_viento = dir_viento.count(viento)
            viento_predominante = viento
    datos_clima.close()   
    
    return viento_predominante



def main():
    estacion, anho = 'sllp', '2018' # La Paz 
    # clima_anho(estacion, anho, 1, 12)
    print(temp_min_max(estacion, anho))
    print('La temperatura maxima promedio de Primavera 2018 en La Paz-Bolivia es: ',temp_max('sllp',9,12)) 
    print('El viento predominante en Primavera de 2018 en La Paz-Bolivia es: ',dir_viento('sllp',9,12))


# RUN

if __name__ == '__main__':
    main()