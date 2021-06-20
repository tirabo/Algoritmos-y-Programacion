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

# Devuelve un diccionario de diccionarios
def registros_dia(dia, mes, año) -> dict:
    nombre_fecha = str(dia) + '-' + mes + '-' + str(año)
    contenido_url = requests.get('https://www.tutiempo.net/registros/saco/' + nombre_fecha + '.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")
    
    return registros_tabla(tabla_dia)

def formatear_fecha(fecha: str) -> str:
    # pre:  fecha es una fecha en el formato 'AAAAMMDD'
    # post: devuelve la fecha  en el foma dia-nombre del mes-año
    meses = {1:'enero', 2:'febrero', 3:'marzo', 4:'abril', 5:'mayo', 6:'junio', 7:'julio', 8:'agosto', 9:'septiembre', 10:'octubre', 11:'noviembre', 12:'diciembre'}
    fecha_int = int(fecha)
    dia = fecha_int % 100
    mes = ((fecha_int % 10000) - dia) // 100
    anho = (fecha_int - mes - dia) // 10000
    mes_str = meses[mes]
    return str(dia) + '-' + mes_str + '-' + str(anho)

def eliminar_unidades(registro: dict):
    # pre:  recibe un diccionario tipo  {'desc': 'Despejado', 'temp': '13°', 'dir': 'Noroeste', 'vel': '7 km/h', 'hum': '88%', 'pres': '1015 hPa'}
    # post: modifica el propio diccionario tipo   {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015}
    unidades = {'temp': '°', 'vel': 'km/h', 'hum': '%', 'pres': 'hPa'}
    claves = unidades.keys()
    registro2 = registro
    for parametro in claves:
        updater = list(registro2[parametro])
        unidad = list(unidades[parametro])
        for caracter in unidad:
            updater.remove(caracter)
        updater = ''.join(updater)
        registro2.update({parametro: int(updater)})
    return registro2


# diccionarios auxiliares
dias_meses = {1: '32' , 2: '29' , 3: '32', 4: '31' , 5: '32', 6: '31' ,7: '32', 8: '32', 9: '31', 10: '32', 11: '31', 12: '32'} # un día de más para que el for corra hasta el anterior
nombre_meses = {1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'}
# función auxiliar
def anho_bisiesto(anho: int) -> bool:
    dev = anho % 4 == 0 and anho % 100 != 0 or anho % 400 == 0
    return dev

# definiciónn de la función
def clima_anho(anho: str, mes_ini: int, mes_fin: int):

    archivo = open('./2021/tareas/caruso/'+anho + ".txt", "w")                                          # abre el archivo
    if anho_bisiesto(int(anho)):                                                # si el año es bisiesto se le agrega un día a febrero
        dias_meses[2] = '30'

    mes_inicio = mes_ini                                                        # llama al argumento mes_ini como mes_inicio

    while mes_inicio <= mes_fin:                                                # recorre los meses solicitados en el argumento
        for i in range(1, int(dias_meses[mes_inicio])):                           # recorre los días del mes que recorre el while
            nombre_fecha = str(i) + '-' + nombre_meses[mes_inicio] + '-' + anho                             # fecha formateada
            url = requests.get('https://www.tutiempo.net/registros/saco/' + nombre_fecha + '.html')         # descarga de datos
            # guardo la fecha en formato AAAAMMDD en la variable month
            if i < 10:
                if mes_inicio < 10:
                    month = anho + '0' + str(mes_inicio) + '0' + str(i)
                else:
                    month = anho + str(mes_inicio) + '0' + str(i)
            else:
                if mes_inicio < 10:
                    month = anho + '0' + str(mes_inicio) + str(i)
                else: 
                    month = anho + str(mes_inicio) + str(i)
            contenido = BeautifulSoup(url.text, 'lxml')                             # analiza la página, saca atributos
            tabla_del_dia = contenido.find('table', {'style': 'width: 100%'})       # extrae lo solicitado
            clima = {month: registros_tabla(tabla_del_dia)}                         # diccionario con clave = m (AAAMMDD) y valor = datos del día     
            month = json.dumps(clima)
            archivo.write(month + '\n')                                             # al archivo le agrega el diccionario creado
        mes_inicio = mes_inicio + 1                                               # para que finalice el while, suma 1 a mes_inicio

    archivo.close()

# clima_anho('2018',1,1) # Ver si se generó el archivo correctamente del primer mes del año 2018


def registros_dia2(estacion: str, fecha: str) -> dict:
    tablas = {}
    nombre_fecha = formatear_fecha(fecha)
    contenido_url = requests.get('https://www.tutiempo.net/registros/' + estacion + '/' + nombre_fecha + '.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'})
    horas = registros_tabla(tabla_dia).keys()
    for i in horas:
        tabla_dia_sin_unidades = eliminar_unidades(registros_tabla(tabla_dia)[i])
        tablas[i] = tabla_dia_sin_unidades
    return tablas

def clima_anho2(estacion: str, anho: str, mes_ini: int, mes_fin: int):
    archivo = open('./2021/tareas/caruso/'+anho + '.' + estacion + ".txt", "w")
    if anho_bisiesto(int(anho)):
        dias_meses[2] = '30'
    mes_inicio = mes_ini
    while mes_inicio <= mes_fin:
        for i in range(1, int(dias_meses[mes_inicio])):
            nombre_fecha = str(i) + '-' + nombre_meses[mes_inicio] + '-' + anho
            url = requests.get('https://www.tutiempo.net/registros/' + estacion + '/' + nombre_fecha + '.html')
            if i < 10:
                if mes_inicio < 10:
                    month = anho + '0' + str(mes_inicio) + '0' + str(i)
                else:
                    month = anho + str(mes_inicio) + '0' + str(i)
            else:
                if mes_inicio < 10:
                    month = anho + '0' + str(mes_inicio) + str(i)
                else: 
                    month = anho + str(mes_inicio) + str(i)
            contenido = BeautifulSoup(url.text, 'lxml')
            tabla_del_dia = contenido.find('table', {'style': 'width: 100%'})
            clima = {month: registros_tabla(tabla_del_dia)}
            month = json.dumps(clima)
            archivo.write(month + '\n')
        mes_inicio = mes_inicio + 1
    archivo.close()

# clima_anho2('mmun', '2018', 1, 12)   


# diccionarios auxiliares
nombre_meses = {1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'}
meses = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
meses_no_unid = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
direcciones_viento = {"Norte": 0, "Sur": 1, "Este": 2, "Oeste": 3, "Nordeste": 4, "Noroeste": 5, "Sureste": 6, "Suroeste": 7, "En calma": 8, "Variable": 9} #Corrección

# funciones auxiliares
def el_mes(fecha: str) -> int:
    fecha_int = int(fecha)
    dia = fecha_int % 100
    mes = ((fecha_int % 10000) - dia) // 100
    return mes

def el_dia(fecha:str) -> int:
    fecha_int = int(fecha)
    dia = fecha_int % 100
    return dia


# funciones del ejercicio 3

def temp_min_max(estacion, anho):
    # pre: obtiene una estación y un año
    # post: devuelve las temperaturas mínimas y máximas de cada mes del año solicitado de la estación elegida
    
    archivo = open('./2021/tareas/caruso/'+anho + '.' + estacion + '.txt', 'r')                           # abre el archivo
    t_dias = []

    for linea in archivo:                                                         # recorre las lineas del archivo y las guarda
        linea_dic = json.loads(linea)
        t_dias.append(linea_dic)

    for i in range(len(t_dias)):                                                  # recorre la lista que tiene los dic
        for fecha in t_dias[i].keys():                                              # recorre día por día
            horas = t_dias[i][fecha]                                                  # dic que contiene las horas 
            mes = el_mes(fecha)                                                       # le asigna el mes que es
            for hora in horas.keys():                                                 # recorre c/hora
                temperatura = horas[hora]['temp']                                       # toma la temp de c/hora
                meses[mes].append(temperatura)                                          # guarda cada temp por hora del mes

    for h in meses.keys():                                                        # cambia la unidad de grado (x°) a un entero
        for j in range(len(meses[h])):
            temp_a = meses[h][j]
            temp_b = temp_a.split('°')
            temp_b.pop()
            if temp_b[0] != 'N/D':
                temp_no_unid = int(temp_b[0])
                meses_no_unid[h].append(temp_no_unid)
                                                        
    for i in range(1, 12 + 1):                                                    # averigua máximos y mínimos
        if len(meses_no_unid[i]) != 0: 
            maximo = max(meses_no_unid[i]) #Corrección: max por maximo
            minimo = min(meses_no_unid[i]) #Corrección: min por minimo
            print('La temperatura máxima del mes {} fue {}°'.format(i, maximo))       # imprime los resultados
            print('La temperatura mínima del mes {} fue {}°'.format(i, minimo))
            print('\n')

    archivo.close()                                                               # cierra el archivo



def temp_max(estacion, mes_ini, mes_fin):
    # pre: recibe una estación meteorológica y un mes de inicio y de fin
    # post: devuelve el promedio de temperaturas máximas diarias durante la primavera del año 2018 en la ciudad elegida.

    archivo = open('./2021/tareas/caruso/'+'2018' + '.' + estacion + '.txt', 'r')                         # abre el archivo
    t_dias = []                      
    
    for linea in archivo:                                                         # recorre las lineas del archivo y las guarda
        linea_dic = json.loads(linea)
        t_dias.append(linea_dic)

    dias = {}                                                                     # para guardar las temp de c/ mes
    for i in range(len(t_dias)):                                                  # recorre la lista que tiene los dic
        for fecha in t_dias[i].keys():                                              # recorre c/ dia
            horas = t_dias[i][fecha]                                                  # dic que contiene las horas
            mes = el_mes(fecha)                                                       # le asigna el mes que es
            dia = el_dia(fecha)                                                       # le asigna el día que es
            dias[fecha] = []
            primavera_cond = (mes == 3 and dia >= 20) or mes == 4 or mes == 5 or (mes == 6 and dia <= 21)     
            if primavera_cond:                                                        # implementa la condición de que fecha sea primavera
                for hora in horas.keys():                                               # recorre c/ hora
                    temp = horas[hora]['temp'] 
                    dias[fecha].append(temp)                                              # guarda las temp en c/ mes
            else:
                del dias[fecha]                                                         # elimina los dias que no cumplen la condición
                
    dias_no_unid = {}                                                             # dic vacio con clave = dia y valor = lista de temp del día
    for fechas in dias.keys():
        dias_no_unid[fechas] = []                                                   # lista para guardar temp    
        for h in dias[fechas]:                                                      # recorre y saca unidades
            temp_a = h
            temp_b = temp_a.split('°')
            temp_b.pop()
            #temp_no_unid = int(temp_b[0]) #Corrección: esta linea no está bien (las 3 que siguen son mias)
            if temp_b[0] != 'N/D':
                temp_no_unid = int(temp_b[0])
                dias_no_unid[fechas].append(temp_no_unid)

    dias = 0 
    max_total = 0 
    for dia in dias_no_unid.keys():                                               # recorre c/dia y averigua el max
        max_dia = max(dias_no_unid[dia])
        max_total = max_total + max_dia 
        dias = dias + 1

    max_prom = max_total // dias                                                  # saca el prom
    
    print('La temperatura máxima promedio diaria de la primavera fue {}°'.format(max_prom))     # imprime el resultado

    archivo.close()                                                               # cierra el archivo

# temp_min_max('mmun', '2018')
# temp_max('mmun', 3, 5)


def dir_viento(estacion, mes_ini, mes_fin):
    # pre: recibe una estación meteorológica y un mes de inicio y de fin
    # post: devuelve la dirección del viento predominante durante la primavera del año 2018 en la ciudad elegida.

    archivo = open('./2021/tareas/caruso/'+'2018' + '.' + estacion + '.txt', 'r')                         # abre el archivo
    t_dias = []     

    for linea in archivo:                                                         # recorre las lineas del archivo y las guarda
        linea_dic = json.loads(linea)
        t_dias.append(linea_dic)    
    mes,  dia , hora,  fecha, horas  = -1, -1, '', '', {} # esta línea la agregué yo como para que no cante errores
    dias = {}                                                                     # para guardar las direc de c/ mes
    for i in range(len(t_dias)):                                                  # recorre la lista que tiene los dic
        for fecha in t_dias[i].keys():                                              # recorre c/ dia
            horas = t_dias[i][fecha]                                                  # dic de c/ hora
            mes = el_mes(fecha)                                                       # asigna el mes que es
            dia = el_dia(fecha)                                                       # asigna el día que es
            dias[fecha] = []  
        condicion = (mes == 3 and dia >= 20) or mes == 4 or mes == 5 or (mes == 6 and dia <= 21)
        if condicion:                                                               # implementa la condición de que fecha sea primavera
            # print(mes, dia,  fecha)
            for hora in horas.keys():                                                 # recorre c/ hora
                direccion1 = horas[hora]['dir'] 
                dias[fecha].append(direccion1)                                          # guarda las direc de c/mes
        else:
            del dias[fecha]                                                           # elimina los dias que no cumplen la condición
    # print(dias)
    vientos = []                                                                  # para guardar las rep de vientos en el día
    for dia in dias.keys():
        for _ in dias[dia]:
            vientos = vientos + dias[dia]     
    #  print(vientos) # son todas las direcciones hora por hora de la primavera
    vient = []                                                                    # para guardar las rep de c/ viento
    rep = []          
    for viento in vientos:
        if viento not in rep:
            rep.append(viento)                                                        # guarda la direc
            repeticion = vientos.count(viento)                                        # cant de veces que se rep la direc
            vient.append(repeticion)   

    rep_viento_pred = max(vient) 
    #viento_predominante = ya_contados[vient.index(rep_viento_pred)]               # averigua el viento predominante
    # print("La dirección del viento predominante durante la primavera del año 2018 en la ciudad elegida fue" + viento_predominante)    # resultado

    #Las próximas líneas son mías
    viento_acumulado = {}
    for direccion  in direcciones_viento:
        viento_acumulado[direccion] = 0
    for viento in vientos:
        viento_acumulado[viento] = viento_acumulado[viento] + 1
    # print(viento_acumulado)
    viento_predominante = ['', 0]
    for dir in viento_acumulado:
        if viento_acumulado[dir] > viento_predominante[1]:
            viento_predominante = [dir, viento_acumulado[dir]]
    print("La dirección del viento predominante durante la primavera del año 2018 en la ciudad elegida fue " + viento_predominante [0])
    # Hasta aqui terminaron mis lineas

    archivo.close() 

dir_viento('mmun', 3, 5)