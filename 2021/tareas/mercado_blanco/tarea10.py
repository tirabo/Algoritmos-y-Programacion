import requests
from bs4 import BeautifulSoup
import json

CLAVES = ['hora', 'desc', 'temp', 'dir', 'vel', 'hum', 'pres'] 
DIR = './2021/tareas/mercado_blanco/'

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
    assert type(fecha) == str,'Debe ingresar una fecha entre comillas, esta debe estar en formato AAAAMMDD'
    # post: devuelve la fecha    en el foma dia-nombre del mes-año
    
    #creamos un diccionario que tiene como clave los numeros de meses y como valor a sus correspondientes nombres
    nombre_mes = {1:'enero',2:'febrero',3:'marzo',4:'abril',5:'mayo',6:'junio',7:'julio',8:'agosto',9:'septiembre',10:'octubre',11:'noviembre', 12:'diciembre'}

    #indexo los ultimos dos digitos de la fecha, que seran los dias, seguido del valor del diccionario indexado en el mes que tiene la fecha y por ultimo el año, que son los primeros 4 digitos.
    fecha_formateada = fecha[6:8] + '-' + nombre_mes[int(fecha[4:6])] + '-' + fecha[:4] 

    return fecha_formateada

def eliminar_unidades(registro: dict):
    # pre:    recibe un diccionario tipo    {'desc': 'Despejado', 'temp': '13°', 'dir': 'Noroeste', 'vel': '7 km/h', 'hum': '88%', 'pres': '1015 hPa'}
    assert type(registro) == dict, 'El argumento debe ser un diccionario con datos del clima'
    # post: modifica el propio diccionario tipo     {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015}
    #creo un diccionario donde coloco las unidades indeseadas en cada clave del diccionario
    indes = {'temp': '°', 'vel': 'km/h', 'hum': '%', 'pres': 'hPa'}
    #Extraigo las claves del diccionario para luego recorrelas 
    claves = indes.keys()
    #recorro cada clave
    for posicion in claves:
        #creo dos listas, una con el valor del diccionario al cual eliminare las unidades y otra con el valor del dicccionario de las unidades que deseo eliminar.
        list1 = list(registro[posicion])
        list2 = list(indes[posicion])
        #recorro cada caracter de la lista de unidades indeseadas y elimino ese caracter en la lista original
        for caracter in list2:
            list1.remove(caracter)
        #elimino los espacios que me quedaron
        list1 = ''.join(list1)
        #al diccionario que tuve de argumento le hago un update en la clave que recorro en el for principal y el valor, seria el elemento de la lista 1 al cual eliminamos las unidades.
        registro.update({posicion: int(list1)})
    return registro



#creo 3 listas, una con los dias de los meses de un año comun, y otra con los dias de los meses de un año bisiesto.
#La lista meses, es basicamente una lista de strings con los nombres de los meses en orden
mesescomun = [31,28,31,30,31,30,31,31,30,31,30,31]
mesesbisiesto = [31,29,31,30,31,30,31,31,30,31,30,31]
meses = ['enero', 'febrero', 'marzo' ,'abril','mayo', 'junio', 'julio','agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

#Esta funcion permite obtener un año, mes, dia y devolverlos en formato AAAAMMDD
def rellenar_fecha(anho: int, mes: int, dia: int):
    # if mes<10:
    #     mes = '0' + str(mes) #
    # if dia<10:
    #     dia = '0' + str(dia)
    # fecha = str(anho) + str(mes) + str(dia)
    fecha = str(anho) + '{:02}'.format(mes) + '{:02}'.format(dia) # Corrección: las líneas anteriores se pueden reemplazar por esta
    return fecha


#La ciudad a trabajar es Tokio, Japón. (siglas de estacion: rjtt)
#Defina el anho en el que va a trabajar:
anho = '2018'

# redefinir 
def registros_dia(estacion: str, fecha: str) -> dict:
    #precondicion: un string representando a la fecha en formato AAAAMMDD y el codigo de la estacion en str
    assert type(fecha) == type(estacion) == str , 'Debe ingresar una fecha entre comillas, esta debe estar en formato AAAAMMDD'
    #post: devuelve el diccionario con los datos del clima en ese dia sin las unidades
    nombre_fecha = formatear_fecha(fecha)

    #extraigo los datos de la pagina a usar, modificando el url con la fecha dada y la estacion ingresada como argumento
    contenido_url = requests.get('https://www.tutiempo.net/registros/'+ estacion +'/' + nombre_fecha + '.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")
    
    dicc = registros_tabla(tabla_dia)
    claves = dicc.keys()    
    for clave in claves:
        dicc[clave] = eliminar_unidades(dicc[clave])
    return dicc

def clima_anho(estacion: str, anho: str, mes_ini: int, mes_fin: int):
    #pre: anho es un str, mes_ini y mes_fin son enteros tal que mes_ini<=mes_fin
    assert type(anho) == type(estacion) == str and type(mes_ini) == type(mes_fin) == int and mes_ini>0 and mes_ini<=12 and    mes_fin>0 and mes_fin<=12    and mes_ini <= mes_fin, 'el primer argumento es una cadena, el segundo y tercer argumento son enteros de meses, tal que el primero es menor o igual al segundo' 
    #post: crea un archivo de texto donde se guardan los datos del clima de CBA entre los meses introducidos

    if int(anho) %    4 == 0 and (int(anho) % 100 != 0 or int(anho) % 400 == 0):
        d_mes = mesesbisiesto
    else:
        d_mes = mesescomun
    archivo = open(DIR + anho + estacion + '.txt','w') 
    while mes_ini <= mes_fin:
        for dia in range(1, d_mes[mes_ini-1]+1):
            fecha1 = str(dia) + '-' + meses[mes_ini-1] + '-' + anho
            #Extraigo los datos de la pagina web modificando la url con la fecha formada y la estacion como nuevo argumento en esta modificacion.
            contenido_url = requests.get('https://www.tutiempo.net/registros/'+ estacion +'/' + fecha1 + '.html')         
            contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml')
            tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")

            fecha2 = rellenar_fecha(int(anho), mes_ini, dia)
            dicc = {}    
            dicc[fecha2] = registros_tabla(tabla_dia)
            agg = json.dumps(dicc)
            archivo.write(agg)
            archivo.write('\n')
        mes_ini += 1
    archivo.close()

#Llamo a la funcion con la estacion correspondiente a Tokio, Japon, para crear el archivo con la información de los 12 meses.
#clima_anho('rjtt', anho, 1, 12) #descomentar para generar el archivo de todos los datos del clima de todos los dias del añon de Tokio, Japon.

def temp_min_max(estacion: str, anho: str):
    #pre: recibe una estacion metereologica y un año, ambos en str
    assert type(estacion) == type(anho) == str, 'La estacion ingresada y el año ingresado deben ser en formato de cadena'
    #post: devuelve las temperaturas maximas y minimas de cada mes del año introducido en un diccionario
    #defino el primer dia para analizar los cambios de meses y un contador para guardar temperaturas de cada mes
    fecha_copia = anho+'0101'
    #este contador seran las claves para acceder al diccionario "temp_meses"
    contador = 1
    #Esta variable sirve para la conversión de un str como "10°" a un entero como 10
    temp1 = []
    #creo un diccionario donde separare las temperaturas por meses
    temp_meses = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[]}
    #abro el archivo para su lectura
    archivo = open(DIR + anho+ estacion +'.txt', 'r')
    #recorro cada linea del archivo
    for linea in archivo:
        #convierto la linea en diccionario
        temporal1 = json.loads(linea)
        #con el siguiente for entro al primer nivel del diccionario, que tiene como clave las fechas
        for fecha in temporal1.keys():
            #El siguiente condicional compara si hubo un cambio en el mes, en dicho caso, aumenta el
            #contador en 1, para empezar a guardar las temperaturas en el mes siguiente del diccionario temp_meses
            if fecha[4:6] != fecha_copia[4:6]:
                fecha_copia = fecha
                contador += 1
            #Con el siguiente for entro al segundo nivel del diccionario, que tiene como clave las horas 
            for horas in temporal1[fecha].keys():
                    #Separo el simbolo de grado del numero, al ser una lista, esta se 
                    #separa en dos elementos, numero como str primero y ° como str segundo
                    temp1 = temporal1[fecha][horas]['temp'].split('°')
                    #tomo el primer elemento de la lista, es decir el numero y lo convierto a entero, 
                    #a este lo agrego al diccionario en clave contador (el que aumenta en 1 cada que cambia el mes) y como el 
                    #valor es una lista, uso append.
                    temp_meses[contador].append(int(temp1[0]))
    #Por ultimo recorro el diccionario con todas las temperaturas
    for almendra in temp_meses.keys():
        #Saco maximos y minimos de cada lista
        maximo = max(temp_meses[almendra])
        minimo = min(temp_meses[almendra])
        #imprimo la temperatura maxima y minima
        print(f'La temperatura maxima del mes {almendra} es {maximo} ')
        print(f'La temperatura minima del mes {almendra} es {minimo} \n')
    #cierro el archivo
    archivo.close()

#Ya que la primavera comienza en un mes y dia especifico, agregue dias inicial y final en argumentos. Usa el año definido a principio de celda.
def temp_max(estacion: str, mes_ini_primavera:int, dia_ini_primavera: int, mes_fin_primavera: int, dia_fin_primavera: int):
    #pre: recibo la estacion a trabajar en str y los meses y dias de inicio de la primavera como enteros
    assert type(estacion) == str, 'La estacion ingresada debe ser en formato str'
    assert type(mes_ini_primavera) == type(mes_fin_primavera) == type(dia_fin_primavera) == type(dia_ini_primavera) == int, 'los meses y dias de inicio y final de primavera deben ser enteros'
    #post: devuelvo el promedio de las temperaturas maximas de la primavera en el año definido al principio de celda
    #defino el primer dia para analizar los cambios de meses
    fecha_copia = anho+'0101'
    #defino al maximo hipotetico como -273 porque es la temperatura mas baja que pueda existir
    maximo = -273
    #este contador seran las claves para acceder al diccionario "dicc_primavera"
    contador = 1
    contador2 = 1
    #Esta variable hará la sumatoria para luego hacer el promedio
    suma = 0.
    contador_para_promedio = 0
    #Esta variable sirve para la conversión de un str como "10°" a un entero como 10
    temp1 = []
    #creo un diccionario donde separare las temperaturas por meses y otro que guardara solo la de los dias de la primavera
    dicc = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[]}
    dicc_primavera = {}
    #defino una lista con los dias de los meses
    d_meses = [31,28,31,30,31,30,31,31,30,31,30,31]
    #abro el archivo para su lectura
    archivo = open(DIR + anho + estacion +'.txt', 'r')
    #recorro cada linea del archivo
    for linea in archivo:
        #convierto la linea en diccionario
        temporal1 = json.loads(linea)
        #con el siguiente for entro al primer nivel del diccionario, que tiene como clave las fechas
        for fecha in temporal1.keys():
            #El siguiente condicional compara si hubo un cambio en el mes, en dicho caso, aumenta el
            #contador en 1, para empezar a guardar las temperaturas en el mes siguiente del diccionario
            if fecha[4:6] != fecha_copia[4:6]:
                fecha_copia = fecha
                contador += 1
            #Con el siguiente for entro al segundo nivel del diccionario, que tiene como clave las horas 
            for horas in temporal1[fecha].keys():
                #Separo el simbolo de grado del numero, al ser una lista, esta se 
                #separa en dos elementos, numero como str primero y ° como str segundo
                temp1 = temporal1[fecha][horas]['temp'].split('°')
                #calculo si la temperatura de esa hora es mayor al de la hora anterior, en ese caso guardo en maximo
                if int(temp1[0])>=maximo:
                    maximo = int(temp1[0])
            #agrego al diccionario la temperatura maxima del dia
            dicc[contador].append(maximo)
            maximo = -273 #reseteo el maximo
    # print(dicc)
    #Por ultimo recorro el diccionario con todas las temperaturas
    for almendra in dicc.keys():
        #acoto el diccionario "dicc" a un nuevo diccionario llamado dicc_primavera 
        #que tiene solo los maximos de los dias de la primavera
        if almendra>=mes_ini_primavera and almendra<=mes_fin_primavera:
            if almendra == mes_ini_primavera:
                dicc_primavera[almendra] = dicc[almendra][dia_ini_primavera:]
            elif almendra == mes_fin_primavera:
                dicc_primavera[almendra] = dicc[almendra][:dia_fin_primavera]
            else:
                dicc_primavera[almendra] = dicc[almendra]
    #hago la sumatoria de todas las temperaturas maximas de todos los dias de la primavera y aparte llevo un contador para luego sacar el promedio
    for castanha in dicc_primavera.keys():
        for elemento in dicc_primavera[castanha]:
            suma += elemento
            contador_para_promedio += 1
    #calculo el promedio y lo imprimo por pantalla
    promedio = suma/contador_para_promedio
    print('El promedio de las temperaturas maximas de los dias de la primavera es {:.2f} grados'.format(promedio))
    #cierro el archivo
    archivo.close()


def dir_viento(estacion: str, mes_ini_primavera:int, dia_ini_primavera: int, mes_fin_primavera: int, dia_fin_primavera: int):
    #pre: recibo la estacion a trabajar en str y los meses y dias de inicio de la primavera como enteros
    assert type(estacion) == str, 'La estacion ingresada debe ser en formato str'
    assert type(mes_ini_primavera) == type(mes_fin_primavera) == type(dia_fin_primavera) == type(dia_ini_primavera) == int, 'los meses y dias de inicio y final de primavera deben ser enteros'
    #post: devuelvo    la dirección del viento predominante durante la primavera en el año definido al principio de celda
    #defino el primer dia para analizar los cambios de meses
    fecha_copia = anho+'0101'
    #Estas lista guarda todos los vientos de toda la primavera
    todos_los_vientos1 = []
    todos_los_vientos2 = []
    #La primera lista guarda los vientos, y la segunda la cantidad de veces que este se repite.
    vientos = []
    repeticiones_vientos = []
    #este contador seran las claves para acceder al diccionario "dicc"
    contador = 1
    #defino la variable que me guardara la cantidad que se repitio el 
    #viento mas predominante y otra que guarda la posicion que esta tendra en la lista de vientos
    maximo = 0
    posicion_maximo = 0
    #creo un diccionario donde separare las direcciones del viento por meses y otro que guardara solo la de los dias de la primavera
    dicc = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[]}
    dicc_primavera = {}
    #defino una lista con los dias de los meses
    d_meses = [31,28,31,30,31,30,31,31,30,31,30,31]
    #abro el archivo para su lectura
    archivo = open(DIR + anho + estacion +'.txt', 'r')
    #recorro cada linea del archivo
    for linea in archivo:
        #convierto la linea en diccionario
        temporal1 = json.loads(linea)
        #con el siguiente for entro al primer nivel del diccionario, que tiene como clave las fechas
        for fecha in temporal1.keys():
            #El siguiente condicional compara si hubo un cambio en el mes, en dicho caso, aumenta el
            #contador en 1, para empezar a guardar las direcciones en el mes siguiente del diccionario dicc
            if fecha[4:6] != fecha_copia[4:6]:
                fecha_copia = fecha
                contador += 1
            #Con el siguiente for entro al segundo nivel del diccionario, que tiene como clave las horas 
            for horas in temporal1[fecha].keys():
                #agrego a dicc la direccion del viento de cada hora
                dicc[contador].append(temporal1[fecha][horas]['dir'])
    #Por ultimo recorro el diccionario con todas las direcciones de los vientos
    for almendra in dicc.keys():
        #acoto el diccionario "dicc" a un nuevo diccionario llamado "dicc_primavera" 
        #que tiene solo las direcciones del viento de los dias de la primavera
        if almendra>=mes_ini_primavera and almendra<=mes_fin_primavera:
            if almendra == mes_ini_primavera:
                dicc_primavera[almendra] = dicc[almendra][dia_ini_primavera:]
            elif almendra == mes_fin_primavera:
                dicc_primavera[almendra] = dicc[almendra][:dia_fin_primavera]
            else:
                dicc_primavera[almendra] = dicc[almendra]
    #A todos los valores de dicc_primavera los juntos en una lista de listas
    for castanha in dicc_primavera.keys():
        todos_los_vientos1.append(dicc_primavera[castanha])
    #Aplano la lista de listas para tener solamente una dimension en la lista.
    for i in range(len(todos_los_vientos1)):
        for j in range(len(todos_los_vientos1[i])):
            todos_los_vientos2.append(todos_los_vientos1[i][j])
    #recorro la lista de todos los vientos de la primavera
    for viento in todos_los_vientos2:
        #Si el viento no esta en la lista vientos, lo guardo en esta y en otra lista guardo las veces que este se repitio en total.
        if viento not in vientos:
            vientos.append(viento)
            repeticiones_vientos.append(todos_los_vientos2.count(viento))
    #en la lista de repeticiones_vientos, busco el más repetido y guardo su posicion. Esta posicion corresponde al nombre del viento mas repetido en la lista vientos
    for i in range(len(repeticiones_vientos)):
        if repeticiones_vientos[i] > maximo:
            posicion_maximo = i
            maximo = repeticiones_vientos[i]
    #teniendo la posicion maxima del viento mas predominanto, hago la impresion por pantalla
    print(f'La direccion del viento mas predominante durante la primavera fue: {vientos[posicion_maximo]}')
    #cierro el archivo
    archivo.close()

"""A partir de las funciones definidas previamente y de estas dos funciones,    se deberán definir tres funciones que devuelven los resultados deseados    en el formato que les resulte más conveniente.

Finalemente, deberán ejecutar las funciones y mostrar los resultados obtenidos.
"""
def main():
    estacion, anho = 'rjtt', '2018' # Tokio
    # clima_anho(estacion, anho, 1, 12)
    temp_min_max('rjtt', '2018')
    temp_max('rjtt',3,20,6,21)
    dir_viento('rjtt',3,20,6,21)

# RUN

if __name__ == '__main__':
    main()


