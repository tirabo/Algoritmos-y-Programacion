import requests
from bs4 import BeautifulSoup
import json


CLAVES = ['hora', 'desc', 'temp', 'dir', 'vel', 'hum', 'pres'] 

def es_biciesto(anho: int) -> bool:
    return anho % 4 == 0 and (anho % 100 != 0 or anho % 400 == 0)

def conv_mes_str(mes1: int) -> str: #Paso el mes tipo int a tipo str para colocarlo en AAAAMMDD
    if mes1 < 10:
        mes2 = '0' + str(mes1)
    else:
        mes2 = str(mes1)
    return mes2
def conv_dia_str(dia1: int) -> str: #Paso el dia tipo int a tipo str para colocarlo en AAAAMMDD
    if dia1 < 10:
        dia2 = '0' + str(dia1)
    else:
        dia2 = str(dia1)
    return dia2 

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
    
    # pre:    fecha es una fecha en el formato 'AAAAMMDD'
    # post: devuelve la fecha    en el foma dia-nombre del mes-año
    meses = {1:'enero', 2: 'febrero', 3:'marzo', 4:'abril', 5:'mayo', 6:'junio', 7:'julio', 8:'agosto', 9:'septiembre', 10:'octubre', 11:'noviembre', 12:'diciembre'}
    fecha_int = int(fecha)
    dia = fecha_int % 100
    mes = ((fecha_int % 10000) - dia) // 100
    año = (fecha_int - mes - dia) // 10000    
    mes_str = meses[mes]
    return str(dia) +'-'+mes_str+'-'+str(año)

def eliminar_unidades(registro: dict):
    # pre:    recibe un diccionario tipo    {'desc': 'Despejado', 'temp': '13°', 'dir': 'Noroeste', 'vel': '7 km/h', 'hum': '88%', 'pres': '1015 hPa'}
    # post: modifica el propio diccionario tipo     {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015}
    unidades = {'temp':'°', 'vel': ' km/h', 'hum': '%', 'pres':' hPa'}
    claves = unidades.keys()
    registro2 = registro
    #Convierto los valores de los diccionarios en listas.
    for parametro in claves:            #Parametro toma el valor de cada clave     
        updater = list(registro2[parametro])        #updater el es valor de cada clave por ejemplo 16km/h ó 76%
        unidad = list(unidades[parametro])            #Creo una lista con las unidades que tengo que quitar por ejemplo[°] ó    [k, m, /, h]
        for caracter in unidad:         #Elimino los caracteres de unidad de los valores
            updater.remove(caracter)
        updater = ''.join(updater)        #Vuelvo a unir los valores
        registro2.update({parametro: int(updater)}) #Actualizo el diccionario                
    return registro2


def registros_dia(estacion: str, fecha: str) -> dict:
    tablas = {}
    nombre_fecha = formatear_fecha(fecha)
    contenido_url = requests.get('https://www.tutiempo.net/registros/'+ estacion +'/' + nombre_fecha + '.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")
    horas =    registros_tabla(tabla_dia).keys()
    for i in horas:        
        tablas[i] = registros_tabla(tabla_dia)[i]
    return tablas


def dias_del_año(n: str) -> list:
    if es_biciesto(int(n)):
        dia = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else:
        dia = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return dia


def mes_MM(n:int):
    if n < 10:
        mes = '0'+ str(n)
    else:
        mes = str(n)
    return mes

def clima_anho(estacion: str, anho: str, mes_ini: int, mes_fin: int):
    mes_ini2 = mes_ini
    mes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    dia = dias_del_año(anho) #Lista en la que cada elemento es la cantidad de dias de cada mes en la que dia[0] = dias del primer mes del anho 
    mes_ini_str = mes_MM(mes_ini2) #paso el mes al formato MM dado que si es un entero = 2 tengo q pasarlo a string como 02

    #Creo el archivo y agrego el diccionario del primer dia
    fecha_prin = anho + mes_ini_str +'01'

    archivo = open('AAAA.txt', 'w')
    dia_completo1 = registros_dia(estacion, fecha_prin) #Diccionario que contiene la info del clima por hora
    dia_completo2 = {fecha_prin:dia_completo1} #Agrego
    dia_completo2_json = json.dumps(dia_completo2)
    archivo.write(dia_completo2_json)
    archivo.write('\n')
    archivo.close()
    archivo = open('AAAA.txt', 'a')

    for i in dia[mes_ini - 1:mes_fin]:     #Con la notacion slice "recorto" la lista dia y hago que i tome como valor la cantidad de dias de cada mes. Si va desde 2 a 4 (en meses) entonce i toma los valores de la lista [28 ó 29, 31, 30]
        mes_str = conv_mes_str(mes_ini2) #Paso el mes a tipo string en el formato MM
        for j in range(1, i+1):         #j correspone al contador de cada dia         
            dia_str = conv_dia_str(j) #Paso el dia a tipo string en formato DD
            fecha = anho + mes_str + dia_str #Fecha tipo string en formato AAAAMMDD                     
            
            #Creo el diccionario y busco con la fecha AAAAMMDD
            if fecha_prin != fecha:
                dia_completo = {fecha:registros_dia(estacion, fecha)}
                dia_json = json.dumps(dia_completo)
                archivo.write(dia_json)
                archivo.write('\n')             
    mes_ini2 += 1 #Luego que se agregan todos los dias del primer mes, sigue al mes que viene
    archivo.close()


def cual_mes(fecha: str) -> int:  # Valor numerico tipo int del mes
    fecha_int = int(fecha)
    dia = fecha_int % 100
    mes = ((fecha_int % 10000) - dia) // 100
    return mes



#GENERACION DEL ARCHIVO QUE SIRVE PARA LAS 3 FUNCIONES siguientes:
def generar_archivo(estacion, anho, mes_ini, mes_fin):
    clima_anho(estacion, anho, mes_ini, mes_fin)
generar_archivo('rjtt','2018', 1, 12)


def temp_min_max():
    
    archivo = open('AAAA.txt', 'r') 
    d_todos_dias = [] 
    
    #Guardo los diccionarios del archivo
    for linea in archivo: #Creo una lista en la que cada elemento es un diccionario de cada dia
        linea_f = json.loads(linea)
        d_todos_dias.append(linea_f)
    
    #Guardo todas las temperaturas por mes
    meses = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[]} #Aca se guardan todas las temperaturas por mes
    for i in range(len(d_todos_dias)): #Recorre la lista que tiene todos los diccionarios
        for fecha in d_todos_dias[i].keys(): #recorre dia por dia
            horas = d_todos_dias[i][fecha] # Diccionario con las horas
            mes = cual_mes(fecha)
            
            for hora in horas.keys(): #Recorro las horas
                temperatura = horas[hora]['temp'] 
                meses[mes].append(temperatura) #Agrego todas las temperaturas en cada mes de cada hora de cada dia
    
    
    #Pasar el string n° a n entero:
    meses_sin_unidades = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[]}
        
    for k in meses.keys():        
        for t in range(len(meses[k])):
            temp1 = meses[k][t]
            temp2 = temp1.split('°')
            temp2.pop()
            temp_final = int(temp2[0])
            meses_sin_unidades[k].append(temp_final)
    
    #Saco los maximos y minimos
    for i in range(1, 12 + 1):
        if len(meses_sin_unidades[i]) != 0: #Por si no están los datos en la página
            maximo = max(meses_sin_unidades[i])
            minimo = min(meses_sin_unidades[i])
            print('La temperatura máxima del mes {} es: {}°'.format(i, maximo))
            print('La temperatura mínima del mes {} es: {}°'.format(i, minimo))
            print('\n')


def cual_dia(fecha:str) -> int:
    fecha_int = int(fecha)
    dia = fecha_int % 100
    return dia



def temp_max():
    archivo = open('AAAA.txt', 'r')
    d_todos_dias = [] 
    
    #Guardo los diccionarios del archivo
    for linea in archivo: #Creo una lista en la que cada elemento es un diccionario de cada dia
        linea_f = json.loads(linea)
        d_todos_dias.append(linea_f)
    
    #Guardo todas las temperaturas por mes
    dias = {} #Aca se guardan todas las temperaturas por mes
    for i in range(len(d_todos_dias)): #Recorre la lista que tiene todos los diccionarios
        for fecha in d_todos_dias[i].keys(): #recorre dia por dia
            horas = d_todos_dias[i][fecha] # Diccionario con las horas
            mes = cual_mes(fecha)
            dia = cual_dia(fecha)
            dias[fecha] = []
            if (mes == 3 and dia >= 21) or mes == 4 or mes ==5 or (mes == 6 and dia <=21):
                for hora in horas.keys(): #Recorro las horas
                    temperatura = horas[hora]['temp'] 
                    dias[fecha].append(temperatura) #Agrego todas las temperaturas en cada mes
            else:
                del dias[fecha] #Elimino los dias que no son de primavera
    
    
    #Saco las unidades de los grados
    dias_sin_unidades = {} #creo un diccionario vacio en el que cada clave es un dia y su valor es una lista con toda las temperaturas del dia
    for fechas in dias.keys():
        dias_sin_unidades[fechas] = []    #Creo la key con el dia y inicializo una lista donde se guardaran las temperaturas         
        for k in dias[fechas]:                 
            temp1 = k
            temp2 = temp1.split('°')
            temp2.pop()
            temp_final = int(temp2[0])
            dias_sin_unidades[fechas].append(temp_final)
    
    dias = 0 #Cuento los dias
    max_total = 0 #Acá acumulo las temperaturas
    for dia in dias_sin_unidades.keys(): #Recorro dia por dia buscando su maximo 
            maxima_por_dia = max(dias_sin_unidades[dia])
            max_total = max_total + maxima_por_dia #Sumo la temp del dia
            dias += 1 
    
    max_prom = max_total // dias #Saco el promedio
    
    print('La temperatura máxima promedio de la primavera es: {}°'.format(max_prom))


def dir_viento():
    archivo = open('AAAA.txt', 'r')
    d_todos_dias = [] 
    
    #Guardo los diccionarios del archivo
    for linea in archivo: #Creo una lista en la que cada elemento es un diccionario de cada dia
        linea_f = json.loads(linea)
        d_todos_dias.append(linea_f)
    
        #Guardo todas las direccion por mes
    dias = {} #Aca se guardan todas las direccion por mes
    for i in range(len(d_todos_dias)): #Recorre la lista que tiene todos los diccionarios
        for fecha in d_todos_dias[i].keys(): #recorre dia por dia
            horas = d_todos_dias[i][fecha] # Diccionario con las horas
            mes = cual_mes(fecha) 
            dia = cual_dia(fecha)
            dias[fecha] = []     #Creo una key que es la fecha y el valor es una lista vacia en donde le agregaré todas las direcciones de viento
            primavera = (mes == 9 and dia >= 21) or mes == 10 or mes ==11 or (mes == 12 and dia <=21)
            if primavera:
                for hora in horas.keys(): #Recorro las horas para extrar sus direcciones
                    direccion1 = horas[hora]['dir'] 
                    dias[fecha].append(direccion1) #Agrego todas las direcciones en cada mes
            else:
                del dias[fecha] #Elimino los dias que no son de primavera del diccionario
    
    
    todos_los_vientos = []            #Acá guardare cuantas veces se repite en el dia la direccion de un viento. La posicion de la cantidad es la misma que la posicion en la que esta dicha dirección.

    #Creo una lista con TODAS las direcciones de los vientos
    for dia in dias.keys():
        for _ in dias[dia]:
            todos_los_vientos = todos_los_vientos + dias[dia]
    
    vientos = [] #Aca guardare cuantas veces se repite cada direccion y su posicion se corresponde con la de ya_contados
    ya_contados = [] #Esta lista tiene dos propositos. Por un lado no buscar los vientos ya buscados y por otro ves su correspondencia con la lista de arriba
    
    for viento in todos_los_vientos:
        if viento not in ya_contados:
            ya_contados.append(viento) #Guardo la direccion para que no se busque en el siguiente loop. Ademas su posicion corresponde con su conteo en la linea que sigue
            repeticion = todos_los_vientos.count(viento) #Cuento cuantas veces se repite la direccion
            vientos.append(repeticion)



def main():
    estacion, anho = 'eddl', '2018' # Düsseldorf
    # estacion, anho = 'saco', '2018' # Córdoba
    # estacion, anho = 'eddb', '2018' # Berlín
    # estacion, anho = 'rjtt', '2018' # Tokio
    # clima_anho(estacion, anho, 1, 12)
    temp_min_max()
    temp_max()
    dir_viento()

# RUN

if __name__ == '__main__':
    main()
