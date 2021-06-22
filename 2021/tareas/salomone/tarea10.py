import requests
from bs4 import BeautifulSoup
import json


CLAVES = ['hora', 'desc', 'temp', 'dir', 'vel', 'hum', 'pres'] 
DIR =  './2021/tareas/salomone/'


#Creo un diccionario en el cual las claves son el numero de cada mes y cada una 
#contiene al nombre de dicho mes. (Voy a usar esto en formatear_fecha)
FERPA = {1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12:'diciembre'}

def registros_dia(fecha: str) -> dict:
    assert type(fecha) == str, 'El parametro debe ser una cadena de caracteres de formato AAAAMMD'
    #Creo un diccionario vacio.
    tablas = {}
    #Uso la funcion para formatear la fecha y asi puea extraer info de la pagina.
    nombre_fecha = formatear_fecha(fecha)
    #Las tres lineas siguientes las copie del codigo de arriba.
    contenido_url = requests.get('https://www.tutiempo.net/registros/saco/' + nombre_fecha + '.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")
    #Creo un ciclo for que se repite 23 veces.

    for u in range(24):
        #Le quito las unidades a las tablas del dia con la funcion definida anteriormente.
        tabla_del_dia_sin_unidades = eliminar_unidades(registros_tabla(tabla_dia)[u])
        #Llamo a la lista vacia que cree al principio y le agrego la tabla sin unidades
        #que toca por el ciclo for.
        tablas[u] = tabla_del_dia_sin_unidades
    #Pido que se retorne el diccionario tablas. 
    return tablas


def formatear_fecha(fecha: str) -> str:
    assert type(fecha) == str, 'El parametro debe ser una cadena de caracteres de formato AAAAMMD'
    #Creo tres variables que utilizando notacion slice les asigno un str con su 
    #respectivo valor para que la pagina del tiempo entienda la fecha.
    dia = fecha[6:]
    mes = FERPA[int(fecha[4] + fecha[5])]
    ano = fecha[:4]
    #Pido que se me retornen los valores de las variables y las concateno con guiones.
    return dia + '-' + mes + '-' + ano
    

def eliminar_unidades(registro: dict):
    assert type(registro) == dict, 'El parametro debe ser un diccionario'
    # pre:    recibe un diccionario tipo    {'desc': 'Despejado', 'temp': '13°', 'dir': 'Noroeste', 'vel': '7 km/h', 'hum': '88%', 'pres': '1015 hPa'}
    # post: modifica el propio diccionario tipo     {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015}
    #Creo un diccionario con las claves que tienen las unidades que debo borrar.
    a_borrar = {'temp': '°', 'vel': 'km/h', 'hum': '%', 'pres': 'hPa'}    
    #Asigno ese diccionario a una variable claves.    
    claves = a_borrar.keys()
    #Creo una copia del parametro.
    registrou = registro
    #Hago un ciclo for que recorre el diccionario de claves a las que les tengo 
    #que eliminar las unidades.
    
    for posicion in claves:
        #Le asigno a las variables h y g el valor de la clave que toca en el ciclo 
        #como una lista.
        h = list(registrou[posicion])
        g = list(a_borrar[posicion])
        #Creo otro ciclo que recorre los caracteres de g y si estan en h los borra
        #de h.
        for caracter in g:
            h.remove(caracter)
        #Retoco la variable h.
        h = ''.join(h)
        #Reemplazo el nuevo valor de las claves sin las unidades contenidas en h
        #en la copia del registro.
        registrou.update({posicion: int(h)})
    #Pido que se me retorne registou.
    return registrou


#Creo dos diccionarios que voy a usar mas adelante.
#Los meses tienen todos un dia mas para no sumarles 1 en un ciclo for que usare.
dias_de_meses = {1: '32' , 2: '29' , 3: '32', 4: '31' , 5: '32', 6: '31' ,7: '32', 8: '32', 9: '31', 10: '32', 11: '31', 12: '32'}
FERPA = {1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12:'diciembre'}


def clima_anho(anho: str, mes_ini: int, mes_fin: int): 
    assert type(anho) == str, 'El parametro anho debe ser una cadena de caracteres' 
    assert type(mes_ini) == type(mes_fin) == int, 'Los parametros mes_ini y mes_fin deben ser enteros'
    assert 1 <= mes_ini <= 12 and 1 <= mes_fin <= 12, 'mes_ini y mes_fin deben ser valores entre 1 y 12'
    #Creo el archico con el nombre indicado.
    archivo = open(DIR + anho + ".txt",'w')
    #Modifico el valor de la clave de febrero si el año es bisiesto. Este mes 
    #tendria un dia mas.
    if es_bisiesto(int(anho)):
        dias_de_meses[2] = '30'
    #Creo una copia del argumento mes_ini.
    mes_ini2 = mes_ini
    #Creo un while que se repite tantas veces como meses haya entre mes_ini y mes_fin.
    
    while mes_ini2 <= mes_fin:
        #Creo un for que se repite tantas veces como dias tenga el mes que toca en el
        #ciclo while. Empieza en 1, porque los meses no tienen dia 0.

        for dia in range(1, int(dias_de_meses[mes_ini2])):
            #Escribo la fecha en un formato que la pagina pueda leer.
            nombre_fecha = str(dia) + '-' + FERPA[mes_ini2] + '-' + anho
            #Descargo los datos del tiempo de la fecha dada.
            contenido_url = requests.get('https://www.tutiempo.net/registros/saco/' + nombre_fecha + '.html')
            #Estos ifs son para escribir la fecha en formato AAAAMMDD y guardarla en 
            #una variable x.
            if dia < 10:
                if mes_ini2 < 10:
                    fecha = anho + '0' + str(mes_ini2) + '0' + str(dia)
                else:
                    fecha = anho + str(mes_ini2) + '0' + str(dia)
            else:
                if mes_ini2 < 10:
                    fecha = anho + '0' + str(mes_ini2) +    str(dia)
                else:
                    fecha = anho + str(mes_ini2) +    str(dia)
            #Formateo la info que descargue de la pagina.
            contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
            tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")
            ##Creo un diccionario clima que tiene como clave la fecha en formato AAAAMMDD
            #y tiene como valor la fila de los datos del dia de esa fecha.
            clima = {fecha:registros_tabla(tabla_dia)}
            linea = json.dumps(clima)
            #Agrego al archivo el diccionario clima.
            archivo.write(linea + '\n')
        #le sumo 1 al valor de mes_ini2 para que el ciclo while finalice.
        mes_ini2 += 1
    #Cierro el archivo.
    archivo.close()


#DEFINICION DE FUNCIONES QUE VOY A USAR EN ESTE EJERCICIO.
def es_bisiesto(anho: int) -> bool:
    bisiesto = (anho % 4 == 0)
    if anho % 100 == 0 and anho % 400 != 0:
            bisiesto = False
    return bisiesto


def registro_fila_tabla(fila_tabla) -> dict: # procesa una fila de la tabla, devuelve un diccionario con las mediciones registradas en esa fila
        celdas_fila = fila_tabla.findAll('td')
        registro = {}
        i = 0
        for celda in celdas_fila:                                # recorre las celdas de la fila correspondiente a una toma de mediciones
                if celda.img != None: # si existe el tag 'img'
                        input_tag = celda.img['title'] # recupera en el tag 'img' el valor del atributo 'title'
                        registro[CLAVES[i]] = input_tag # dirección del viento
                        i = i + 1
                registro[CLAVES[i]] = celda.text
                i = i + 1
        return registro


def registros_tabla(tabla) -> dict:                    # procesa una tabla, devuelve un diccionario de registros contenidos en esa tabla
        registros = {}
        for fila_tabla in tabla.findAll('tr'):
                registro = registro_fila_tabla(fila_tabla)
                if len(registro) != 0:
                        hora = registro.pop('hora')
                        hh = int(hora[:2])
                        registros[hh] = registro
        return registros


#Creo una funcion que_mes y otra que_dia que reciben una fecha AAAAMMDD que voy 
#a usar luego.
def que_mes(fecha: str):
    if int(fecha[4]) < 1:
        mes = int(fecha[4] + fecha[5])
    else:
        mes = 10 + int(fecha[5])
    return mes


def que_dia(fecha:str):
    dia = fecha[6:]
    return int(dia)


#Creo una funcion cuantos dias que voy a usar luego.
def cuantos_dias(anho: str):
    anhos = {1: 31 , 2: 28, 3: 31, 4: 30 , 5: 31, 6: 30 ,7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    if es_bisiesto(int(anho[:4])):
        anhos[2] = 29
    res = 0
    for i in range(1, int(anho[4] + anho[5])):
        res += anhos[i]
    res += int(anho[6:])
    return res


#REDEFINICION DE LA FUNCION clima_anho.
#Creo un diccionario que voy a usar luego.
FERPA = {1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12:'diciembre'}
DIAS_DE_MESES = {1: '32' , 2: '29' , 3: '32', 4: '31' , 5: '32', 6: '31' ,7: '32', 8: '32', 9: '31', 10: '32', 11: '31', 12: '32'}
#Esta funcion es practicamente igual que clima_anho, solo cambia la linea donde
#se le asigan un valor a la variable contenido_url, donde se usa el valor del parametro 
#estacion.
def clima_anho2(estacion: str, anho: str, mes_ini: int, mes_fin: int):
    assert type(estacion) == type(anho) == str, 'anho y estacion deben ser una cadena de caracteres' 
    assert type(mes_ini) == type(mes_fin) == int, 'Los parametros mes_ini y mes_fin deben ser enteros'
    assert 1 <= mes_ini <= 12 and 1 <= mes_fin <= 12, 'mes_ini y mes_fin deben ser valores entre 1 y 12'
    archivo = open(DIR + anho + '.' + estacion + '.txt', 'w')
    if es_bisiesto(int(anho)):
        dias_de_meses[2] = '30'
    mes_ini2 = mes_ini
    while mes_ini2 <= mes_fin:
        for dia in range(1, int(DIAS_DE_MESES[mes_ini2])):
            nombre_fecha = str(dia) + '-' + FERPA[mes_ini2] + '-' + anho
            contenido_url = requests.get('https://www.tutiempo.net/registros/' + estacion + '/' + nombre_fecha + '.html')
            if dia < 10:
                if mes_ini2 < 10:
                    fecha = anho + '0' + str(mes_ini2) + '0' + str(dia)
                else:
                    fecha = anho + str(mes_ini2) + '0' + str(dia)
            else:
                if mes_ini2 < 10:
                    fecha = anho + '0' + str(mes_ini2) +    str(dia)
                else:
                    fecha = anho + str(mes_ini2) +    str(dia)
            contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
            tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")
            clima = {fecha: registros_tabla(tabla_dia)}
            linea = json.dumps(clima)
            archivo.write(linea + '\n')
        mes_ini2 += 1
    archivo.close()


#Voy a trabajar con el registro de tiempo se la ciudad de San Petersburgo, Rusia.


def temp_min_max(estacion, anho: str):
    assert type(estacion) == type(anho) == str, 'estacion y anho deben ser cadenas de caracteres'
    #Creo un diccionario que voy a usar luego.
    months = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12:[]}
    #Abro el archivo.
    archivo = open(DIR + anho + '.' + estacion + '.txt', 'r')
    #Con el siguiente for reviso linea por linea el archivo abierto anteriormente.
    for linea in archivo:
        #Paso la linea que esta en str a dicc con json.loads.
        line_in_dict = json.loads(linea)            #Linea completa
        #Obtengo la clave de la linea, que seria la fecha del dia en AAAAMMDD.
        key = " ".join(str(key) for key in line_in_dict.keys()) #Fecha de linea en AAAAMMDD.
        #Obtengo la linea sin la clave, osea, un diccionario hora por hora del dia.
        line2 = line_in_dict[key]                                                             #Linea del dia hora por hora.
        #Obtengo las claves de la linea, para que no este con el formato dict_keys['clave'].
        keys_line2 = list(line2.keys())
        #Le asigno a una variable el valor del mes en el que este el dia que esta trabajando 
        #el for.
        month_num = que_mes(key)
        #Creo un for que recorre todas las horas del dia que esta trabajando el for.
        for i in range(len(keys_line2)):
            #Obtengo el valor de la hora que toca.
            line_per_hour = line2[keys_line2[i]]
            #Obtengo la temperatura de esa hora.
            temp_per_hour = line_per_hour['temp'] 
            #Le elimino la unidad de grado.
            temp_per_hour = list(temp_per_hour)
            temp_per_hour.pop()
            temp_per_hour = ''.join(temp_per_hour)
            #Al diccionario que cree al principio con los numeros de cada mes y con valores
            #listas vacias, agrego a la lista del mes r, todas las temperaturas registradas 
            #en el mes r.
            if temp_per_hour != 'N/D':
                months[month_num].append(int(temp_per_hour))
    #Creo un ciclo for que recorre la lista months.
    for y in months:
        #Saco la maxima y la minima de cada mes.
        max_of_the_month = max(months[y])
        min_of_the_month = min(months[y])
        #Imprimo los resultados.
        print('La temperatura maxima de ' + FERPA[y] +' fue ' + str(max_of_the_month) + '°' )
        print('La temperatura minima de ' + FERPA[y] +' fue ' + str(min_of_the_month) + '°\n' )
    #Cierro el archivo.
    archivo.close()


def temp_max(estacion : str, mes_ini, mes_fin : int):
    assert type(estacion) == str, 'El parametro estacion debe ser una cadena de caracteres' 
    assert type(mes_ini) == type(mes_fin) == int, 'Los parametros mes_ini y mes_fin deben ser enteros'
    assert 1 <= mes_ini <= 12 and 1 <= mes_fin <= 12, 'mes_ini y mes_fin deben ser valores entre 1 y 12'
    #mes_ini y mes_fin deben ser los meses en los que empieza y termina la primavera
    #Abro el archivo.
    archivo = open(DIR + '2018' + '.' + estacion + '.txt', 'r') #Corrección:  hay que cerrar todos los archivos que se abren
    #Con este for creo un diccionario con 93 claves del 1 al 93, a cada una le asigno
    #como valor una lista vacia.
    dict_days = {}
    for z in range(1, 94):
        dict_days[z] = []
    #Con el siguiente for leo linea por linea el archivo.

    for linea in archivo:
        line_in_dict = json.loads(linea)            #Linea completa
        #La variable key tiene como valor la fecha de la linea, en formato AAAAMMDD.
        key = " ".join(str(key) for key in line_in_dict.keys()) #Fecha de linea en AAAAMMDD.
        #Creo dos variables r y f, la primera me dice que mes tiene la fecha de key,
        #la segunda, me dice que dia tiene la fecha de key.
        month = que_mes(key)
        day = que_dia(key)
        #Creo una condicion vara saber si la fecha que la linea que toca es de la primavera. 
        condition = month == 5 or month == 4 or (month == mes_ini and day >= 21) or (month == mes_fin and day <= 21)
        #Creo un if que filtra las fechas que son de la primavera.
        if condition:                                                                                                                                        
            #La variable line_per_hour tiene como valor un diccionario con el clima 
            #de cada hora del dia de la linea que recorre el for.
            line_per_hour = line_in_dict[key]
            #Creo un for que recorre cada hora del dia.

            for j in line_per_hour:
                #Le asigno a la variable data_hour el diccionario de la hora que esta 
                #recorriendo el for.
                data_hour = line_per_hour[j]
                #Con las siguientes lineas obtengo la temperatura de la hora del dia, y 
                #le elimino la unidad de grado.
                int_temp = data_hour['temp']
                int_temp = list(int_temp)
                int_temp.pop()
                int_temp = int(''.join(int_temp))
                #El siguiente if lo puse porque en algunos lugares la temperatura esta 
                #registrada como 'N/D', y eso me da problemas para sacar el max y el min,
                #por lo que si la temperatura no es 'N/D', la agrego al diccionario dict_days
                #en la clave del dia al que corresponda la temperatura.
                if int_temp != 'N/D':
                    dict_days[cuantos_dias(key) - 79].append(int_temp)
    archivo.close() # Agregada por mi
    #Con el siguiente for reemplazo el valor de cada clave del diccionario dict_days
    #por el valor maximo entre todos los valores de la lista que corresponde a cada
    #dia.
    for i in range(1, len(dict_days) + 1):
        dict_days[i] = max(dict_days[i])

    #Con el siguiente for imprimo la temperatura maxima de dicho dia con un texto
    #para que sea mas facil de leer.
    for g in dict_days:
        print('la temperatura maxima del dia ' + str(g) + ' de la primavera fue: ' + str(dict_days[g]) + '°')


def dir_viento(estacion : str, mes_ini, mes_fin : int):
    assert type(estacion) == str, 'El parametro estacion debe ser una cadena de caracteres' 
    assert type(mes_ini) == type(mes_fin) == int, 'Los parametros mes_ini y mes_fin deben ser enteros'
    assert 1 <= mes_ini <= 12 and 1 <= mes_fin <= 12, 'mes_ini y mes_fin deben ser valores entre 1 y 12'
    #Creo un diccionario que voy a usar mas adelante.
    wind_directions = {'Norte': 0, 'Sur': 1, 'Este': 2, 'Oeste': 3, 'Noroeste': 4, 'Nordeste': 5, 'Sureste': 6, 'Suroeste': 7, 'En calma': 8, 'Variable': 9}
    #Abro el archivo.
    archivo = open(DIR + '2018' + '.' + estacion + '.txt', 'r') # Corrección: hay que cerrar los open()
    #Creo una lista vacia.
    winds = []
    #Recorro todas las lineas del archico, es decir, todos los dias del año.
    for linea in archivo:
        #Hasta el if incluido, esta parte es igual a la de la funcion temp_max.
        line_in_dict = json.loads(linea)            #Linea completa
        key = " ".join(str(key) for key in line_in_dict.keys()) #Fecha de linea en AAAAMMDD.
        month = que_mes(key)
        day = que_dia(key)
        condition = month == 5 or month == 4 or (month == mes_ini and day >= 21) or (month == mes_fin and day <= 21)
        if condition: 
            #Creo una variable y le asigno como valor el clima del dia.                                                                                                                                     
            line_per_hour = line_in_dict[key]
            #Con el siguiente for recorro todas las horas del dia.
            for j in line_per_hour:
                #Creo una variable y le asigno como valor el clima de la hora que esta 
                #recorriendo el for.
                data_hour = line_per_hour[j]
                #Creo una variable y le asigno como valor la direccion del viento de esa
                #hora del dia.
                dir_wind = data_hour['dir']
                #Agrego el valor de dir_wind a la lista que habia creado despues de abrir 
                #el archivo.
                winds.append(dir_wind)
    archivo.close() # agregada por mi
    #Creo una lista vacia.
    winds_keys = []
    #Creo un for que se repite tantas veces como elementos tenga la lista wind,
    #que tiene la direccion del viento de cada hora de cada dia de la primavera.
    for i in range(len(winds)):
        #Agrego a la lista winds_keys Todos los vientos de la lista winds, pero en vez
        #de estar escritas en str, como por ejemplo 'Norte', estan escritas con el valor
        #que le corresponderia a esa str en el diccionario wind_directions. Por ejemplo
        #si la lista wind tenia un elemento 'Norte', la lista winds_keys tendra como
        #elemento 0.
        winds_keys.append(wind_directions[winds[i]])
        
    #Creo un diccionario vacio.
    wind_direction_keys = {}
    #El siguiente ciclo for se repite 10 veces, el total de diferentes vientos que 
    #puede haber.
    for i in range(10):
        #Se crea un diccionario que tiene como claves los numeros del 0 al 9, y a cada 
        #clave se le asigna cuantas veces se repite una direccion del viento.
        wind_direction_keys[i] = winds_keys.count(i)

    #El siguiente for recorre el diccionario que cree al principio de la definicion 
    #de la funcion.
    for a in wind_directions:
        #Se modifican los valores de las claves del diccionario dicho por cuantas veces
        #se repitio cada viento.
        wind_directions[a] = wind_direction_keys[wind_directions[a]]

    #Creo una lista vacia.
    total_winds = []
    #Recorro el diccionario que cree al principio de la definicion de la funcion.
    for x in wind_directions:
        #Agrego a la lista que cree anteriormente los valores de las claves de wind_directions,
        #es decir,cuantas veces se repitio cada viento.
        total_winds.append(wind_directions[x])

    #Creo una variable que toma como valor cuantas veces se repitio el viento predominante.
    main_wind = max(total_winds)
    #Recorro la lista wind_directions y si la variable main_wind es igual a el valor
    #de alguna clave de dicho diccionario, esa clave sera el viento predominante.
    for z in wind_directions:
        if wind_directions[z] == main_wind:
            #Imprimo el resultado.
            print('La dirección del viento predominante durante la primavera de 2018 en San Petersburgo fue ' + z)



def main():
    # clima_anho2('ulli', '2018', 1, 12)
    #temp_min_max('ulli', '2018')
    temp_max('ulli', 3, 6)
    #dir_viento('ulli', 3, 6)


# RUN

if __name__ == '__main__':
    main()